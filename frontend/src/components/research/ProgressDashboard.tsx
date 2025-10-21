import React from 'react';
import { motion } from 'framer-motion';
import { 
  Clock, 
  CheckCircle, 
  AlertCircle, 
  Users, 
  Wrench,
  FileText 
} from 'lucide-react';
import { Card } from '../ui/Card';
import { ProgressBar } from '../ui/ProgressBar';
import { ResearchResponse } from '../../types';

interface ProgressDashboardProps {
  research: ResearchResponse;
}

const getStatusIcon = (status: string) => {
  switch (status) {
    case 'completed':
      return <CheckCircle className="w-5 h-5 text-success-500" />;
    case 'running':
      return <Clock className="w-5 h-5 text-primary-500 animate-spin" />;
    case 'failed':
      return <AlertCircle className="w-5 h-5 text-red-500" />;
    default:
      return <Clock className="w-5 h-5 text-gray-400" />;
  }
};

const getAgentIcon = (agent: string) => {
  switch (agent) {
    case 'Digital Intelligence Gatherer':
      return <Wrench className="w-4 h-4" />;
    case 'Quantitative Insights Specialist':
      return <Users className="w-4 h-4" />;
    case 'Strategic Communications Expert':
      return <FileText className="w-4 h-4" />;
    default:
      return <Users className="w-4 h-4" />;
  }
};

export const ProgressDashboard: React.FC<ProgressDashboardProps> = ({ research }) => {
  const { progress } = research;

  if (!progress) return null;

  return (
    <motion.div 
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="space-y-6"
    >
      <Card>
        <div className="flex items-center justify-between mb-6">
          <div>
            <h3 className="text-xl font-bold text-white">AI Crew Active</h3>
            <p className="text-gray-400">{progress.current_phase}</p>
          </div>
          <div className="flex items-center gap-2">
            {getStatusIcon(research.status)}
            <span className="text-sm font-medium capitalize">{research.status}</span>
          </div>
        </div>

        <ProgressBar progress={progress.progress_percentage} />
        
        <div className="mt-4 text-center">
          <p className="text-sm text-gray-400">
            {research.status === 'running' ? 'Agents are working...' : 
             research.status === 'completed' ? 'Research completed!' : 'Processing...'}
          </p>
        </div>
      </Card>

      {progress.tasks.length > 0 && (
        <Card>
          <h4 className="text-lg font-semibold text-white mb-4">Active Agents</h4>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
            {progress.tasks.map((task, index) => (
              <motion.div
                key={task.task_name}
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ delay: index * 0.1 }}
                className={`p-3 rounded-lg border text-center ${
                  task.status === 'completed'
                    ? 'bg-success-500/10 border-success-500/30'
                    : task.status === 'running'
                    ? 'bg-primary-500/10 border-primary-500/30'
                    : 'bg-dark-700 border-dark-600'
                }`}
              >
                <div className="flex items-center justify-center gap-2 mb-2">
                  {getAgentIcon(task.agent)}
                  {getStatusIcon(task.status)}
                </div>
                <h5 className="font-medium text-white text-sm">{task.agent}</h5>
                <p className="text-xs text-gray-400 capitalize">
                  {task.task_name.replace(/_/g, ' ')}
                </p>
              </motion.div>
            ))}
          </div>
        </Card>
      )}
    </motion.div>
  );
};}