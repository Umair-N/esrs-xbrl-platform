import { queryOptions, useQuery } from '@tanstack/react-query';

import { api } from '@/lib/api-client';
import { QueryConfig } from '@/lib/react-query';
import { UserStats } from '@/types/api';

export const getUserStats = (): Promise<UserStats> => {
    return api.get(`/stats/users`);
};

export const getUserStatsQueryOptions = () => {
    return queryOptions({
        queryKey: ['stats', 'users'],
        queryFn: getUserStats,
    });
};

type UseUserStatsOptions = {
    queryConfig?: QueryConfig<typeof getUserStatsQueryOptions>;
};

export const useUserStats = ({ queryConfig }: UseUserStatsOptions = {}) => {
    return useQuery({
        ...getUserStatsQueryOptions(),
        ...queryConfig,
    });
};