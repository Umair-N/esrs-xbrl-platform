import { PlatformAccess } from '@//utils/platform-access';

export default function EditorLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return <PlatformAccess showError>{children}</PlatformAccess>;
}
