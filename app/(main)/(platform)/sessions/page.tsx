// This page has been deprecated. The application previously exposed a
// list of saved editor sessions under the `/sessions` route. In the
// refactored architecture, sessions have been replaced by persistent
// canvases stored on the backend and accessed via `/reports/[id]`.
// To maintain backward compatibility and ensure a smooth user
// experience, navigating to `/sessions` will redirect to the upload
// page where users can begin a new document.

"use client";

import { redirect } from 'next/navigation';

export default function DeprecatedSessionsPage() {
  redirect('/upload');
  return null;
}