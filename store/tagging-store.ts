import { create } from 'zustand';

/**
 * A global store used to coordinate tagging interactions between the text editor
 * and the tagging panel. When a user selects a recommendation from the
 * suggestion popover, the selected concept is stored here as a pending
 * concept. The tagging panel reads this pending concept and preselects it,
 * allowing the user to choose a context before finalising the tag. The
 * selected context is also persisted in this store so that other parts of
 * the application, such as the editor, can access it when needed.
 */
type RecommendationConcept = {
    /**
     * The unique identifier for the concept. This corresponds to the tag name
     * returned by the recommendation service.
     */
    id: string;
    /**
     * A human‑readable label or reference for the concept. Used by the
     * taxonomy tree and tagging panel to display the concept to the user.
     */
    label: string;
    /**
     * A definition or original label associated with the concept. When
     * available, this will populate the definition field in the tagging
     * panel.
     */
    definition: string;
    /**
     * The data type of the concept (e.g. monetary, string, etc.).
     */
    type: string;
    /**
     * The period type of the concept (e.g. instant or duration). When not
     * provided by the recommendation service, this may be left empty and
     * resolved later by the taxonomy lookup.
     */
    periodType: string;

    /**
     * Optional feedback ID associated with the recommendation. This is
     * returned from the AI recommender when feedback is posted for a
     * selected suggestion. When present, it allows the tagging panel
     * and other components to remove the corresponding feedback on
     * deletion of a tag.
     */
    feedbackId?: number;
};

type TaggingStore = {
    /**
     * A concept that has been selected from the recommendation popover but has
     * not yet been committed as a tag. When present, the tagging panel will
     * automatically preselect this concept and clear the value afterwards.
     */
    pendingConcept: RecommendationConcept | null;
    /**
     * Update the pending concept stored in the tagging store. Passing null
     * clears any existing pending concept.
     */
    setPendingConcept: (concept: RecommendationConcept | null) => void;
    /**
     * The ID of the currently selected context. This is persisted in the
     * store so that tags created outside the tagging panel (for example via
     * recommendations) can include the selected context if appropriate.
     */
    selectedContextId: string | null;
    /**
     * Update the currently selected context ID. Components should call this
     * whenever the user changes the context selection.
     */
    setSelectedContextId: (contextId: string | null) => void;
};

export const useTaggingStore = create<TaggingStore>((set) => ({
    pendingConcept: null,
    setPendingConcept: (concept) => set({ pendingConcept: concept }),
    selectedContextId: null,
    setSelectedContextId: (contextId) => set({ selectedContextId: contextId }),
}));