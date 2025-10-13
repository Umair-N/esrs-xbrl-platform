"use client";

// This legacy editor component has been deprecated. Previously it handled
// loading and saving editor sessions via localStorage and a dedicated
// sessions API. That functionality has been removed in favour of a
// Figma‑style canvas storage system backed by the backend under
// ``/reports/canvas``. To ensure any stale imports of this component
// still lead users to the correct editor, the component simply
// redirects to the new editor route at runtime.

import { redirect } from 'next/navigation';

export default function EditorPageLegacy() {
  // Redirect to the new editor page. This call executes immediately
  // on render and prevents the legacy component from mounting.
  redirect('/editor');
  return null;
}