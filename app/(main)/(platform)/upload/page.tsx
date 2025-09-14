// 'UploadPage' provides a dedicated screen for uploading a new report. Once a
// report is selected and processed, it is merged into a single block and
// persisted into localStorage. The user is then redirected to the editor
// page to begin tagging.

'use client';

import { useRouter } from 'next/navigation';
import { useCallback } from 'react';
import { FileUploader } from '@/components/editor/file-uploader';
import type { ReportDocument } from '@/types/report';
import type { ReportBlock, XbrlTag } from '@/types/report';

/**
 * Merge multiple blocks of a report into a single block. This combines the
 * content of all blocks with double newline separators and adjusts the start
 * and end indices of each tag to account for the offset in the merged content.
 * If the report already contains a single block, it is returned unchanged.
 *
 * @param report The original report document
 * @returns A new report document with a single merged block
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

export default function UploadPage() {
  const router = useRouter();

  // Once a report is uploaded, merge its blocks, persist to localStorage
  // and navigate to the editor page.
  const handleReportLoaded = useCallback((report: ReportDocument) => {
    const merged = mergeReportBlocks(report);
    if (typeof window !== 'undefined') {
      localStorage.setItem('xbrl-editor-session', JSON.stringify(merged));
      // also clear any session id since this is a brand‑new upload
      localStorage.removeItem('xbrl-session-id');
    }
    router.push('/editor');
  }, [router]);

  return (
    <div className='flex items-center justify-center py-8'>
      <div className='w-full max-w-3xl'>
        <FileUploader onReportLoaded={handleReportLoaded} />
      </div>
    </div>
  );
}