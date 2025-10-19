import React, { useEffect } from 'react';
import { motion } from 'framer-motion';
import { BarChart3, Clock, CheckCircle, Database } from 'lucide-react';
import { Card } from '../components/ui/Card';
import { useResearchStore } from '../store/useResearchStore';
import { useKnowledgeStore } from '../store/useKnowledgeStore';

export const DashboardPage: React.FC = () => {
  const { researchHistory, loadHistory } = useResearchStore();
  const { stats, loadStats } = useKnowledgeStore();

  useEffect(() => {
    loadHistory();
    loadStats();
  }, [loadHistory, loadStats]);

  const recentResearch = researchHistory.slice(0, 5);
  const completedCount = researchHistory.filter(r => r.status === 'completed').length;
  const pendingCount = researchHistory.filter(r => r.status === 'pending' || r.status === 'running').length;

  return (
    <div className="max-w-7xl mx-auto p-6 space-y-8">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
      >
        <h1 className="text-3xl font-bold text-white mb-2">Dashboard</h1>
        <p className="text-gray-400">Overview of your market research activities</p>
      </motion.div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <Card>
          <div className="flex items-center gap-4">
            <div className="p-3 bg-primary-500/20 rounded-lg">
              <BarChart3 className="w-6 h-6 text-primary-500" />
            </div>
            <div>
              <p className="text-2xl font-bold text-white">{researchHistory.length}</p>
              <p className="text-gray-400 text-sm">Total Research</p>
            </div>
          </div>
        </Card>

        <Card>
          <div className="flex items-center gap-4">
            <div className="p-3 bg-success-500/20 rounded-lg">
              <CheckCircle className="w-6 h-6 text-success-500" />
            </div>
            <div>
              <p className="text-2xl font-bold text-white">{completedCount}</p>
              <p className="text-gray-400 text-sm">Completed</p>
            </div>
          </div>
        </Card>

        <Card>
          <div className="flex items-center gap-4">
            <div className="p-3 bg-yellow-500/20 rounded-lg">
              <Clock className="w-6 h-6 text-yellow-500" />
            </div>
            <div>
              <p className="text-2xl font-bold text-white">{pendingCount}</p>
              <p className="text-gray-400 text-sm">In Progress</p>
            </div>
          </div>
        </Card>

        <Card>
          <div className="flex items-center gap-4">
            <div className="p-3 bg-secondary-500/20 rounded-lg">
              <Database className="w-6 h-6 text-secondary-500" />
            </div>
            <div>
              <p className="text-2xl font-bold text-white">{stats?.total_documents || 0}</p>
              <p className="text-gray-400 text-sm">Knowledge Docs</p>
            </div>
          </div>
        </Card>
      </div>

      {/* Recent Activity */}
      <Card>
        <h3 className="text-xl font-semibold text-white mb-4">Recent Research</h3>
        {recentResearch.length > 0 ? (
          <div className="space-y-3">
            {recentResearch.map((research) => (
              <div key={research.research_id} className="flex items-center justify-between p-3 bg-dark-700 rounded-lg">
                <div>
                  <p className="text-white font-medium">{research.research_topic}</p>
                  <p className="text-gray-400 text-sm">
                    {new Date(research.created_at).toLocaleDateString()}
                  </p>
                </div>
                <span className={`px-2 py-1 rounded text-xs ${
                  research.status === 'completed' ? 'bg-success-500/20 text-success-500' :
                  research.status === 'failed' ? 'bg-red-500/20 text-red-500' :
                  'bg-yellow-500/20 text-yellow-500'
                }`}>
                  {research.status}
                </span>
              </div>
            ))}
          </div>
        ) : (
          <p className="text-gray-400">No research history yet. Start your first research!</p>
        )}
      </Card>
    </div>
  );
};