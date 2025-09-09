import { useMutation, useQueryClient } from '@tanstack/react-query';
import { api } from '@/lib/api-client';
import type { MutationConfig } from '@/lib/react-query';

const deleteContext = ({ id }: { id: number }) => api.delete(`/contexts/${id}`);

type UseDeleteContextOptions = {
  mutationConfig?: MutationConfig<typeof deleteContext>;
};

export const useDeleteContext = ({
  mutationConfig,
}: UseDeleteContextOptions = {}) => {
  const queryClient = useQueryClient();
  const { onSuccess, ...rest } = mutationConfig || {};
  return useMutation({
    mutationFn: deleteContext,
    onSuccess: (...args) => {
      queryClient.invalidateQueries({ queryKey: ['contexts'] });
      onSuccess?.(...args);
    },
    ...rest,
  });
};
