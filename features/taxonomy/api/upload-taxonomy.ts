// taxonomy/api/upload-taxonomy.ts
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { api } from '@/lib/api-client';
import { MutationConfig } from '@/lib/react-query';

export interface UploadTaxonomyPayload {
  name: string;
  file: File;
}

export const uploadTaxonomy = ({ name, file }: UploadTaxonomyPayload) => {
  const formData = new FormData();
  formData.append('name', name);
  formData.append('file', file);

  return api.post('/taxonomy/admin/upload', formData, {
    params: { name },
  });
};

type UseUploadTaxonomyOptions = {
  mutationConfig?: MutationConfig<typeof uploadTaxonomy>;
};

export const useUploadTaxonomy = ({
  mutationConfig,
}: UseUploadTaxonomyOptions = {}) => {
  const queryClient = useQueryClient();

  const { onSuccess, ...restConfig } = mutationConfig || {};

  return useMutation({
    onSuccess: (...args) => {
      queryClient.invalidateQueries({
        queryKey: ['all', 'taxonomies'],
      });
      onSuccess?.(...args);
    },
    ...restConfig,
    mutationFn: uploadTaxonomy,
  });
};
