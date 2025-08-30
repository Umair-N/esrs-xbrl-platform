'use client';

import { useState } from 'react';
import {
  MoreHorizontal,
  UserCheck,
  UserX,
  Eye,
  Shield,
  ShieldOff,
  Calendar,
  Search,
  Users,
  Tags,
} from 'lucide-react';
import { Button } from '@/components/ui/button';
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from '@/components/ui/card';
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu';
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table';
import { Badge } from '@/components/ui/badge';
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar';
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
  DialogFooter,
} from '@/components/ui/dialog';
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
} from '@/components/ui/alert-dialog';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from '@/components/ui/popover';
import { usePagination } from '@/hooks/use-paginated';
import { useUsers } from '@/features/users/get-users';
import { getInitials } from '@/lib/utils';
import { User } from '@/types/api';
import { Pagination } from '../pagination';
import { DialogClose } from '@radix-ui/react-dialog';
import {
  Form,
  FormControl,
  FormDescription,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from '../ui/form';
import { MultiSelect } from '../ui/multi-select';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import z from 'zod';
import { useAllTaxonomies } from '@/features/taxonomy/api/get-all-taxonomy-list';
import { TaxonomyList } from '@/types/taxonomy';
import { useSetActiveUserTaxonomy } from '@/features/taxonomy/api/assign-taxonomies';
import { toast } from 'sonner';

// const mockUsers: User[] = [
//   {
//     id: '1',
//     name: 'John Doe',
//     email: 'john.doe@example.com',
//     role: 'Admin',
//     status: 'active',
//     lastLogin: '2 hours ago',
//     joinDate: '2024-01-15',
//     hasSystemAccess: true,
//   },
//   {
//     id: '2',
//     name: 'Jane Smith',
//     email: 'jane.smith@example.com',
//     role: 'User',
//     status: 'active',
//     lastLogin: '1 day ago',
//     joinDate: '2024-01-20',
//     hasSystemAccess: true,
//   },
//   {
//     id: '3',
//     name: 'Bob Johnson',
//     email: 'bob.johnson@example.com',
//     role: 'User',
//     status: 'inactive',
//     lastLogin: '1 week ago',
//     joinDate: '2024-01-10',
//     hasSystemAccess: false,
//   },
//   {
//     id: '4',
//     name: 'Alice Brown',
//     email: 'alice.brown@example.com',
//     role: 'Moderator',
//     status: 'disabled',
//     lastLogin: '2 weeks ago',
//     joinDate: '2024-01-05',
//     hasSystemAccess: false,
//   },
//   {
//     id: '5',
//     name: 'Charlie Wilson',
//     email: 'charlie.wilson@example.com',
//     role: 'User',
//     status: 'pending',
//     lastLogin: 'Never',
//     joinDate: '2024-01-25',
//     hasSystemAccess: false,
//   },
// ];

export function UserManagement() {
  const [selectedUser, setSelectedUser] = useState<User | null>(null);
  const [actionUser, setActionUser] = useState<User | null>(null);
  const [actionType, setActionType] = useState<
    'disable' | 'enable' | 'grant' | 'revoke' | null
  >(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [statusFilter, setStatusFilter] = useState('all');
  const [dateFilter, setDateFilter] = useState('all');
  const [taxonomyModalOpen, setTaxonomyModalOpen] = useState<boolean>(false);

  const pagination = usePagination({ initialPage: 1, initialLimit: 10 });
  const { data, error, isLoading } = useUsers({
    params: {
      page: pagination.currentPage,
      limit: pagination.limit,
      sort_by: 'created_at',
      sort_order: 'desc',
    },
  });
  const users = data?.users;

  const updateUserStatus = (userId: string, newStatus: User['status']) => {
    // setUsers(
    //   users?.map((user) =>
    //     user.id === userId ? { ...user, status: newStatus } : user
    //   )
    // );
  };

  const updateUserAccess = (userId: string, hasAccess: boolean) => {
    // setUsers(
    //   users?.map((user) =>
    //     user.id === userId ? { ...user, hasSystemAccess: hasAccess } : user
    //   )
    // );
  };

  const handleAction = () => {
    if (!actionUser || !actionType) return;

    switch (actionType) {
      case 'disable':
        updateUserStatus(actionUser.id, 'disabled');
        break;
      case 'enable':
        updateUserStatus(actionUser.id, 'active');
        break;
      case 'grant':
        updateUserAccess(actionUser.id, true);
        break;
      case 'revoke':
        updateUserAccess(actionUser.id, false);
        break;
    }

    setActionUser(null);
    setActionType(null);
  };

  // const filteredUsers = users.filter((user) => {
  //   const matchesSearch =
  //     user.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
  //     user.email.toLowerCase().includes(searchTerm.toLowerCase());
  //   const matchesStatus =
  //     statusFilter === 'all' || user.status === statusFilter;

  //   let matchesDate = true;
  //   if (dateFilter !== 'all') {
  //     const joinDate = new Date(user.joinDate);
  //     const now = new Date();
  //     const daysDiff = Math.floor(
  //       (now.getTime() - joinDate.getTime()) / (1000 * 60 * 60 * 24)
  //     );

  //     switch (dateFilter) {
  //       case 'week':
  //         matchesDate = daysDiff <= 7;
  //         break;
  //       case 'month':
  //         matchesDate = daysDiff <= 30;
  //         break;
  //       case 'quarter':
  //         matchesDate = daysDiff <= 90;
  //         break;
  //     }
  //   }

  //   return matchesSearch && matchesStatus && matchesDate;
  // });

  const getStatusBadge = (status: User['status'] | undefined) => {
    switch (status) {
      case 'active':
        return (
          <Badge className='bg-green-100 text-green-800 border-green-200'>
            Active
          </Badge>
        );
      case 'inactive':
        return (
          <Badge className='bg-yellow-100 text-yellow-800 border-yellow-200'>
            Inactive
          </Badge>
        );
      case 'disabled':
        return (
          <Badge className='bg-red-100 text-red-800 border-red-200'>
            Disabled
          </Badge>
        );
      case 'pending':
        return (
          <Badge className='bg-blue-100 text-blue-800 border-blue-200'>
            Pending
          </Badge>
        );
    }
  };

  const getRoleIcon = (role: string) => {
    switch (role) {
      case 'admin':
        return <Shield className='h-4 w-4 text-red-600' />;
      case 'Moderator':
        return <ShieldOff className='h-4 w-4 text-orange-600' />;
      default:
        return <UserCheck className='h-4 w-4 text-blue-600' />;
    }
  };
  const handlePageChange = (page: number) => {
    pagination.setPage(page);
  };

  const handleItemsPerPageChange = (itemsPerPage: number) => {
    pagination.setLimit(itemsPerPage);
    pagination.goToFirstPage();
  };
  const handleSetTaxonomy = (e: Event, user: User) => {
    e.preventDefault();
    setActionUser(user);
    setTaxonomyModalOpen(true); // Assuming you have this function
  };
  return (
    <div className='space-y-6'>
      <Card className='border-0 shadow-lg'>
        <CardHeader className='bg-gradient-to-r from-slate-50 to-slate-100 dark:from-slate-800 dark:to-slate-900'>
          <CardTitle className='flex items-center gap-2'>
            <Users className='h-5 w-5 text-primary' />
            User Management
          </CardTitle>
          <CardDescription>
            Manage user accounts, permissions, and access controls
          </CardDescription>
        </CardHeader>
        <CardContent className='p-6'>
          {/* Filters */}
          <div className='flex flex-col sm:flex-row gap-4 mb-6'>
            <div className='relative flex-1'>
              <Search className='absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-muted-foreground' />
              <Input
                placeholder='Search users...'
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className='pl-10'
              />
            </div>
            <Select value={statusFilter} onValueChange={setStatusFilter}>
              <SelectTrigger className='w-full sm:w-[180px]'>
                <SelectValue placeholder='Filter by status' />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value='all'>All Status</SelectItem>
                <SelectItem value='active'>Active</SelectItem>
                <SelectItem value='inactive'>Inactive</SelectItem>
                <SelectItem value='disabled'>Disabled</SelectItem>
                <SelectItem value='pending'>Pending</SelectItem>
              </SelectContent>
            </Select>
            <Popover>
              <PopoverTrigger asChild>
                <Button
                  variant='outline'
                  className='w-full sm:w-[180px] bg-transparent'
                >
                  <Calendar className='mr-2 h-4 w-4' />
                  {dateFilter === 'all'
                    ? 'All Time'
                    : dateFilter === 'week'
                      ? 'Last Week'
                      : dateFilter === 'month'
                        ? 'Last Month'
                        : 'Last Quarter'}
                </Button>
              </PopoverTrigger>
              <PopoverContent className='w-48'>
                <div className='space-y-2'>
                  <Button
                    variant={dateFilter === 'all' ? 'default' : 'ghost'}
                    className='w-full justify-start'
                    onClick={() => setDateFilter('all')}
                  >
                    All Time
                  </Button>
                  <Button
                    variant={dateFilter === 'week' ? 'default' : 'ghost'}
                    className='w-full justify-start'
                    onClick={() => setDateFilter('week')}
                  >
                    Last Week
                  </Button>
                  <Button
                    variant={dateFilter === 'month' ? 'default' : 'ghost'}
                    className='w-full justify-start'
                    onClick={() => setDateFilter('month')}
                  >
                    Last Month
                  </Button>
                  <Button
                    variant={dateFilter === 'quarter' ? 'default' : 'ghost'}
                    className='w-full justify-start'
                    onClick={() => setDateFilter('quarter')}
                  >
                    Last Quarter
                  </Button>
                </div>
              </PopoverContent>
            </Popover>
          </div>

          <div className='rounded-lg border border-border/50 overflow-hidden'>
            <Table>
              <TableHeader className='bg-muted/50'>
                <TableRow>
                  <TableHead>User</TableHead>
                  <TableHead>Role</TableHead>
                  <TableHead>Status</TableHead>
                  <TableHead>System Access</TableHead>
                  <TableHead>Last Login</TableHead>
                  <TableHead className='text-right'>Actions</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {users?.map((user) => (
                  <TableRow
                    key={user.id}
                    className='hover:bg-muted/30 transition-colors'
                  >
                    <TableCell className='font-medium'>
                      <div className='flex items-center gap-3'>
                        <Avatar className='h-10 w-10 ring-2 ring-background shadow-sm'>
                          <AvatarImage
                          // src={user.avatar || '/placeholder.svg'}
                          />
                          <AvatarFallback className='bg-gradient-to-br from-blue-500 to-purple-600 text-white'>
                            {getInitials(user?.full_name || user?.username)}
                          </AvatarFallback>
                        </Avatar>
                        <div>
                          <div className='font-medium'>
                            {user?.full_name || user?.username}
                          </div>
                          <div className='text-sm text-muted-foreground'>
                            {user.email}
                          </div>
                        </div>
                      </div>
                    </TableCell>
                    <TableCell>
                      <div className='flex items-center gap-2'>
                        {getRoleIcon(user.role)}
                        <span className='font-medium capitalize'>
                          {user.role}
                        </span>
                      </div>
                    </TableCell>
                    <TableCell>{getStatusBadge(user?.status)}</TableCell>
                    <TableCell>
                      <Badge
                        className={`${
                          user?.platform_access
                            ? 'bg-green-100 text-green-600'
                            : 'bg-red-100 text-red-600'
                        }`}
                      >
                        {user?.platform_access ? 'Granted' : 'Denied'}
                      </Badge>
                    </TableCell>
                    <TableCell className='text-muted-foreground'>
                      {user?.last_login}
                    </TableCell>
                    <TableCell className='text-right'>
                      <DropdownMenu>
                        <DropdownMenuTrigger asChild>
                          <Button variant='ghost' className='h-8 w-8 p-0'>
                            <span className='sr-only'>Open menu</span>
                            <MoreHorizontal className='h-4 w-4' />
                          </Button>
                        </DropdownMenuTrigger>
                        <DropdownMenuContent align='end'>
                          <DropdownMenuLabel>Actions</DropdownMenuLabel>

                          <Dialog>
                            <DialogTrigger asChild>
                              <DropdownMenuItem
                                onSelect={(e) => {
                                  e.preventDefault();
                                  setSelectedUser(user);
                                }}
                              >
                                <Eye className='mr-2 h-4 w-4' />
                                View Profile
                              </DropdownMenuItem>
                            </DialogTrigger>
                          </Dialog>

                          <DropdownMenuSeparator />

                          {user.status === 'active' ? (
                            <DropdownMenuItem
                              onSelect={(e) => {
                                e.preventDefault();
                                setActionUser(user);
                                setActionType('disable');
                              }}
                            >
                              <UserX className='mr-2 h-4 w-4' />
                              Disable Account
                            </DropdownMenuItem>
                          ) : (
                            <DropdownMenuItem
                              onSelect={(e) => {
                                e.preventDefault();
                                setActionUser(user);
                                setActionType('enable');
                              }}
                            >
                              <UserCheck className='mr-2 h-4 w-4' />
                              Enable Account
                            </DropdownMenuItem>
                          )}

                          <DropdownMenuSeparator />

                          {user?.platform_access ? (
                            <DropdownMenuItem
                              onSelect={(e) => {
                                e.preventDefault();
                                setActionUser(user);
                                setActionType('revoke');
                              }}
                            >
                              <ShieldOff className='mr-2 h-4 w-4' />
                              Revoke Access
                            </DropdownMenuItem>
                          ) : (
                            <DropdownMenuItem
                              onSelect={(e) => {
                                e.preventDefault();
                                setActionUser(user);
                                setActionType('grant');
                              }}
                            >
                              <Shield className='mr-2 h-4 w-4' />
                              Grant Access
                            </DropdownMenuItem>
                          )}

                          <DropdownMenuSeparator />

                          <DropdownMenuItem
                            onSelect={(e) => handleSetTaxonomy(e, user)}
                          >
                            <Tags className='mr-2 h-4 w-4' />
                            Set Taxonomies
                          </DropdownMenuItem>
                        </DropdownMenuContent>
                      </DropdownMenu>

                      <SetTaxonomyModal
                        user={actionUser!}
                        open={taxonomyModalOpen}
                        setOpen={setTaxonomyModalOpen}

                        // taxonomies={taxonomies}
                      />
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </div>
        </CardContent>
        <CardFooter className='pt-0'>
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
      </Card>

      {/* User Profile Dialog */}
      {selectedUser && (
        <Dialog
          open={!!selectedUser}
          onOpenChange={() => setSelectedUser(null)}
        >
          <DialogContent className='sm:max-w-[500px]'>
            <DialogHeader>
              <DialogTitle>User Profile</DialogTitle>
              <DialogDescription>
                View and manage user account details
              </DialogDescription>
            </DialogHeader>
            <div className='grid gap-6 py-4'>
              <div className='flex items-center gap-4'>
                <Avatar className='h-20 w-20 ring-4 ring-background shadow-lg'>
                  <AvatarImage
                  // src={selectedUser.avatar || '/placeholder.svg'}
                  />
                  <AvatarFallback className='text-xl bg-gradient-to-br from-blue-500 to-purple-600 text-white'>
                    {getInitials(
                      selectedUser?.full_name || selectedUser?.username
                    )}
                  </AvatarFallback>
                </Avatar>
                <div className='space-y-1'>
                  <h3 className='text-xl font-semibold'>
                    {selectedUser?.full_name || selectedUser?.username}
                  </h3>
                  <p className='text-muted-foreground'>{selectedUser.email}</p>
                  <div className='flex items-center gap-2'>
                    {getRoleIcon(selectedUser.role)}
                    <span className='text-sm font-medium'>
                      {selectedUser.role}
                    </span>
                  </div>
                </div>
              </div>
              <div className='grid grid-cols-2 gap-4'>
                <div className='space-y-2'>
                  <Label>Status</Label>
                  <div>{getStatusBadge(selectedUser.status)}</div>
                </div>
                <div className='space-y-2'>
                  <Label>System Access</Label>
                  <div>
                    <Badge
                      variant={
                        selectedUser?.platform_access ? 'default' : 'secondary'
                      }
                    >
                      {selectedUser?.platform_access ? 'Granted' : 'Denied'}
                    </Badge>
                  </div>
                </div>
                <div className='space-y-2'>
                  <Label>Join Date</Label>
                  <Input
                    value={new Date(
                      selectedUser?.created_at
                    ).toLocaleDateString()}
                    readOnly
                  />
                </div>
                <div className='space-y-2'>
                  <Label>Last Login</Label>
                  <Input value={selectedUser?.created_at} readOnly />
                </div>
              </div>
            </div>
            <DialogFooter>
              <Button variant='outline' onClick={() => setSelectedUser(null)}>
                Close
              </Button>
            </DialogFooter>
          </DialogContent>
        </Dialog>
      )}

      {/* Confirmation Dialog */}
      <AlertDialog
        open={!!actionUser && !!actionType}
        onOpenChange={() => {
          setActionUser(null);
          setActionType(null);
        }}
      >
        <AlertDialogContent>
          <AlertDialogHeader>
            <AlertDialogTitle>
              {actionType === 'disable' && 'Disable User Account'}
              {actionType === 'enable' && 'Enable User Account'}
              {actionType === 'grant' && 'Grant System Access'}
              {actionType === 'revoke' && 'Revoke System Access'}
            </AlertDialogTitle>
            <AlertDialogDescription>
              {actionType === 'disable' &&
                `Are you sure you want to disable ${actionUser?.full_name || actionUser?.username}'s account? They will no longer be able to access the system.`}
              {actionType === 'enable' &&
                `Are you sure you want to enable ${actionUser?.full_name || actionUser?.username}'s account? They will regain access to the system.`}
              {actionType === 'grant' &&
                `Are you sure you want to grant system access to ${actionUser?.full_name || actionUser?.username}? They will be able to access all system features.`}
              {actionType === 'revoke' &&
                `Are you sure you want to revoke system access for ${actionUser?.full_name || actionUser?.username}? They will lose access to system features.`}
            </AlertDialogDescription>
          </AlertDialogHeader>
          <AlertDialogFooter>
            <AlertDialogCancel>Cancel</AlertDialogCancel>
            <AlertDialogAction onClick={handleAction}>
              {actionType === 'disable' && 'Disable'}
              {actionType === 'enable' && 'Enable'}
              {actionType === 'grant' && 'Grant Access'}
              {actionType === 'revoke' && 'Revoke Access'}
            </AlertDialogAction>
          </AlertDialogFooter>
        </AlertDialogContent>
      </AlertDialog>
    </div>
  );
}

type SetTaxonomyModalProps = {
  user: User;
  open: boolean;
  setOpen: React.Dispatch<React.SetStateAction<boolean>>;
};

export function SetTaxonomyModal({
  user,
  open,
  setOpen,
}: SetTaxonomyModalProps) {
  const { data: taxonomiesList, isLoading } = useAllTaxonomies();
  const { mutate: setActiveUserTaxonomies } = useSetActiveUserTaxonomy({
    mutationConfig: {
      onSuccess: (data, variables) => {
        toast.success('User taxonomies updated successfully.');
      },
      onError: (error, variables) => {
        toast.error('Failed to update user taxonomies. Please try again.');
        console.error('Update user taxonomies error:', error);
      },
    },
  });
  const convertTaxonomiesToOptions = (taxonomies: TaxonomyList[]) => {
    return taxonomies
      .filter((taxonomy) => taxonomy.enabled) // Only show enabled taxonomies
      .map((taxonomy) => ({
        value: taxonomy.id.toString(),
        label: taxonomy.name,
      }));
  };
  const taxonomyFormSchema = z.object({
    taxonomies: z.array(z.string()).min(1, {
      message: 'Please select at least one taxonomy.',
    }),
  });
  const form = useForm({
    resolver: zodResolver(taxonomyFormSchema),
    defaultValues: {
      taxonomies: [],
    },
  });
  type TaxonomyFormValues = z.infer<typeof taxonomyFormSchema>;
  const onSubmit = (data: TaxonomyFormValues): void => {
    // Convert selected IDs back to taxonomy objects for API call
    setActiveUserTaxonomies({
      data: { taxonomy_ids: data.taxonomies },
      userId: Number(user.id),
    });
    // const selectedTaxonomyIds = data.taxonomies.map((id) => parseInt(id));
    // const selectedTaxonomies = convertTaxonomiesToOptions(
    //   taxonomiesList!
    // ).filter((t) => selectedTaxonomyIds.includes(t.id));

    // console.log('Assigning taxonomies:', selectedTaxonomies, 'to user:', user);
    // Add your API call or state update logic here
    // Example API call structure:
    // assignTaxonomiesToUser(user.id, selectedTaxonomyIds);

    // Reset form and close modal
    form.reset();
    setOpen(false);
  };

  const handleOpenChange = (newOpen: boolean): void => {
    if (!newOpen) {
      form.reset();
    }
    setOpen(newOpen);
  };

  return (
    <Dialog open={open} onOpenChange={handleOpenChange}>
      <DialogContent className='sm:max-w-[500px]'>
        <DialogHeader>
          <DialogTitle>Set Taxonomies</DialogTitle>
          <DialogDescription>
            Assign taxonomies to{' '}
            <strong>{user?.full_name || 'selected user'}</strong>. Select
            multiple taxonomies to define their roles and permissions.
          </DialogDescription>
        </DialogHeader>

        <Form {...form}>
          <form onSubmit={form.handleSubmit(onSubmit)} className='space-y-6'>
            <FormField
              control={form.control}
              name='taxonomies'
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Taxonomies</FormLabel>
                  <FormControl>
                    <MultiSelect
                      value={field.value}
                      onValueChange={field.onChange}
                      options={convertTaxonomiesToOptions(taxonomiesList!)}
                      placeholder='Select taxonomies...'
                    />
                  </FormControl>
                  <FormDescription>
                    Choose one or more taxonomies to assign to this user.
                  </FormDescription>
                  <FormMessage />
                </FormItem>
              )}
            />

            <DialogFooter>
              <DialogClose asChild>
                <Button type='button' variant='outline'>
                  Cancel
                </Button>
              </DialogClose>
              <Button type='submit' disabled={form.formState.isSubmitting}>
                {form.formState.isSubmitting
                  ? 'Assigning...'
                  : 'Assign Taxonomies'}
              </Button>
            </DialogFooter>
          </form>
        </Form>
      </DialogContent>
    </Dialog>
  );
}
