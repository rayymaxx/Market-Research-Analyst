import React, { useEffect } from 'react';
import { motion } from 'framer-motion';
import { ResearchForm } from '../components/research/ResearchForm';
import { ProgressDashboard } from '../components/research/ProgressDashboard';
import { ResultsDisplay } from '../components/research/ResultsDisplay';
import { useResearchStore } from '../store/useResearchStore';

export const ResearchPage: React.FC = () => {
  const { currentResearch, error, clearError } = useResearchStore();

  useEffect(() => {
    // Clear any existing errors when component mounts
    clearError();
  }, [clearError]);

  return (
    <div className="max-w-7xl mx-auto p-6 space-y-8">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="text-center"
      >
        <h1 className="text-3xl font-bold text-white mb-2">
          AI Market Research
        </h1>
        <p className="text-gray-400">
          Let our intelligent agents conduct comprehensive market analysis for you
        </p>
      </motion.div>

      {error && (
        <motion.div
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          className="bg-red-500/10 border border-red-500/30 rounded-lg p-4"
        >
          <p className="text-red-400">{error}</p>
        </motion.div>
      )}

      <div className="grid grid-cols-1 xl:grid-cols-2 gap-6 lg:gap-8">
        <div>
          <ResearchForm />
        </div>
        
        <div className="space-y-6">
          {currentResearch && (
            <>
              <ProgressDashboard research={currentResearch} />
              {currentResearch.status === 'completed' && currentResearch.result && (
                <ResultsDisplay research={currentResearch} />
              )}
            </>
          )}
        </div>
      </div>
    </div>
  );
};