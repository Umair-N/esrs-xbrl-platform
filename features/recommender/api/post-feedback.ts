import { useMutation } from '@tanstack/react-query';
import { z } from 'zod';

import { api } from '@/lib/api-client';
import { MutationConfig } from '@/lib/react-query';

/**
 * Schema definition for the feedback API call.
 * The recommender service expects the shape defined here when
 * collecting user feedback on suggested taxonomy tags. Fields
 * mirror the backend contract exactly to ensure type-safety.
 */
export const FeedbackBodySchema = z.object({
    taxonomy: z.string().min(1, 'Required'),
    query: z.string().min(1, 'Required'),
    reference: z.string().min(1, 'Required'),
    tag: z.string().min(1, 'Required'),
    is_correct: z.boolean(),
    is_custom: z.boolean(),
    rank: z.number(),
});

export type FeedbackBody = z.infer<typeof FeedbackBodySchema>;

/**
 * Posts feedback to the AI recommender service. This function
 * wraps the call to the `/feedback` endpoint and attaches the correct
 * service type so the base URL is selected from the client configuration.
 */
export const postFeedback = ({
    data,
}: {
    data: FeedbackBody;
}): Promise<unknown> => {
    return api.post('/feedback', data, { serviceType: 'aiRecommender' });
};

type UsePostFeedbackOptions = {
    mutationConfig?: MutationConfig<typeof postFeedback>;
};

/**
 * Custom hook for submitting feedback about recommendation quality.
 * Consumers can call the returned `mutate` function with an object
 * containing a `data` property that conforms to `FeedbackBody`.
 */
export const usePostFeedback = ({
    mutationConfig,
}: UsePostFeedbackOptions = {}) => {
    const { onSuccess, ...restConfig } = mutationConfig || {};
    return useMutation({
        mutationFn: postFeedback,
        onSuccess: (...args) => {
            onSuccess?.(...args);
        },
        // Simple onError could be extended to surface error toasts etc.
        onError: () => {
            // Optionally handle errors centrally here
        },
        ...restConfig,
    });
};