import { api } from '@/lib/api-client';
import { useQuery } from '@tanstack/react-query';

type TaxonomyData = any; // Adjust according to your expected data type

// Your hook will be dynamic based on various filters
export const useTaxonomyData = ({
  filter_key,
  filter_value,
  search_query,
  search_field = 'label',
  parent_id,
  level,
  chunk_bytes = 65536,
  download = false,
  raw = false,
  entity = 'presentations',
}: {
  filter_key?: string;
  filter_value?: string;
  search_query?: string;
  search_field?: string;
  parent_id?: number;
  level?: number;
  chunk_bytes?: number;
  download?: boolean;
  raw?: boolean;
  entity?: string;
}) => {
  return useQuery<TaxonomyData, Error>({
    queryKey: [
      'taxonomy',
      filter_key,
      filter_value,
      search_query,
      parent_id,
      level,
      entity,
    ],
    queryFn: async () => {
      const params: Record<string, string | number | boolean | undefined> = {};

      if (filter_key) params.filter_key = filter_key;
      if (filter_value) params.filter_value = filter_value;
      if (search_query) params.search_query = search_query;
      if (search_field) params.search_field = search_field;
      if (parent_id !== undefined) params.parent_id = parent_id;
      if (level !== undefined) params.level = level;
      if (chunk_bytes) params.chunk_bytes = chunk_bytes;

      // Handling download and raw as query parameters correctly
      params.download = download ? 'true' : 'false'; // Ensure "true" / "false" strings are passed
      params.raw = raw ? 'true' : 'false'; // Ensure "true" / "false" strings are passed

      const response = await api.get<TaxonomyData>(`/taxonomy/${entity}`, {
        params, // Axios will automatically serialize the parameters into the query string
      });

      return response;
    },
    staleTime: 60_000, // Optional: to manage cache time
    refetchOnWindowFocus: false,
  });
};
