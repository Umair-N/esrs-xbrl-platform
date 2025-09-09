import { useQuery } from '@tanstack/react-query';
import { api } from '@/lib/api-client';

export type PeriodType = 'instant' | 'duration' | 'forever';
export type ContextStatus = 'valid' | 'warning' | 'error';

// types/context.ts
export interface ContextOut {
  id: number;
  user_id: number;
  context_id: string;
  entity_scheme: string;
  entity_identifier: string;
  entity_name?: string | null;
  lei?: string | null;
  period_type: PeriodType;
  start_date?: string | null;
  end_date?: string | null;
  instant_date?: string | null;
  dimensions_json?: Record<string, any> | null;
  taxonomy_id?: number | null;
  content_hash: string;
  is_default_context: boolean;
  status: ContextStatus;
  validation_messages?: Array<Record<string, any>> | null;
  created_at: string;
  updated_at: string;
}

export interface ListFilters {
  entity_identifier?: string;
  period_type?: PeriodType;
  taxonomy_id?: number;
  context_id?: string;
  date_from?: string; // YYYY-MM-DD
  date_to?: string; // YYYY-MM-DD
  is_default_context?: boolean; // optional boolean filter
  limit?: number;
  offset?: number;
}

export const useContexts = (filters: ListFilters = {}) => {
  return useQuery<ContextOut[], Error>({
    queryKey: [
      'contexts',
      'list',
      filters.entity_identifier,
      filters.period_type,
      filters.taxonomy_id,
      filters.context_id,
      filters.date_from,
      filters.date_to,
      filters.is_default_context,
      filters.limit ?? 50,
      filters.offset ?? 0,
    ],
    queryFn: async () => {
      // Build params like your taxonomy hook (booleans as string)
      const params: Record<string, string | number | undefined> = {};

      if (filters.entity_identifier)
        params.entity_identifier = filters.entity_identifier;
      if (filters.period_type) params.period_type = filters.period_type;
      if (typeof filters.taxonomy_id === 'number')
        params.taxonomy_id = filters.taxonomy_id;
      if (filters.context_id) params.context_id = filters.context_id;
      if (filters.date_from) params.date_from = filters.date_from;
      if (filters.date_to) params.date_to = filters.date_to;
      if (typeof filters.is_default_context === 'boolean') {
        params.is_default_context = filters.is_default_context
          ? 'true'
          : 'false';
      }
      params.limit = typeof filters.limit === 'number' ? filters.limit : 50;
      params.offset = typeof filters.offset === 'number' ? filters.offset : 0;

      const res = await api.get<ContextOut[]>('/contexts', { params });
      return res;
    },
    staleTime: 60_000,
    refetchOnWindowFocus: false,
  });
};
