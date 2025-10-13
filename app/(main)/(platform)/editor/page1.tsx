"use client";

// This legacy editor page wrapper has been deprecated. When users
// navigate to /editor/page1 (which may have been bookmarked under
// previous versions), immediately redirect to the current editor
// implementation located at /editor. This ensures stale routes still
// resolve correctly after the refactor.
import { redirect } from 'next/navigation';

export default function DeprecatedEditorPageWrapper() {
  redirect('/editor');
  return null;
}
