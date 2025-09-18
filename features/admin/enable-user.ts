// contexts/api/enable-user.ts
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { api } from '@/lib/api-client';
import type { MutationConfig } from '@/lib/react-query';
import { toast } from 'sonner';

export interface EnableUserPayload {
  user_id: number;
}

export const enableUser = ({ user_id }: EnableUserPayload) =>
  api.put(`/users/${user_id}/enable`);

type UseEnableUserOptions = {
  mutationConfig?: MutationConfig<typeof enableUser>;
};

export const useEnableUser = ({
  mutationConfig,
}: UseEnableUserOptions = {}) => {
  const queryClient = useQueryClient();
  const { onSuccess, ...rest } = mutationConfig || {};

  return useMutation({
    mutationFn: enableUser,
    onSuccess: (...args) => {
      // Optional: invalidate any relevant cache or refetch queries
      // queryClient.invalidateQueries({ queryKey: ['users'] });
      toast.success('Access revoked successfully.');
      queryClient.invalidateQueries({ queryKey: ['users'] });
      onSuccess?.(...args);
    },
    ...rest,
  });
};
