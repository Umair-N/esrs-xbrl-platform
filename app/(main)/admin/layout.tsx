import { AdminAccess } from '@/utils/admin-access';

export default function EditorLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return <AdminAccess showError>{children}</AdminAccess>;
}
