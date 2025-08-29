'use client';

import {
  Users,
  UserCheck,
  Activity,
  TrendingUp,
  Shield,
  TrendingDownIcon,
  RefreshCw,
  Clock,
  CheckCircle,
} from 'lucide-react';
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from '@/components/ui/card';
import { useUserStats } from '@/features/stats/get-stats';
import { Button } from '../ui/button';
import { Skeleton } from '../ui/skeleton';

type StatsOptions = {
  title: string;
  value: number | undefined;
  change: string | undefined;
  changeType?: 'positive' | 'negative';
  changeSince?: string;
  icon: any;
  description: string;
  gradient: string;
};
export function OverviewCards() {
  const { data, isLoading } = useUserStats();

  const stats: StatsOptions[] = [
    {
      title: 'Total Users',
      value: data?.total,
      change: data?.change_percentage + '%',
      changeType:
        data?.change_percentage && data?.change_percentage > 0
          ? 'positive'
          : 'negative',
      icon: Users,
      description: 'Total users in the system',
      gradient: 'from-blue-500 to-blue-600',
    },
    {
      title: 'Active Sessions',
      value: 1234,
      change: '+8.2%',
      changeType: 'positive' as const,
      icon: UserCheck,
      description: 'Currently logged in users',
      gradient: 'from-green-500 to-green-600',
    },
    {
      title: 'Pending Access',
      value: data?.platform_access_false,
      change: data?.platform_access_true.toString(),
      // changeType: '',
      icon: Shield,
      changeSince: 'Platform access granted',
      description: 'Users have pending access',
      gradient: 'from-orange-500 to-orange-600',
    },
    {
      title: 'Daily Activity',
      value: data?.last_accessed_today,
      change: data?.access_change_percentage + '%',
      changeType:
        data?.access_change_percentage && data?.access_change_percentage > 0
          ? 'positive'
          : 'negative',
      changeSince: 'from last 24h',
      icon: Activity,
      description: 'User actions in the last 24h',
      gradient: 'from-purple-500 to-purple-600',
    },
  ];

  // const quickStats = [
  //   {
  //     label: 'Online Users',
  //     value: '234',
  //     icon: Users,
  //     color: 'text-green-600',
  //   },
  //   {
  //     label: 'Pending Requests',
  //     value: '12',
  //     icon: Clock,
  //     color: 'text-orange-600',
  //   },
  //   {
  //     label: 'Active Sessions',
  //     value: '1,234',
  //     icon: Shield,
  //     color: 'text-blue-600',
  //   },
  //   {
  //     label: 'Completed Today',
  //     value: '89',
  //     icon: CheckCircle,
  //     color: 'text-purple-600',
  //   },
  // ];

  if (isLoading) {
    return (
      <div className='grid gap-6 md:grid-cols-2 lg:grid-cols-4'>
        {Array.from({ length: 4 }).map((_, index) => (
          <Skeleton key={index} className='h-40' />
        ))}
      </div>
    );
  }
  return (
    <div className='grid gap-6 md:grid-cols-2 lg:grid-cols-4'>
      {stats.map((stat) => (
        <Card
          key={stat.title}
          className='relative overflow-hidden border-0 shadow-lg'
        >
          <div
            className={`absolute inset-0 bg-gradient-to-br ${stat.gradient} opacity-5`}
          />
          <CardHeader className='flex flex-row items-center justify-between space-y-0 pb-2'>
            <CardTitle className='text-sm font-medium text-muted-foreground'>
              {stat.title}
            </CardTitle>
            <div
              className={`p-2 rounded-lg bg-gradient-to-br ${stat.gradient}`}
            >
              <stat.icon className='h-4 w-4 text-white' />
            </div>
          </CardHeader>
          <CardContent>
            <div className='text-3xl font-bold text-foreground'>
              {stat.value}
            </div>
            <div className='flex items-center gap-2 mt-2'>
              <div className='flex items-center gap-1'>
                {stat.changeType &&
                  (stat.changeType === 'positive' ? (
                    <TrendingUp className='h-3 w-3 text-green-600' />
                  ) : (
                    <TrendingDownIcon className='h-3 w-3 text-red-600' />
                  ))}

                <span
                  className={`text-sm font-medium ${stat.changeType && (stat.changeType === 'positive' ? 'text-green-600' : 'text-red-600')}`}
                >
                  {stat.change}
                </span>
              </div>
              <span className='text-xs text-muted-foreground'>
                {stat?.changeSince || ' from last month'}
              </span>
            </div>
            <p className='text-xs text-muted-foreground mt-1'>
              {stat.description}
            </p>
          </CardContent>
        </Card>
      ))}
      {/* <Card className="border-0 shadow-lg">
        <CardHeader className="bg-gradient-to-r from-slate-50 to-slate-100 dark:from-slate-800 dark:to-slate-900">
          <div className="flex items-center justify-between">
            <div>
              <CardTitle className="flex items-center gap-2">
                <TrendingUp className="h-5 w-5 text-primary" />
                Quick Stats
              </CardTitle>
              <CardDescription>Last updated: {}</CardDescription>
            </div>
            <Button
              variant="outline"
              size="sm"
              className="hover:bg-muted/50 bg-transparent"
            >
              <RefreshCw className="h-4 w-4" />
            </Button>
          </div>
        </CardHeader>
        <CardContent className="p-6">
          <div className="grid grid-cols-2 gap-4">
            {quickStats.map((stat) => (
              <div
                key={stat.label}
                className="flex items-center gap-3 p-3 rounded-lg bg-muted/30 hover:bg-muted/50 transition-colors"
              >
                <div className="p-2 rounded-lg bg-background shadow-sm">
                  <stat.icon className={`h-4 w-4 ${stat.color}`} />
                </div>
                <div>
                  <p className="text-sm font-medium text-muted-foreground">
                    {stat.label}
                  </p>
                  <p className={`text-lg font-bold ${stat.color}`}>
                    {stat.value}
                  </p>
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card> */}
    </div>
  );
}
