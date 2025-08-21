import { queryOptions, useQuery } from '@tanstack/react-query';
import { api } from '@/lib/api-client';
import { QueryConfig } from '@/lib/react-query';
import { User, UsersAPIResponse } from '@/types/api';

type QueryParams = {
    page?: number;
    limit?: number;
    sort_by?: string;
    sort_order?: 'asc' | 'desc';
    search?: string | null;
};

export const getUsers = (params?: QueryParams): Promise<UsersAPIResponse> => {
    return api.get(`/users`, { params: params });
};

export const getUsersQueryOptions = (params?: QueryParams) => {
    return queryOptions({
        queryKey: ['users', params],
        queryFn: () => getUsers(params),
        refetchOnMount: false,
    });
};

type UseUsersOptions = {
    queryConfig?: QueryConfig<typeof getUsersQueryOptions>;
    params?: QueryParams;
};

export const useUsers = ({ queryConfig, params }: UseUsersOptions = {}) => {
    return useQuery({
        ...getUsersQueryOptions(params),
        ...queryConfig,
    });
};
