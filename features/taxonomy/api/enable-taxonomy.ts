import { useMutation, useQueryClient } from '@tanstack/react-query';
import { api } from '@/lib/api-client';
import { MutationConfig } from '@/lib/react-query';

// Enable taxonomy mutation
export const enableTaxonomy = ({ taxonomyId }: { taxonomyId: number }) => {
  return api.post(`/taxonomy/admin/taxonomies/${taxonomyId}/enable`);
};

type UseEnableTaxonomyOptions = {
  mutationConfig?: MutationConfig<typeof enableTaxonomy>;
};

export const useEnableTaxonomy = ({
  mutationConfig,
}: UseEnableTaxonomyOptions) => {
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
    mutationFn: enableTaxonomy,
  });
};
