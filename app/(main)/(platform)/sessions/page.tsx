// 'SessionsPage' displays a list of previously saved tagging sessions. If no
// sessions exist, the user is redirected to the upload page. Selecting a
// session loads its associated report into localStorage and navigates to the
// editor page.

'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { axiosInstance } from '@/lib/axios';
import { toast } from 'sonner';
import type { ReportDocument } from '@/types/report';
import type { ReportBlock, XbrlTag } from '@/types/report';

interface SessionSummary {
  id: string;
  name: string;
  created_at?: string;
  updated_at?: string;
}

/**
 * Merge multiple blocks of a report into a single block.
 * See mergeReportBlocks in other files for details.
 */
function mergeReportBlocks(report: ReportDocument): ReportDocument {
  if (!report.blocks || report.blocks.length <= 1) {
    return report;
  }
  let combinedContent = '';
  const combinedTags: XbrlTag[] = [];
  let offset = 0;
  report.blocks.forEach((block, idx) => {
    combinedContent += block.content;
    block.tags?.forEach((tag) => {
      const start = tag.startIndex ?? 0;
      const end = tag.endIndex ?? block.content.length;
      combinedTags.push({
        ...tag,
        startIndex: start + offset,
        endIndex: end + offset,
      });
    });
    offset += block.content.length;
    if (idx < report.blocks.length - 1) {
      combinedContent += '\n\n';
      offset += 2;
    }
  });
  const combinedBlock: ReportBlock = {
    id: `combined-block-${report.id}`,
    content: combinedContent,
    type: report.blocks[0].type,
    tags: combinedTags,
  };
  return {
    ...report,
    blocks: [combinedBlock],
  };
}

export default function SessionsPage() {
  const router = useRouter();
  const [sessions, setSessions] = useState<SessionSummary[] | null>(null);
  const [loading, setLoading] = useState(true);

  // Fetch sessions on mount. Redirect to upload if none are found.
  useEffect(() => {
    const fetchSessions = async () => {
      try {
        const res = await axiosInstance.get<SessionSummary[]>('/sessions');
        setSessions(res.data);
      } catch (err) {
        console.error('Failed to fetch sessions', err);
        toast.error('Failed to load saved sessions');
        setSessions([]);
      } finally {
        setLoading(false);
      }
    };
    fetchSessions();
  }, []);

  // When sessions load, redirect to upload page if empty.
  useEffect(() => {
    if (!loading && sessions && sessions.length === 0) {
      router.replace('/upload');
    }
  }, [loading, sessions, router]);

  const handleSessionSelect = async (sessionId: string) => {
    try {
      const res = await axiosInstance.get(`/sessions/${sessionId}`);
      const session = res.data;
      const reportData = session?.data as ReportDocument;
      // If the session originates from a PDF report, preserve the
      // page‑level blocks. Otherwise, merge all blocks into one to
      // simplify editing and maintain tag indices.
      const isPdf = reportData?.file_type?.toLowerCase().includes('pdf');
      const merged = isPdf ? reportData : mergeReportBlocks(reportData);
      if (typeof window !== 'undefined') {
        localStorage.setItem('xbrl-editor-session', JSON.stringify(merged));
        // Persist session ID so subsequent saves update the same record
        localStorage.setItem('xbrl-session-id', sessionId);
      }
      router.push('/editor');
    } catch (err) {
      console.error('Failed to load session', err);
      toast.error('Failed to load session');
    }
  };

  if (loading || !sessions) {
    return (
      <div className='flex items-center justify-center py-8'>
        <p className='text-sm text-muted-foreground'>Loading your sessions…</p>
      </div>
    );
  }

  return (
    <div className='flex items-center justify-center py-8'>
      <div className='w-full max-w-4xl space-y-4'>
        <Card className='border shadow-none bg-white/80 dark:bg-slate-800/80'>
          <CardHeader>
            <CardTitle className='flex items-center justify-between text-lg'>
              <span>Your Sessions</span>
              <Button
                variant='outline'
                size='sm'
                onClick={() => router.push('/upload')}
              >
                New Document
              </Button>
            </CardTitle>
          </CardHeader>
          <CardContent className='space-y-2'>
            {sessions.map((s) => (
              <div
                key={s.id}
                className='flex items-center justify-between p-2 border rounded cursor-pointer hover:bg-slate-50 dark:hover:bg-slate-700'
                onClick={() => handleSessionSelect(s.id)}
              >
                <div>
                  <p className='font-medium'>{s.name}</p>
                  <p className='text-xs text-muted-foreground'>
                    Last updated&nbsp;
                    {s.updated_at
                      ? new Date(s.updated_at).toLocaleString()
                      : 'n/a'}
                  </p>
                </div>
                <Button
                  variant='outline'
                  size='sm'
                  onClick={(e) => {
                    e.stopPropagation();
                    handleSessionSelect(s.id);
                  }}
                >
                  Open
                </Button>
              </div>
            ))}
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
