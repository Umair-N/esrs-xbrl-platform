import { useMutation, useQueryClient } from '@tanstack/react-query';
import { z } from 'zod';

import { api } from '@/lib/api-client';
import { MutationConfig } from '@/lib/react-query';
import { QueryRecommendations } from '@/types/api';
import { showError } from '@/components/heads-up';

export const QueryRecommendationsBodySchema = z.object({
    query: z.string().min(1, 'Required'),
    taxonomy: z.string().min(1, 'Required'),
    k: z.number().default(5),
    rerank: z.boolean().default(false),
});

export type QueryRecommendationsBody = z.infer<typeof QueryRecommendationsBodySchema>;

type QueryResult = {
    tag: string;
    datatype: string;
    reference: string;
    score: number;
    rank: number;
};

type QueryDataAPI = {
    query: string;
    taxonomy: string;
    results: QueryResult[];
};

export const getQueryRecommendations = ({
    data,
}: {
    data: QueryRecommendationsBody;
}): Promise<QueryDataAPI> => {
    return api.post('/query', data, { serviceType: 'aiRecommender' });
};

type UseQueryRecommendationsOptions = {
    mutationConfig?: MutationConfig<typeof getQueryRecommendations>;
};

export const useRecommendations = ({
    mutationConfig,
}: UseQueryRecommendationsOptions = {}) => {
    const queryClient = useQueryClient();

    const { onSuccess, ...restConfig } = mutationConfig || {};

    return useMutation({
        onSuccess: (...args) => {
            onSuccess?.(...args);
        },
        onError: (err) => {
            showError({ title: 'Failed to get recommendation', message: '' });
        },
        ...restConfig,
        mutationFn: getQueryRecommendations
    });
};