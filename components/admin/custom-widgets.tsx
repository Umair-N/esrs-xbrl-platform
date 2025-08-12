'use client';

import { useState } from 'react';
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import {
  RefreshCw,
  TrendingUp,
  Users,
  Shield,
  Clock,
  CheckCircle,
} from 'lucide-react';

export function CustomWidgets() {
  const [lastUpdated, setLastUpdated] = useState(new Date());

  const refreshData = () => {
    setLastUpdated(new Date());
  };

  const pendingApprovals = [
    {
      id: 1,
      name: 'Sarah Connor',
      email: 'sarah.connor@example.com',
      type: 'Access Request',
      time: '2 hours ago',
    },
    {
      id: 2,
      name: 'Mike Johnson',
      email: 'mike.johnson@example.com',
      type: 'Role Change',
      time: '4 hours ago',
    },
    {
      id: 3,
      name: 'Lisa Wang',
      email: 'lisa.wang@example.com',
      type: 'Account Recovery',
      time: '6 hours ago',
    },
  ];

  // const quickStats = [
  //   { label: "Online Users", value: "234", icon: Users, color: "text-green-600" },
  //   { label: "Pending Requests", value: "12", icon: Clock, color: "text-orange-600" },
  //   { label: "Active Sessions", value: "1,234", icon: Shield, color: "text-blue-600" },
  //   { label: "Completed Today", value: "89", icon: CheckCircle, color: "text-purple-600" },
  // ]

  return (
    <div className='space-y-4'>
      {/* <Card className="border-0 shadow-lg">
        <CardHeader className="bg-gradient-to-r from-slate-50 to-slate-100 dark:from-slate-800 dark:to-slate-900">
          <div className="flex items-center justify-between">
            <div>
              <CardTitle className="flex items-center gap-2">
                <TrendingUp className="h-5 w-5 text-primary" />
                Quick Stats
              </CardTitle>
              <CardDescription>Last updated: {lastUpdated.toLocaleTimeString()}</CardDescription>
            </div>
            <Button variant="outline" size="sm" onClick={refreshData} className="hover:bg-muted/50 bg-transparent">
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
                  <p className="text-sm font-medium text-muted-foreground">{stat.label}</p>
                  <p className={`text-lg font-bold ${stat.color}`}>{stat.value}</p>
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card> */}

      <Card className='border-0 shadow-lg'>
        <CardHeader className='bg-gradient-to-r from-slate-50 to-slate-100 dark:from-slate-800 dark:to-slate-900'>
          <CardTitle className='flex items-center gap-2'>
            <Clock className='h-5 w-5 text-primary' />
            Pending Approvals
          </CardTitle>
          <CardDescription>Items requiring your attention</CardDescription>
        </CardHeader>
        <CardContent className='p-0'>
          <div className='divide-y divide-border'>
            {pendingApprovals.map((item) => (
              <div
                key={item.id}
                className='p-4 hover:bg-muted/30 transition-colors'
              >
                <div className='flex items-center justify-between'>
                  <div className='space-y-1'>
                    <p className='font-medium'>{item.name}</p>
                    <p className='text-sm text-muted-foreground'>
                      {item.email}
                    </p>
                  </div>
                  <div className='text-right space-y-1'>
                    <Badge className='bg-orange-100 text-orange-800 border-orange-200'>
                      {item.type}
                    </Badge>
                    <p className='text-xs text-muted-foreground'>{item.time}</p>
                  </div>
                </div>
                <div className='flex gap-2 mt-3'>
                  <Button size='sm' className='bg-green-600 hover:bg-green-700'>
                    Approve
                  </Button>
                  <Button size='sm' variant='outline'>
                    Review
                  </Button>
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
