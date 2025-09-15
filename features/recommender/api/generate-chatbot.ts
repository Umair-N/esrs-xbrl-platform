import { useMutation, useQueryClient } from '@tanstack/react-query';
import { z } from 'zod';

import { api } from '@/lib/api-client';
import { MutationConfig } from '@/lib/react-query';
import { GenerateChatBot, User } from '@/types/api';
// import { Comment } from '@/types/api';


export const generateChatbotSchema = z.object({
    prompt: z.string().min(1, 'Required'),
    session_id: z.string().min(1, 'Required'),
});

// export type CreateCommentInput = z.infer<typeof createCommentInputSchema>;

export const generateChatBot = (body: z.infer<typeof generateChatbotSchema>): Promise<GenerateChatBot> => {
    return api.post(`/chatbot/generate`, body, { serviceType: 'aiRecommender' });
};

type UseGenerateChatbot = {
    userId?: string;
    mutationConfig?: MutationConfig<typeof generateChatBot>;
};

export const useGenerateChatbot = ({
    mutationConfig,
}: UseGenerateChatbot = {}) => {
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
        mutationFn: generateChatBot,
    });
};