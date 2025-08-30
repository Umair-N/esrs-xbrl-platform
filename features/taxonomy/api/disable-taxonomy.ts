import { useMutation, useQueryClient } from '@tanstack/react-query';
import { api } from '@/lib/api-client';
import { MutationConfig } from '@/lib/react-query';

export const disableTaxonomy = ({ taxonomyId }: { taxonomyId: number }) => {
  return api.post(`/taxonomy/admin/taxonomies/${taxonomyId}/disable`);
};

type UseDisableTaxonomyOptions = {
  mutationConfig?: MutationConfig<typeof disableTaxonomy>;
};

export const useDisableTaxonomy = ({
  mutationConfig,
}: UseDisableTaxonomyOptions) => {
  const queryClient = useQueryClient();

  const { onSuccess, ...restConfig } = mutationConfig || {};

  return useMutation({
    onSuccess: (...args) => {
      queryClient.invalidateQueries({
        queryKey: ['all', 'taxonomies'],
      });

      onSuccess?.(...args);
    },
    onSettled: () => {
      queryClient.invalidateQueries({
        queryKey: ['all', 'taxonomies'],
      });
    },
    ...restConfig,
    mutationFn: disableTaxonomy,
  });
};
