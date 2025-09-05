import { create } from 'zustand';

type Taxonomy = {
    id: number;
    name: string;
};

type TaxonomyStore = {
    selectedTaxonomy: Taxonomy | null;
    setSelectedTaxonomy: (taxonomy: Taxonomy) => void;
};

export const useTaxonomyStore = create<TaxonomyStore>((set) => ({
    selectedTaxonomy: null,
    setSelectedTaxonomy: (taxonomy) => set({ selectedTaxonomy: taxonomy }),
}));
