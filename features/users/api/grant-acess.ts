import { useMutation, useQueryClient } from '@tanstack/react-query';
import { z } from 'zod';

import { api } from '@/lib/api-client';
import { MutationConfig } from '@/lib/react-query';
import { User } from '@/types/api';
// import { Comment } from '@/types/api';


// export const createCommentInputSchema = z.object({
//   discussionId: z.string().min(1, 'Required'),
//   body: z.string().min(1, 'Required'),
// });

// export type CreateCommentInput = z.infer<typeof createCommentInputSchema>;

export const grantAccess = (user_id: string): Promise<User> => {
    return api.put(`/users/${user_id}/grant-access`);
};

type UseGrantAccess = {
    userId?: string;
    mutationConfig?: MutationConfig<typeof grantAccess>;
};

export const useGrantAccess = ({
    mutationConfig,
    // userId,
}: UseGrantAccess = {}) => {
    const queryClient = useQueryClient();

    const { onSuccess, ...restConfig } = mutationConfig || {};

    return useMutation({
        onSuccess: (...args) => {
            // queryClient.invalidateQueries({
            //     queryKey: getInfiniteCommentsQueryOptions(discussionId).queryKey,
            // });
            onSuccess?.(...args);
        },
        ...restConfig,
        mutationFn: grantAccess,
    });
};