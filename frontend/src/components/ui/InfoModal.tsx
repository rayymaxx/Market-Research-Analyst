import React from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { X, Search, FileText, BarChart3, Download } from 'lucide-react';

interface InfoModalProps {
  isOpen: boolean;
  onClose: () => void;
}

export const InfoModal: React.FC<InfoModalProps> = ({ isOpen, onClose }) => {
  return (
    <AnimatePresence>
      {isOpen && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          className="fixed inset-0 bg-black/80 backdrop-blur-sm z-50 flex items-center justify-center p-4"
          onClick={onClose}
        >
          <motion.div
            initial={{ scale: 0.9, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            exit={{ scale: 0.9, opacity: 0 }}
            className="w-full max-w-2xl bg-dark-800 rounded-xl border border-dark-600 overflow-hidden"
            onClick={(e) => e.stopPropagation()}
          >
            <div className="flex items-center justify-between p-6 border-b border-dark-600">
              <h2 className="text-xl font-bold text-white">How to Use Market Research AI</h2>
              <button
                onClick={onClose}
                className="p-2 hover:bg-dark-700 text-gray-400 hover:text-white rounded-lg transition-colors"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            <div className="p-6 space-y-6 max-h-96 overflow-y-auto">
              <div className="space-y-4">
                <div className="flex items-start gap-3">
                  <div className="p-2 bg-primary-500/20 rounded-lg">
                    <Search className="w-5 h-5 text-primary-500" />
                  </div>
                  <div>
                    <h3 className="font-semibold text-white mb-1">1. Start Research</h3>
                    <p className="text-gray-300 text-sm">
                      Go to the Research page and enter your market research topic. Be specific about what you want to analyze (e.g., "Electric vehicle charging infrastructure market in North America").
                    </p>
                  </div>
                </div>

                <div className="flex items-start gap-3">
                  <div className="p-2 bg-secondary-500/20 rounded-lg">
                    <BarChart3 className="w-5 h-5 text-secondary-500" />
                  </div>
                  <div>
                    <h3 className="font-semibold text-white mb-1">2. Monitor Progress</h3>
                    <p className="text-gray-300 text-sm">
                      Watch as AI agents work on your research. You'll see real-time progress as they gather data, analyze competitors, and generate insights.
                    </p>
                  </div>
                </div>

                <div className="flex items-start gap-3">
                  <div className="p-2 bg-success-500/20 rounded-lg">
                    <FileText className="w-5 h-5 text-success-500" />
                  </div>
                  <div>
                    <h3 className="font-semibold text-white mb-1">3. Review Results</h3>
                    <p className="text-gray-300 text-sm">
                      Once complete, review your comprehensive market analysis including executive summary, SWOT analysis, competitive landscape, and strategic recommendations.
                    </p>
                  </div>
                </div>

                <div className="flex items-start gap-3">
                  <div className="p-2 bg-purple-500/20 rounded-lg">
                    <Download className="w-5 h-5 text-purple-500" />
                  </div>
                  <div>
                    <h3 className="font-semibold text-white mb-1">4. Export & Share</h3>
                    <p className="text-gray-300 text-sm">
                      Download your report as PDF, preview it in-browser, or access it later from the Reports page. All reports are automatically saved for future reference.
                    </p>
                  </div>
                </div>
              </div>

              <div className="bg-dark-700 p-4 rounded-lg">
                <h4 className="font-semibold text-white mb-2">💡 Pro Tips</h4>
                <ul className="text-gray-300 text-sm space-y-1">
                  <li>• Be specific with your research topics for better results</li>
                  <li>• Upload relevant documents to enhance AI knowledge</li>
                  <li>• Check the Analytics page to track your research history</li>
                  <li>• Use the Knowledge Base to manage your research documents</li>
                </ul>
              </div>
            </div>
          </motion.div>
        </motion.div>
      )}
    </AnimatePresence>
  );
};