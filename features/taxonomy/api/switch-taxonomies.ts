import { useMutation, useQueryClient } from '@tanstack/react-query';
import { z } from 'zod';

import { api } from '@/lib/api-client';
import { MutationConfig } from '@/lib/react-query';

export const switchTaxonomy = ({ taxonomyId }: { taxonomyId: number }) => {
  return api.post(`/taxonomy/my/switch-taxonomy/${taxonomyId}`);
};

type UseSwitchTaxonomyOptions = {
  mutationConfig?: MutationConfig<typeof switchTaxonomy>;
};

export const useSwitchTaxonomy = ({
  mutationConfig,
}: UseSwitchTaxonomyOptions) => {
  const queryClient = useQueryClient();

  const { onSuccess, ...restConfig } = mutationConfig || {};

  return useMutation({
    onSuccess: (...args) => {
      queryClient.invalidateQueries({
        queryKey: ['taxonomy-data', 'taxonomy'],
      });

      onSuccess?.(...args);
    },
    onSettled: () => {
      queryClient.invalidateQueries({
        queryKey: ['taxonomy-data', 'taxonomy'],
      });
    },
    ...restConfig,
    mutationFn: switchTaxonomy,
  });
};
