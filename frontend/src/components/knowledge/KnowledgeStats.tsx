import React from 'react';
import { motion } from 'framer-motion';
import { 
  Database, 
  Building, 
  FileText, 
  BarChart, 
  User,
  RefreshCw 
} from 'lucide-react';
import { Card } from '../ui/Card';
import { Button } from '../ui/Button';
import { KnowledgeStats as StatsType } from '../../types';

interface KnowledgeStatsProps {
  stats: StatsType;
  onReindex: () => void;
  isLoading: boolean;
}

const statItems = [
  {
    key: 'total_documents' as keyof StatsType,
    label: 'Total Documents',
    icon: Database,
    color: 'text-primary-500',
  },
  {
    key: 'company_profiles' as keyof StatsType,
    label: 'Company Profiles',
    icon: Building,
    color: 'text-secondary-500',
  },
  {
    key: 'industry_reports' as keyof StatsType,
    label: 'Industry Reports',
    icon: FileText,
    color: 'text-success-500',
  },
  {
    key: 'market_data' as keyof StatsType,
    label: 'Market Data',
    icon: BarChart,
    color: 'text-yellow-500',
  },
  {
    key: 'user_preferences' as keyof StatsType,
    label: 'User Preferences',
    icon: User,
    color: 'text-pink-500',
  },
];

export const KnowledgeStats: React.FC<KnowledgeStatsProps> = ({
  stats,
  onReindex,
  isLoading
}) => {
  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold text-white">Knowledge Base</h2>
          <p className="text-gray-400">
            Last updated: {new Date(stats.last_updated).toLocaleString()}
          </p>
        </div>
        <Button
          variant="outline"
          onClick={onReindex}
          isLoading={isLoading}
        >
          <RefreshCw className="w-4 h-4" />
          Reindex
        </Button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {statItems.map((item, index) => (
          <motion.div
            key={item.key}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: index * 0.1 }}
          >
            <Card hover className="text-center">
              <div className={`inline-flex p-3 rounded-full bg-dark-700 mb-4 ${item.color}`}>
                <item.icon className="w-6 h-6" />
              </div>
              <h3 className="text-2xl font-bold text-white mb-2">
                {stats[item.key] as number}
              </h3>
              <p className="text-gray-400 text-sm">{item.label}</p>
            </Card>
          </motion.div>
        ))}
      </div>
    </div>
  );
};