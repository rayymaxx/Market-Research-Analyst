import React from 'react';
import { motion } from 'framer-motion';

interface ProgressBarProps {
  progress: number;
  className?: string;
  showPercentage?: boolean;
}

export const ProgressBar: React.FC<ProgressBarProps> = ({
  progress,
  className = '',
  showPercentage = true
}) => {
  return (
    <div className={`space-y-2 ${className}`}>
      <div className="flex justify-between items-center">
        <span className="text-sm text-gray-300">Progress</span>
        {showPercentage && (
          <span className="text-sm text-primary-500 font-medium">
            {progress}%
          </span>
        )}
      </div>
      <div className="w-full bg-dark-700 rounded-full h-2">
        <motion.div
          className="bg-gradient-to-r from-primary-500 to-secondary-500 h-2 rounded-full"
          initial={{ width: 0 }}
          animate={{ width: `${progress}%` }}
          transition={{ duration: 0.5, ease: "easeOut" }}
        />
      </div>
    </div>
  );
};