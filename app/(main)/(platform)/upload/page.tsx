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
import Link from 'next/link';
import { buttonVariants } from '@/components/ui/button';

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
  const handleReportLoaded = useCallback(
    (report: ReportDocument) => {
      // When uploading a PDF, keep its pages as separate blocks to
      // preserve character indices. For other formats or pasted text,
      // merge all blocks into one combined block for ease of editing.
      const isPdf = report.file_type?.toLowerCase().includes('pdf');
      const merged = isPdf ? report : mergeReportBlocks(report);
      if (typeof window !== 'undefined') {
        localStorage.setItem('xbrl-editor-session', JSON.stringify(merged));
        // clear any existing session ID since this is a brand new upload
        localStorage.removeItem('xbrl-session-id');
      }
      router.push('/editor');
    },
    [router]
  );

  return (
    <div className='flex items-center justify-center py-8 '>
      <div className='w-full max-w-3xl'>
        <div className='flex justify-center items-center gap-6'>
          {/* Button for viewing files */}
          <Link
            className={`${buttonVariants()} bg-gradient-to-r from-blue-700 to-indigo-800 hover:from-blue-800 hover:to-indigo-900 py-2 px-6 rounded-lg shadow-xl font-bold text-white border-0 transition duration-300 ease-in-out transform hover:scale-105`}
            href='/sessions'
          >
            View My Files
          </Link>

          {/* Link for continuing previous session */}
          <Link
            href='/editor'
            className='flex items-center text-violet-600 hover:bg-violet-100 hover:text-violet-800 px-4 py-2 rounded-lg text-lg font-semibold transition duration-300 ease-in-out hover:shadow-md'
          >
            <svg
              xmlns='http://www.w3.org/2000/svg'
              className='h-5 w-5 mr-2'
              fill='none'
              stroke='currentColor'
              viewBox='0 0 24 24'
              strokeWidth='2'
            >
              <path
                strokeLinecap='round'
                strokeLinejoin='round'
                d='M9 5l7 7-7 7'
              ></path>
            </svg>
            Continue Previous Session
          </Link>
        </div>

        <FileUploader onReportLoaded={handleReportLoaded} />
      </div>
    </div>
  );
}
