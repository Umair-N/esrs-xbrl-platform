"use client";

import dynamic from "next/dynamic";
import { Suspense } from "react";

const LazyEditorPage = dynamic(
  () => import("@/components/editor/editor-page"),
  {
    ssr: false,
  }
);

export default function EditorPageWrapper() {
  return (
    <Suspense fallback={<div>Loading editor...</div>}>
      <LazyEditorPage />
    </Suspense>
  );
}
