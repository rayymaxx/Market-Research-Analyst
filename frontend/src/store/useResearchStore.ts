import { create } from 'zustand';
import { ResearchResponse, ResearchRequest, ResearchHistoryItem } from '../types';
import { researchApi } from '../services/api';

interface ResearchStore {
  currentResearch: ResearchResponse | null;
  researchHistory: ResearchHistoryItem[];
  isLoading: boolean;
  error: string | null;
  
  // Actions
  startResearch: (request: ResearchRequest) => Promise<void>;
  pollResearchStatus: (researchId: string) => void;
  stopPolling: () => void;
  loadHistory: () => Promise<void>;
  clearError: () => void;
  setCurrentResearch: (research: ResearchResponse | null) => void;
}

let pollingInterval: NodeJS.Timeout | null = null;

export const useResearchStore = create<ResearchStore>((set, get) => ({
  currentResearch: null,
  researchHistory: [],
  isLoading: false,
  error: null,

  startResearch: async (request: ResearchRequest) => {
    set({ isLoading: true, error: null });
    try {
      const response = await researchApi.startResearch(request);
      set({ currentResearch: response, isLoading: false });
      
      // Start polling if research is pending or running
      if (response.status === 'pending' || response.status === 'running') {
        get().pollResearchStatus(response.research_id);
      }
    } catch (error: any) {
      set({ 
        error: error.response?.data?.detail || 'Failed to start research',
        isLoading: false 
      });
    }
  },

  pollResearchStatus: (researchId: string) => {
    // Clear existing polling
    if (pollingInterval) {
      clearInterval(pollingInterval);
    }

    pollingInterval = setInterval(async () => {
      try {
        const response = await researchApi.getResearchStatus(researchId);
        set({ currentResearch: response });
        
        // Stop polling if research is completed or failed
        if (response.status === 'completed' || response.status === 'failed') {
          get().stopPolling();
        }
      } catch (error) {
        console.error('Polling error:', error);
      }
    }, 2000); // Poll every 2 seconds
  },

  stopPolling: () => {
    if (pollingInterval) {
      clearInterval(pollingInterval);
      pollingInterval = null;
    }
  },

  loadHistory: async () => {
    try {
      const response = await researchApi.getResearchHistory();
      set({ researchHistory: response.history });
    } catch (error: any) {
      set({ error: error.response?.data?.detail || 'Failed to load history' });
    }
  },

  clearError: () => set({ error: null }),
  
  setCurrentResearch: (research: ResearchResponse | null) => {
    set({ currentResearch: research });
    if (!research) {
      get().stopPolling();
    }
  },
}));