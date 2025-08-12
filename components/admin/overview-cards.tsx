'use client';

import { Users, UserCheck, Activity, TrendingUp, Shield } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { useUsers } from '@/features/users/get-users';

export function OverviewCards() {
  const { data } = useUsers();

  const stats = [
    {
      title: 'Total Users',
      value: data?.total,
      change: '+12.5%',
      changeType: 'positive' as const,
      icon: Users,
      description: 'Active users in the system',
      gradient: 'from-blue-500 to-blue-600',
    },
    {
      title: 'Active Sessions',
      value: '1,234',
      change: '+8.2%',
      changeType: 'positive' as const,
      icon: UserCheck,
      description: 'Currently logged in users',
      gradient: 'from-green-500 to-green-600',
    },
    {
      title: 'Pending Access',
      value: '23',
      change: '+5.1%',
      changeType: 'positive' as const,
      icon: Shield,
      description: 'Users awaiting approval',
      gradient: 'from-orange-500 to-orange-600',
    },
    {
      title: 'Daily Activity',
      value: '4,567',
      change: '+15.3%',
      changeType: 'positive' as const,
      icon: Activity,
      description: 'User actions in the last 24h',
      gradient: 'from-purple-500 to-purple-600',
    },
  ];

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
                <TrendingUp className='h-3 w-3 text-green-600' />
                <span className='text-sm font-medium text-green-600'>
                  {stat.change}
                </span>
              </div>
              <span className='text-xs text-muted-foreground'>
                from last month
              </span>
            </div>
            <p className='text-xs text-muted-foreground mt-1'>
              {stat.description}
            </p>
          </CardContent>
        </Card>
      ))}
    </div>
  );
}
