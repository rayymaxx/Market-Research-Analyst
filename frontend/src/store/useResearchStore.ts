import { create } from 'zustand';
import { ResearchResponse, ResearchRequest, ResearchHistoryItem } from '../types';
import { researchApi } from '../services/api';
import { useAnalyticsStore } from './useAnalyticsStore';

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
  saveReportToStorage: (research: ResearchResponse) => void;
  getStoredReports: () => ResearchResponse[];
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
          if (response.status === 'completed') {
            get().saveReportToStorage(response);
          }
          
          // Update analytics
          const completionTime = response.completed_at ? 
            new Date(response.completed_at).getTime() - new Date(response.created_at).getTime() : undefined;
          useAnalyticsStore.getState().updateAnalytics(
            response.research_id,
            response.status,
            response.progress?.current_phase || 'Unknown',
            completionTime
          );
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

  saveReportToStorage: (research: ResearchResponse) => {
    const storedReports = get().getStoredReports();
    const topicName = research.progress?.current_phase?.replace(/[^a-zA-Z0-9]/g, '_') || 'Research';
    const reportName = `${topicName}_${new Date().toISOString().split('T')[0]}`;
    const reportWithName = { ...research, reportName };
    
    const updatedReports = [reportWithName, ...storedReports.filter(r => r.research_id !== research.research_id)];
    localStorage.setItem('research_reports', JSON.stringify(updatedReports));
  },

  getStoredReports: () => {
    try {
      const stored = localStorage.getItem('research_reports');
      return stored ? JSON.parse(stored) : [];
    } catch {
      return [];
    }
  },
}));