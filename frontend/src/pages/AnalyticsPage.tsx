import React, { useEffect, useMemo } from 'react';
import { motion } from 'framer-motion';
import { TrendingUp, Clock, Target, BarChart3 } from 'lucide-react';
import { Card } from '../components/ui/Card';
import { useResearchStore } from '../store/useResearchStore';
import { useKnowledgeStore } from '../store/useKnowledgeStore';

export const AnalyticsPage: React.FC = () => {
  const { researchHistory, loadHistory } = useResearchStore();
  const { stats, loadStats } = useKnowledgeStore();

  useEffect(() => {
    loadHistory();
    loadStats();
  }, [loadHistory, loadStats]);

  const analytics = useMemo(() => {
    const completed = researchHistory.filter(r => r.status === 'completed').length;
    const failed = researchHistory.filter(r => r.status === 'failed').length;
    const total = researchHistory.length;
    const successRate = total > 0 ? Math.round((completed / total) * 100) : 0;

    return {
      totalResearch: total,
      completedResearch: completed,
      failedResearch: failed,
      successRate,
      totalDocuments: stats?.total_documents || 0
    };
  }, [researchHistory, stats]);

  return (
    <div className="max-w-7xl mx-auto p-6 space-y-8">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
      >
        <h1 className="text-3xl font-bold text-white mb-2">Analytics</h1>
        <p className="text-gray-400">Insights and metrics from your research activities</p>
      </motion.div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <Card>
          <div className="flex items-center gap-4">
            <div className="p-3 bg-primary-500/20 rounded-lg">
              <BarChart3 className="w-6 h-6 text-primary-500" />
            </div>
            <div>
              <p className="text-2xl font-bold text-white">{analytics.totalResearch}</p>
              <p className="text-gray-400 text-sm">Total Research</p>
            </div>
          </div>
        </Card>

        <Card>
          <div className="flex items-center gap-4">
            <div className="p-3 bg-success-500/20 rounded-lg">
              <Target className="w-6 h-6 text-success-500" />
            </div>
            <div>
              <p className="text-2xl font-bold text-white">{analytics.successRate}%</p>
              <p className="text-gray-400 text-sm">Success Rate</p>
            </div>
          </div>
        </Card>

        <Card>
          <div className="flex items-center gap-4">
            <div className="p-3 bg-secondary-500/20 rounded-lg">
              <Clock className="w-6 h-6 text-secondary-500" />
            </div>
            <div>
              <p className="text-2xl font-bold text-white">3.2 min</p>
              <p className="text-gray-400 text-sm">Avg. Time</p>
            </div>
          </div>
        </Card>

        <Card>
          <div className="flex items-center gap-4">
            <div className="p-3 bg-yellow-500/20 rounded-lg">
              <TrendingUp className="w-6 h-6 text-yellow-500" />
            </div>
            <div>
              <p className="text-2xl font-bold text-white">{analytics.totalDocuments}</p>
              <p className="text-gray-400 text-sm">Knowledge Docs</p>
            </div>
          </div>
        </Card>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <Card>
          <h3 className="text-xl font-semibold text-white mb-4">Research Status</h3>
          <div className="space-y-4">
            <div className="flex justify-between items-center">
              <span className="text-gray-300">Completed</span>
              <span className="text-success-500 font-medium">{analytics.completedResearch}</span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-gray-300">Failed</span>
              <span className="text-red-500 font-medium">{analytics.failedResearch}</span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-gray-300">Success Rate</span>
              <span className="text-primary-500 font-medium">{analytics.successRate}%</span>
            </div>
          </div>
        </Card>

        <Card>
          <h3 className="text-xl font-semibold text-white mb-4">Performance Insights</h3>
          <div className="space-y-4">
            <div className="flex justify-between items-center">
              <span className="text-gray-300">Research Quality</span>
              <span className="text-success-500 font-medium">
                {analytics.successRate >= 80 ? 'Excellent' : 
                 analytics.successRate >= 60 ? 'Good' : 'Needs Improvement'}
              </span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-gray-300">Knowledge Base</span>
              <span className="text-primary-500 font-medium">
                {analytics.totalDocuments > 0 ? 'Active' : 'Empty'}
              </span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-gray-300">Activity Level</span>
              <span className="text-white font-medium">
                {analytics.totalResearch > 10 ? 'High' : 
                 analytics.totalResearch > 5 ? 'Medium' : 'Low'}
              </span>
            </div>
          </div>
        </Card>
      </div>
    </div>
  );
};