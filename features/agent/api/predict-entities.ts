import { useMutation } from '@tanstack/react-query';

import { api } from '@/lib/api-client';
import { MutationConfig } from '@/lib/react-query';
import { showError } from '@/components/heads-up';
import { NERPredictRequest, NERPredictResponse } from '../types';

export const predictEntities = ({
  data,
}: {
  data: NERPredictRequest;
}): Promise<NERPredictResponse> => {
  return api.post('/predict', data, { serviceType: 'nerAgent' });
};

type UsePredictEntitiesOptions = {
  mutationConfig?: MutationConfig<typeof predictEntities>;
};

export const usePredictEntities = ({
  mutationConfig,
}: UsePredictEntitiesOptions = {}) => {
  const { onSuccess, ...restConfig } = mutationConfig || {};

  return useMutation({
    onSuccess: (...args) => {
      onSuccess?.(...args);
    },
    onError: (err) => {
      showError({ title: 'NER prediction failed', message: err.message || '' });
    },
    ...restConfig,
    mutationFn: predictEntities,
  });
};
