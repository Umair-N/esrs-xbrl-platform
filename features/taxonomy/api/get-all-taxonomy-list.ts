import { queryOptions, useQuery } from '@tanstack/react-query';

import { api } from '@/lib/api-client';
import { QueryConfig } from '@/lib/react-query';
import { TaxonomyList } from '@/types/taxonomy';

export const getAllTaxonomyList = (): Promise<TaxonomyList[]> => {
  return api.get(`/taxonomy/admin/list`);
};

export const getTaxonomyList = () => {
  return queryOptions({
    queryKey: ['all', 'taxonomies'],
    queryFn: getAllTaxonomyList,
  });
};

type UseAllTaxonomiesOptions = {
  queryConfig?: QueryConfig<typeof getTaxonomyList>;
};

export const useAllTaxonomies = ({
  queryConfig,
}: UseAllTaxonomiesOptions = {}) => {
  return useQuery({
    ...getTaxonomyList(),
    ...queryConfig,
  });
};
