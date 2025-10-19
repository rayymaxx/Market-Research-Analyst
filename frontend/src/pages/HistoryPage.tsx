import React, { useEffect, useState } from 'react';
import { motion } from 'framer-motion';
import { Trash2, Eye } from 'lucide-react';
import { Card } from '../components/ui/Card';
import { Button } from '../components/ui/Button';
import { Input } from '../components/ui/Input';
import { useResearchStore } from '../store/useResearchStore';

export const HistoryPage: React.FC = () => {
  const { researchHistory, loadHistory, setCurrentResearch } = useResearchStore();
  const [searchTerm, setSearchTerm] = useState('');
  const [statusFilter, setStatusFilter] = useState('all');

  useEffect(() => {
    loadHistory();
  }, [loadHistory]);

  const filteredHistory = researchHistory.filter(research => {
    const matchesSearch = research.research_topic.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesStatus = statusFilter === 'all' || research.status === statusFilter;
    return matchesSearch && matchesStatus;
  });

  const handleViewResearch = (researchId: string) => {
    const research = researchHistory.find(r => r.research_id === researchId);
    if (research) {
      setCurrentResearch({
        ...research,
        progress: {
          current_phase: 'completed',
          completed_tasks: ['all'],
          tasks: [],
          progress_percentage: 100
        }
      });
    }
  };

  const handleDeleteResearch = (researchId: string) => {
    // Remove from localStorage
    const stored = localStorage.getItem('research_history') || '[]';
    const history = JSON.parse(stored);
    const updated = history.filter((r: any) => r.research_id !== researchId);
    localStorage.setItem('research_history', JSON.stringify(updated));
    loadHistory();
  };

  return (
    <div className="max-w-7xl mx-auto p-6 space-y-8">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
      >
        <h1 className="text-3xl font-bold text-white mb-2">Research History</h1>
        <p className="text-gray-400">View and manage your past research sessions</p>
      </motion.div>

      {/* Filters */}
      <Card>
        <div className="flex flex-col md:flex-row gap-4">
          <div className="flex-1">
            <Input
              placeholder="Search research topics..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
            />
          </div>
          <select
            value={statusFilter}
            onChange={(e) => setStatusFilter(e.target.value)}
            className="input-field"
          >
            <option value="all">All Status</option>
            <option value="completed">Completed</option>
            <option value="failed">Failed</option>
            <option value="pending">Pending</option>
            <option value="running">Running</option>
          </select>
        </div>
      </Card>

      {/* History List */}
      <div className="space-y-4">
        {filteredHistory.length > 0 ? (
          filteredHistory.map((research) => (
            <motion.div
              key={research.research_id}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
            >
              <Card>
                <div className="flex items-center justify-between">
                  <div className="flex-1">
                    <h3 className="text-lg font-semibold text-white mb-2">
                      {research.research_topic}
                    </h3>
                    <div className="flex items-center gap-4 text-sm text-gray-400">
                      <span>Created: {new Date(research.created_at).toLocaleDateString()}</span>
                      {research.completed_at && (
                        <span>Completed: {new Date(research.completed_at).toLocaleDateString()}</span>
                      )}
                      <span className={`px-2 py-1 rounded ${
                        research.status === 'completed' ? 'bg-success-500/20 text-success-500' :
                        research.status === 'failed' ? 'bg-red-500/20 text-red-500' :
                        'bg-yellow-500/20 text-yellow-500'
                      }`}>
                        {research.status}
                      </span>
                    </div>
                  </div>
                  <div className="flex gap-2">
                    <Button
                      variant="ghost"
                      size="sm"
                      onClick={() => handleViewResearch(research.research_id)}
                    >
                      <Eye className="w-4 h-4" />
                    </Button>
                    <Button
                      variant="ghost"
                      size="sm"
                      onClick={() => handleDeleteResearch(research.research_id)}
                    >
                      <Trash2 className="w-4 h-4" />
                    </Button>
                  </div>
                </div>
              </Card>
            </motion.div>
          ))
        ) : (
          <Card>
            <div className="text-center py-8">
              <p className="text-gray-400">No research history found.</p>
              <p className="text-gray-500 text-sm mt-2">
                {searchTerm || statusFilter !== 'all' 
                  ? 'Try adjusting your filters.' 
                  : 'Start your first research to see it here!'}
              </p>
            </div>
          </Card>
        )}
      </div>
    </div>
  );
};