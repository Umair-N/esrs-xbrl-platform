// ReportsListPage displays all saved canvases (reports) for the current
// authenticated user. Users can open a report to continue tagging or
// delete it. The list is fetched from the backend via the
// ``/reports/canvas`` endpoint. Pagination can be added later if
// required. This page is accessible at ``/reports`` in the app router.

'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { axiosInstance } from '@/lib/axios';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Skeleton } from '@/components/ui/skeleton';
import { toast } from 'sonner';

interface CanvasListItem {
  id: string;
  name?: string | null;
  report_id?: string | null;
  created_at?: string;
  updated_at?: string;
}

export default function ReportsListPage() {
  const router = useRouter();
  const [items, setItems] = useState<CanvasListItem[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchItems = async () => {
      try {
        const res = await axiosInstance.get('/reports/canvas');
        // Backend returns an array of CanvasResponse objects; extract
        // only the fields needed for display. The ``data`` field
        // contains the serialized report and is not shown here.
        setItems(
          Array.isArray(res.data)
            ? res.data.map((item: any) => ({
                id: item.id,
                name: item.name ?? item.data?.title ?? 'Untitled report',
                report_id: item.report_id,
                created_at: item.created_at,
                updated_at: item.updated_at,
              }))
            : []
        );
      } catch (err) {
        console.error('Failed to load reports', err);
        toast.error('Failed to load reports');
      } finally {
        setLoading(false);
      }
    };
    fetchItems();
  }, []);

  const handleOpen = (id: string) => {
    router.push(`/reports/${id}`);
  };

  const handleDelete = async (id: string) => {
    const confirmed = window.confirm('Are you sure you want to delete this report?');
    if (!confirmed) return;
    try {
      await axiosInstance.delete(`/reports/canvas/${id}`);
      setItems((prev) => prev.filter((it) => it.id !== id));
      toast.success('Report deleted');
    } catch (err) {
      console.error('Failed to delete report', err);
      toast.error('Failed to delete report');
    }
  };

  return (
    <div className='p-4 space-y-4'>
      <Card>
        <CardHeader>
          <CardTitle className='text-xl'>Your Reports</CardTitle>
        </CardHeader>
        <CardContent>
          {loading ? (
            <div className='space-y-2'>
              <Skeleton className='h-8 w-full' />
              <Skeleton className='h-8 w-full' />
              <Skeleton className='h-8 w-full' />
            </div>
          ) : items.length === 0 ? (
            <p className='text-sm text-muted-foreground'>No reports saved yet.</p>
          ) : (
            <table className='w-full text-sm'>
              <thead>
                <tr className='border-b text-left'>
                  <th className='py-2'>Name</th>
                  <th className='py-2'>Updated</th>
                  <th className='py-2'>Actions</th>
                </tr>
              </thead>
              <tbody>
                {items.map((item) => (
                  <tr key={item.id} className='border-b hover:bg-muted/50'>
                    <td className='py-2 pr-4'>{item.name}</td>
                    <td className='py-2 pr-4'>
                      {item.updated_at ? new Date(item.updated_at).toLocaleString() : ''}
                    </td>
                    <td className='py-2 flex gap-2'>
                      <Button size='sm' variant='outline' onClick={() => handleOpen(item.id)}>
                        Open
                      </Button>
                      <Button size='sm' variant='destructive' onClick={() => handleDelete(item.id)}>
                        Delete
                      </Button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </CardContent>
      </Card>
    </div>
  );
}