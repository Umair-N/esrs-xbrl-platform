// contexts/api/revoke-access.ts
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { api } from '@/lib/api-client';
import type { MutationConfig } from '@/lib/react-query';
import { toast } from 'sonner';

export interface RevokeAccessPayload {
  user_id: number;
}

export const revokeAccess = ({ user_id }: RevokeAccessPayload) => {
  return api.put(`/users/${user_id}/revoke-access`);
};

type UseRevokeAccessOptions = {
  mutationConfig?: MutationConfig<typeof revokeAccess>;
};

export const useRevokeAccess = ({
  mutationConfig,
}: UseRevokeAccessOptions = {}) => {
  const queryClient = useQueryClient();
  const { onSuccess, ...rest } = mutationConfig || {};

  return useMutation({
    mutationFn: revokeAccess,
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
