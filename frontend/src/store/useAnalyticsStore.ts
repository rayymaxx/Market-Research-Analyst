import { create } from 'zustand';

interface AnalyticsData {
  totalReports: number;
  completedReports: number;
  failedReports: number;
  averageCompletionTime: number;
  recentActivity: Array<{
    id: string;
    action: string;
    timestamp: Date;
    topic: string;
  }>;
}

interface AnalyticsStore {
  analytics: AnalyticsData;
  updateAnalytics: (researchId: string, status: string, topic: string, completionTime?: number) => void;
  getAnalytics: () => AnalyticsData;
}

export const useAnalyticsStore = create<AnalyticsStore>((set, get) => ({
  analytics: {
    totalReports: 0,
    completedReports: 0,
    failedReports: 0,
    averageCompletionTime: 0,
    recentActivity: []
  },

  updateAnalytics: (researchId: string, status: string, topic: string, completionTime?: number) => {
    const current = get().analytics;
    const activity = {
      id: researchId,
      action: status === 'completed' ? 'Report Generated' : 'Research Failed',
      timestamp: new Date(),
      topic
    };

    const updatedAnalytics = {
      ...current,
      totalReports: current.totalReports + 1,
      completedReports: status === 'completed' ? current.completedReports + 1 : current.completedReports,
      failedReports: status === 'failed' ? current.failedReports + 1 : current.failedReports,
      averageCompletionTime: completionTime ? 
        (current.averageCompletionTime + completionTime) / 2 : current.averageCompletionTime,
      recentActivity: [activity, ...current.recentActivity.slice(0, 9)]
    };

    set({ analytics: updatedAnalytics });
    localStorage.setItem('research_analytics', JSON.stringify(updatedAnalytics));
  },

  getAnalytics: () => {
    try {
      const stored = localStorage.getItem('research_analytics');
      if (stored) {
        const analytics = JSON.parse(stored);
        set({ analytics });
        return analytics;
      }
    } catch (error) {
      console.error('Failed to load analytics:', error);
    }
    return get().analytics;
  }
}));