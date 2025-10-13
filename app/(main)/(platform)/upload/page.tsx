// 'UploadPage' provides a dedicated screen for uploading a new report.
// After a file is selected and processed, it is merged into a single
// block (for non‑PDF formats) and the user is redirected to the editor
// page with the report ID in the query string. Client‑side storage is
// no longer used to persist session state.

'use client';

import { useRouter } from 'next/navigation';
import { useCallback } from 'react';
import { FileUploader } from '@/components/editor/file-uploader';
import type { ReportDocument } from '@/types/report';
import type { ReportBlock, XbrlTag } from '@/types/report';
// The legacy navigation components for viewing saved sessions have been
// removed. We no longer import Link or button styling utilities here.

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

  // Once a report is uploaded, merge its blocks if necessary and
  // navigate to the editor page with the report ID in the query. The
  // application no longer persists reports in localStorage; instead it
  // relies on server‑side storage and query parameters to fetch
  // document data.
  const handleReportLoaded = useCallback(
    (report: ReportDocument) => {
      const isPdf = report.file_type?.toLowerCase().includes('pdf');
      const merged = isPdf ? report : mergeReportBlocks(report);
      // Redirect to the editor with the reportId query parameter. The
      // editor page will fetch the report from the backend using this ID.
      router.push(`/editor?reportId=${merged.id}`);
    },
    [router]
  );

  return (
    <div className='flex items-center justify-center py-8 '>
      <div className='w-full max-w-3xl'>
        {/* The legacy buttons for viewing saved sessions have been
            removed. With the refactor to server‑persisted canvases, all
            reports are edited via their unique URLs. */}

        <FileUploader onReportLoaded={handleReportLoaded} />
      </div>
    </div>
  );
}
