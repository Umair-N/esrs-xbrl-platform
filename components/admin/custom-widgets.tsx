'use client';

import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Clock } from 'lucide-react';

import { useUsers } from '@/features/users/get-users';
import { useGrantAccess } from '@/features/users/api/grant-acess';
import { useState } from 'react';
import { showSuccess } from '@/components/heads-up';
import { User } from '@/types/api';
import { useQueryClient } from '@tanstack/react-query';
import { usePagination } from '@/hooks/use-paginated';
import { Pagination } from '@/components/pagination';
import { Skeleton } from '@/components/ui/skeleton';
import { format } from 'date-fns';
import { Separator } from '@/components/ui/separator';

export function CustomWidgets() {
  const queryClient = useQueryClient();
  const pagination = usePagination({ initialPage: 1, initialLimit: 5 });

  const { data, error, isLoading } = useUsers({
    params: {
      skip: pagination.currentPage,
      limit: pagination.limit,
      sort_by: 'platform_access',
      sort_order: 'asc',
    },
  });
  const users = data?.users;
  const [activeUser, setActiveUser] = useState<User>();

  const { mutate, isPending } = useGrantAccess({
    mutationConfig: {
      onSuccess: () => {
        showSuccess({
          title: `Access granted !`,
          message: `Platform access granted to ${activeUser?.full_name}`,
        });
      },
      onSettled: () => {
        setActiveUser(undefined);
        queryClient.invalidateQueries({ queryKey: ['users'] });
      },
    },
  });

  const handleGrantAccess = (user: User) => {
    setActiveUser(user);
    if (user?.id) {
      mutate(user?.id);
    }
  };
  const handlePageChange = (page: number) => {
    pagination.setPage(page);
  };

  const handleItemsPerPageChange = (itemsPerPage: number) => {
    pagination.setLimit(itemsPerPage);
    pagination.goToFirstPage();
  };

  if (error) {
    return (
      <div className="container mx-auto py-8">
        <Card>
          <CardContent className="pt-6">
            <p className="text-destructive">
              Error loading users: {error.message}
            </p>
          </CardContent>
        </Card>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      <Card className="border-0 shadow-lg">
        <CardHeader className="bg-gradient-to-r from-slate-50 to-slate-100 dark:from-slate-800 dark:to-slate-900">
          <CardTitle className="flex items-center gap-2">
            <Clock className="h-5 w-5 text-primary" />
            Pending Approvals
          </CardTitle>
          <CardDescription>Items requiring your attention</CardDescription>
        </CardHeader>
        <CardContent className="p-0">
          {isLoading ? (
            <div className="space-y-4 p-4">
              {Array.from({ length: pagination.limit }).map((_, i) => (
                <div key={i} className="flex items-center space-x-4">
                  <Skeleton className="h-12 w-12 rounded-full" />
                  <div className="space-y-2">
                    <Skeleton className="h-4 w-[200px]" />
                    <Skeleton className="h-4 w-[160px]" />
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div className="divide-y divide-border">
              {users?.map((user) => {
                const isUserPending = activeUser?.id === user?.id && isPending;
                return (
                  <div
                    key={user?.id}
                    className="p-4 hover:bg-muted/30 transition-colors flex items-center justify-between"
                  >
                    <div className="space-y-1">
                      <p className="font-medium">
                        {user?.full_name || user?.username}
                      </p>
                      <p className="text-sm text-muted-foreground">
                        {user?.email}
                      </p>
                    </div>
                    <div className="flex items-center gap-3">
                      <div className="text-right space-y-1">
                        <Badge className="bg-orange-100 text-orange-800 border-orange-200">
                          Access Request
                        </Badge>
                        <p className="text-xs text-muted-foreground">
                          {format(new Date(user?.created_at), 'PPP h:mm a')}
                        </p>
                      </div>
                      <Button
                        size="sm"
                        className="bg-green-600 hover:bg-green-700"
                        onClick={() => handleGrantAccess(user)}
                        disabled={isUserPending || user?.platform_access}
                      >
                        {isUserPending
                          ? 'Approving...'
                          : user?.platform_access
                            ? 'Approved'
                            : 'Approve'}
                      </Button>
                    </div>
                    {/* <div className="flex gap-2 mt-3">
                      <Button size="sm" variant="outline">
                    Review
                  </Button>
                    </div> */}
                  </div>
                );
              })}
            </div>
          )}
          <Separator />
          <CardFooter className="p-4">
            <Pagination
              currentPage={data?.page}
              totalPages={data?.pages}
              totalItems={data?.total}
              itemsPerPage={data?.limit}
              onPageChange={handlePageChange}
              onItemsPerPageChange={handleItemsPerPageChange}
              showInfo={false}
              className="ml-auto"
            />
          </CardFooter>
        </CardContent>
      </Card>
    </div>
  );
}
