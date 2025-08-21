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
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar';
import { Clock, UserPlus, UserMinus, Shield, Eye } from 'lucide-react';
import { usePagination } from '@/hooks/use-paginated';
import { useUsers } from '@/features/users/get-users';
import { getInitials } from '@/lib/utils';
import { format } from 'date-fns';
import { Pagination } from '@/components/pagination';
import { Separator } from '@/components/ui/separator';

export function AnalyticsCharts() {
  const pagination = usePagination({ initialPage: 1, initialLimit: 5 });

  const { data, error, isLoading } = useUsers({
    params: {
      page: pagination.currentPage,
      limit: pagination.limit,
      sort_by: 'last_login',
      sort_order: 'desc',
    },
  });
  const users = data?.users;

  const handlePageChange = (page: number) => {
    pagination.setPage(page);
  };

  const handleItemsPerPageChange = (itemsPerPage: number) => {
    pagination.setLimit(itemsPerPage);
    pagination.goToFirstPage();
  };

  const getActionIcon = (type: string) => {
    switch (type) {
      case 'user_created':
        return <UserPlus className='h-4 w-4 text-green-600' />;
      case 'access_granted':
        return <Shield className='h-4 w-4 text-blue-600' />;
      case 'account_disabled':
        return <UserMinus className='h-4 w-4 text-red-600' />;
      case 'profile_viewed':
        return <Eye className='h-4 w-4 text-purple-600' />;
      default:
        return <Clock className='h-4 w-4 text-gray-600' />;
    }
  };

  const getActionBadge = (type: string) => {
    switch (type) {
      case 'user_created':
        return (
          <Badge className='bg-green-100 text-green-800 border-green-200'>
            New User
          </Badge>
        );
      case 'access_granted':
        return (
          <Badge className='bg-blue-100 text-blue-800 border-blue-200'>
            Access
          </Badge>
        );
      case 'account_disabled':
        return (
          <Badge className='bg-red-100 text-red-800 border-red-200'>
            Disabled
          </Badge>
        );
      case 'profile_viewed':
        return (
          <Badge className='bg-purple-100 text-purple-800 border-purple-200'>
            Viewed
          </Badge>
        );
      case 'pending':
        return (
          <Badge className='bg-yellow-100 text-yellow-800 border-yellow-200'>
            Pending
          </Badge>
        );
      default:
        return <Badge variant='secondary'>Activity</Badge>;
    }
  };

  return (
    <Card className='border-0 shadow-lg'>
      <CardHeader className='bg-gradient-to-r from-slate-50 to-slate-100 dark:from-slate-800 dark:to-slate-900'>
        <CardTitle className='flex items-center gap-2'>
          <Clock className='h-5 w-5 text-primary' />
          Recent Activities
        </CardTitle>
        <CardDescription>
          Latest user management activities and system events
        </CardDescription>
      </CardHeader>
      <CardContent className='p-0'>
        <div className='divide-y divide-border'>
          {users?.map((user) => (
            <div
              key={user?.id}
              className='p-4 hover:bg-muted/50 transition-colors'
            >
              <div className='flex items-center gap-4'>
                <Avatar className='size-10 rounded-md'>
                  <AvatarImage
                  // src={`https://api.dicebear.com/7.x/initials/svg?seed=${user?.username}`}
                  />
                  <AvatarFallback className='text-lg rounded-md font-medium bg-gradient-to-br from-blue-500 to-purple-600 text-white'>
                    {getInitials(user?.full_name || user?.username)}
                  </AvatarFallback>
                </Avatar>
                <div className='flex-1 min-w-0'>
                  <div className='flex items-center gap-2 mb-1'>
                    {getActionIcon(user?.status)}
                    <span className='font-medium text-foreground'>
                      {user?.full_name || user?.username}
                    </span>
                    {/* <span className="text-sm text-muted-foreground">•</span> */}
                    {/* <span className="text-sm text-muted-foreground">
                      {user?.action}
                   
                    </span> */}
                  </div>
                  <p className='text-sm text-muted-foreground truncate'>
                    {user?.email}
                  </p>
                </div>
                <div className=' flex flex-col items-end gap-3'>
                  {/* {getActionBadge(user?.status)} */}
                  <span className='text-xs text-muted-foreground whitespace-nowrap'>
                    {format(user?.last_login, 'PPP h:mm a')}
                  </span>
                  <Badge variant='secondary'>Last Login</Badge>
                </div>
              </div>
            </div>
          ))}
        </div>
        <Separator />
        <CardFooter className='p-4'>
          <Pagination
            currentPage={data?.page}
            totalPages={data?.pages}
            totalItems={data?.total}
            itemsPerPage={data?.limit}
            onPageChange={handlePageChange}
            onItemsPerPageChange={handleItemsPerPageChange}
            showInfo={false}
            className='ml-auto'
          />
        </CardFooter>
      </CardContent>
    </Card>
  );
}
