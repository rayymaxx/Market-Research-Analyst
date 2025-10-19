import { create } from 'zustand';
import { KnowledgeStats } from '../types';
import { knowledgeApi } from '../services/api';

interface KnowledgeStore {
  stats: KnowledgeStats | null;
  files: any[];
  isLoading: boolean;
  error: string | null;
  
  // Actions
  loadStats: () => Promise<void>;
  uploadFile: (file: File) => Promise<void>;
  loadFiles: () => Promise<void>;
  deleteFile: (filename: string) => Promise<void>;
  reindexKnowledge: () => Promise<void>;
  clearError: () => void;
}

export const useKnowledgeStore = create<KnowledgeStore>((set, get) => ({
  stats: null,
  files: [],
  isLoading: false,
  error: null,

  loadStats: async () => {
    set({ isLoading: true, error: null });
    try {
      const stats = await knowledgeApi.getStats();
      set({ stats, isLoading: false });
    } catch (error: any) {
      set({ 
        error: error.response?.data?.detail || 'Failed to load knowledge stats',
        isLoading: false 
      });
    }
  },

  uploadFile: async (file: File) => {
    set({ isLoading: true, error: null });
    try {
      await knowledgeApi.uploadFile(file);
      // Reload stats and files after upload
      await Promise.all([
        get().loadStats(),
        get().loadFiles()
      ]);
      set({ isLoading: false });
    } catch (error: any) {
      set({ 
        error: error.response?.data?.detail || 'Failed to upload file',
        isLoading: false 
      });
    }
  },

  loadFiles: async () => {
    try {
      const response = await knowledgeApi.listFiles();
      set({ files: response.files || [] });
    } catch (error: any) {
      set({ error: error.response?.data?.detail || 'Failed to load files' });
    }
  },

  deleteFile: async (filename: string) => {
    try {
      await knowledgeApi.deleteFile(filename);
      // Reload files after deletion
      await get().loadFiles();
      await get().loadStats();
    } catch (error: any) {
      set({ error: error.response?.data?.detail || 'Failed to delete file' });
    }
  },

  reindexKnowledge: async () => {
    set({ isLoading: true, error: null });
    try {
      await knowledgeApi.reindex();
      await get().loadStats();
      set({ isLoading: false });
    } catch (error: any) {
      set({ 
        error: error.response?.data?.detail || 'Failed to reindex knowledge base',
        isLoading: false 
      });
    }
  },

  clearError: () => set({ error: null }),
}));