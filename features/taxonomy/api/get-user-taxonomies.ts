import { queryOptions, useQuery } from '@tanstack/react-query';

import { api } from '@/lib/api-client';
import { QueryConfig } from '@/lib/react-query';
import { TaxonomyList } from '@/types/taxonomy';

export const getUserTaxonomies = (): Promise<TaxonomyList[]> => {
  return api.get(`/taxonomy/my/taxonomies`);
};

export const getMyTaxonomy = () => {
  return queryOptions({
    queryKey: ['taxonomies', 'my'],
    queryFn: getUserTaxonomies,
  });
};

type UseUserStatsOptions = {
  queryConfig?: QueryConfig<typeof getMyTaxonomy>;
};

export const useMyTaxonomies = ({ queryConfig }: UseUserStatsOptions = {}) => {
  return useQuery({
    ...getMyTaxonomy(),
    ...queryConfig,
  });
};
