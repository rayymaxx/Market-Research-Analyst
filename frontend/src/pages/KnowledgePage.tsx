import React, { useEffect } from 'react';
import { motion } from 'framer-motion';
import { KnowledgeStats } from '../components/knowledge/KnowledgeStats';
import { FileUpload } from '../components/knowledge/FileUpload';
import { useKnowledgeStore } from '../store/useKnowledgeStore';

export const KnowledgePage: React.FC = () => {
  const {
    stats,
    isLoading,
    error,
    loadStats,
    uploadFile,
    reindexKnowledge,
    clearError
  } = useKnowledgeStore();

  useEffect(() => {
    loadStats();
    clearError();
  }, [loadStats, clearError]);

  const handleFileUpload = async (file: File) => {
    await uploadFile(file);
  };

  const handleReindex = async () => {
    await reindexKnowledge();
  };

  return (
    <div className="max-w-7xl mx-auto p-6 space-y-8">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="text-center"
      >
        <h1 className="text-3xl font-bold text-white mb-2">
          Knowledge Base Management
        </h1>
        <p className="text-gray-400">
          Upload and manage documents to enhance AI research capabilities
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

      <div className="grid grid-cols-1 xl:grid-cols-3 gap-6 lg:gap-8">
        <div className="xl:col-span-2">
          {stats && (
            <KnowledgeStats
              stats={stats}
              onReindex={handleReindex}
              isLoading={isLoading}
            />
          )}
        </div>
        
        <div>
          <FileUpload
            onUpload={handleFileUpload}
            isLoading={isLoading}
          />
        </div>
      </div>
    </div>
  );
};