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
    <div className="space-y-6">
      <Card>
        <div className="flex items-center justify-between mb-6">
          <div>
            <h3 className="text-xl font-bold text-white">Research Progress</h3>
            <p className="text-gray-400">Current Phase: {progress.current_phase}</p>
          </div>
          <div className="flex items-center gap-2">
            {getStatusIcon(research.status)}
            <span className="text-sm font-medium capitalize">{research.status}</span>
          </div>
        </div>

        <ProgressBar progress={progress.progress_percentage} />
      </Card>

      <Card>
        <h4 className="text-lg font-semibold text-white mb-4">Agent Tasks</h4>
        <div className="space-y-4">
          {progress.tasks.map((task, index) => (
            <motion.div
              key={task.task_name}
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: index * 0.1 }}
              className={`p-4 rounded-lg border ${
                task.status === 'completed'
                  ? 'bg-success-500/10 border-success-500/30'
                  : task.status === 'running'
                  ? 'bg-primary-500/10 border-primary-500/30'
                  : task.status === 'failed'
                  ? 'bg-red-500/10 border-red-500/30'
                  : 'bg-dark-700 border-dark-600'
              }`}
            >
              <div className="flex items-center justify-between mb-2">
                <div className="flex items-center gap-3">
                  {getAgentIcon(task.agent)}
                  <div>
                    <h5 className="font-medium text-white">{task.agent}</h5>
                    <p className="text-sm text-gray-400 capitalize">
                      {task.task_name.replace(/_/g, ' ')}
                    </p>
                  </div>
                </div>
                {getStatusIcon(task.status)}
              </div>

              {task.tools_used.length > 0 && (
                <div className="mt-3">
                  <p className="text-xs text-gray-400 mb-1">Tools Used:</p>
                  <div className="flex flex-wrap gap-1">
                    {task.tools_used.map((tool) => (
                      <span
                        key={tool}
                        className="px-2 py-1 bg-dark-600 text-xs text-gray-300 rounded"
                      >
                        {tool}
                      </span>
                    ))}
                  </div>
                </div>
              )}

              {task.start_time && (
                <p className="text-xs text-gray-400 mt-2">
                  Started: {new Date(task.start_time).toLocaleTimeString()}
                </p>
              )}
            </motion.div>
          ))}
        </div>
      </Card>
    </div>
  );
};