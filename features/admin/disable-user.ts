// contexts/api/disable-user.ts
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { api } from '@/lib/api-client';
import type { MutationConfig } from '@/lib/react-query';
import { toast } from 'sonner';

export interface DisableUserPayload {
  user_id: number;
}

export const disableUser = ({ user_id }: DisableUserPayload) =>
  api.put(`/users/${user_id}/disable`);

type UseDisableUserOptions = {
  mutationConfig?: MutationConfig<typeof disableUser>;
};

export const useDisableUser = ({
  mutationConfig,
}: UseDisableUserOptions = {}) => {
  const queryClient = useQueryClient();
  const { onSuccess, ...rest } = mutationConfig || {};

  return useMutation({
    mutationFn: disableUser,
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
