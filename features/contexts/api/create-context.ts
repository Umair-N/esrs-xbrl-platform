// contexts/api/create-context.ts
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { api } from '@/lib/api-client';
import type { MutationConfig } from '@/lib/react-query';

export type PeriodType = 'instant' | 'duration' | 'forever';
export type ContextStatus = 'valid' | 'warning' | 'error';

export interface CreateContextPayload {
  context_id: string;
  entity_scheme: string;
  entity_identifier: string;
  entity_name?: string;
  lei?: string;
  period_type: PeriodType;
  start_date?: string | null;
  end_date?: string | null;
  instant_date?: string | null;
  dimensions_json?: Record<string, any> | null;
  taxonomy_id?: number | null;
  is_default_context?: boolean;
  status?: ContextStatus;
  validation_messages?: Array<Record<string, any>>;
}

export const createContext = (payload: CreateContextPayload) =>
  api.post('/contexts', payload);

type UseCreateContextOptions = {
  mutationConfig?: MutationConfig<typeof createContext>;
};

export const useCreateContext = ({
  mutationConfig,
}: UseCreateContextOptions = {}) => {
  const queryClient = useQueryClient();
  const { onSuccess, ...rest } = mutationConfig || {};

  return useMutation({
    mutationFn: createContext,
    onSuccess: (...args) => {
      // refresh lists
      queryClient.invalidateQueries({ queryKey: ['contexts'] });
      onSuccess?.(...args);
    },
    ...rest,
  });
};
