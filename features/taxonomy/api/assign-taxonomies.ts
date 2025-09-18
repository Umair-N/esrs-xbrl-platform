import { useMutation, useQueryClient } from '@tanstack/react-query';

import { api } from '@/lib/api-client';
import { MutationConfig } from '@/lib/react-query';

// Set active user taxonomy mutation
export const setActiveUserTaxonomy = ({
  userId,

  data,
}: {
  userId: number;
  data: { taxonomy_ids: string[] };
}) => {
  return api.patch(`/taxonomy/admin/users/${userId}/set-active`, data);
};

type UseSetActiveUserTaxonomyOptions = {
  mutationConfig?: MutationConfig<typeof setActiveUserTaxonomy>;
};

export const useSetActiveUserTaxonomy = ({
  mutationConfig,
}: UseSetActiveUserTaxonomyOptions) => {
  const queryClient = useQueryClient();

  const { onSuccess, ...restConfig } = mutationConfig || {};

  return useMutation({
    onSuccess: async (...args) => {
      // Invalidate user-related queries
      queryClient.invalidateQueries({
        queryKey: ['taxonomy-data', 'users'],
      });
      queryClient.invalidateQueries({
        queryKey: ['taxonomy-data', 'admin', 'users'],
      });
      // Refetch user data
      await queryClient.refetchQueries({
        queryKey: ['taxonomy-data', 'users'],
      });
      await queryClient.refetchQueries({
        queryKey: ['taxonomy-data', 'admin', 'users'],
      });
      onSuccess?.(...args);
    },
    onSettled: () => {
      queryClient.invalidateQueries({
        queryKey: ['taxonomy-data', 'users'],
      });
      queryClient.invalidateQueries({
        queryKey: ['taxonomy-data', 'admin', 'users'],
      });
    },
    ...restConfig,
    mutationFn: setActiveUserTaxonomy,
  });
};
