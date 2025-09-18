import { useMutation } from '@tanstack/react-query';

import { api } from '@/lib/api-client';
import { MutationConfig } from '@/lib/react-query';

/**
 * Calls the AI recommender service to delete a feedback entry by ID. The
 * API expects the ID as a query parameter on the `/feedback` endpoint.
 */
export const deleteFeedback = ({ id }: { id: number }): Promise<unknown> => {
    return api.delete('/feedback', {
        serviceType: 'aiRecommender',
        params: { id },
    });
};

type UseDeleteFeedbackOptions = {
    mutationConfig?: MutationConfig<typeof deleteFeedback>;
};

/**
 * Custom hook for deleting feedback from the AI recommender. It exposes a
 * `mutate` function that accepts an object with an `id` property. The
 * feedback entry will be removed when invoked. Consumers can pass
 * additional mutation configuration if needed.
 */
export const useDeleteFeedback = ({
    mutationConfig,
}: UseDeleteFeedbackOptions = {}) => {
    const { onSuccess, ...restConfig } = mutationConfig || {};
    return useMutation({
        mutationFn: deleteFeedback,
        onSuccess: (...args) => {
            onSuccess?.(...args);
        },
        onError: () => {
            // Errors are silently ignored; consumers can override via mutationConfig
        },
        ...restConfig,
    });
};