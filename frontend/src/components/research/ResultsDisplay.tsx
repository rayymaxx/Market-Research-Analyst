import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { Download, Share, Eye } from 'lucide-react';
import ReactMarkdown from 'react-markdown';
import { Card } from '../ui/Card';
import { Button } from '../ui/Button';
import { PDFPreviewModal } from '../ui/PDFPreviewModal';
import { ResearchResponse } from '../../types';

interface ResultsDisplayProps {
  research: ResearchResponse;
}

export const ResultsDisplay: React.FC<ResultsDisplayProps> = ({ research }) => {
  const [showPDFPreview, setShowPDFPreview] = useState(false);
  
  if (!research.result) return null;

  const downloadPDF = async () => {
    try {
      const response = await fetch(`/api/research/${research.research_id}/download-pdf`);
      const blob = await response.blob();
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `market-research-${research.research_id}.pdf`;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
    } catch (error) {
      console.error('PDF download failed:', error);
    }
  };

  const previewPDF = () => {
    setShowPDFPreview(true);
  };



  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="space-y-6"
    >
      <Card>
        <div className="flex items-center justify-between mb-6">
          <div>
            <h3 className="text-xl font-bold text-white">Research Results</h3>
            <p className="text-gray-400">
              Completed: {new Date(research.completed_at || '').toLocaleString()}
            </p>
          </div>
          <div className="flex gap-2">
            <Button variant="outline" size="sm" onClick={previewPDF}>
              <Eye className="w-4 h-4" />
              Preview PDF
            </Button>
            <Button variant="outline" size="sm">
              <Share className="w-4 h-4" />
              Share
            </Button>
            <Button variant="primary" size="sm" onClick={downloadPDF}>
              <Download className="w-4 h-4" />
              Download PDF
            </Button>
          </div>
        </div>

        <div className="prose prose-invert max-w-none">
          <ReactMarkdown
            components={{
              h1: ({ children }) => (
                <h1 className="text-2xl font-bold text-white mb-4">{children}</h1>
              ),
              h2: ({ children }) => (
                <h2 className="text-xl font-semibold text-white mb-3 mt-6">{children}</h2>
              ),
              h3: ({ children }) => (
                <h3 className="text-lg font-medium text-white mb-2 mt-4">{children}</h3>
              ),
              p: ({ children }) => (
                <p className="text-gray-300 mb-4 leading-relaxed">{children}</p>
              ),
              ul: ({ children }) => (
                <ul className="list-disc list-inside text-gray-300 mb-4 space-y-1">
                  {children}
                </ul>
              ),
              ol: ({ children }) => (
                <ol className="list-decimal list-inside text-gray-300 mb-4 space-y-1">
                  {children}
                </ol>
              ),
              strong: ({ children }) => (
                <strong className="text-white font-semibold">{children}</strong>
              ),
              table: ({ children }) => (
                <div className="overflow-x-auto mb-4">
                  <table className="min-w-full border border-dark-600 rounded-lg">
                    {children}
                  </table>
                </div>
              ),
              th: ({ children }) => (
                <th className="px-4 py-2 bg-dark-700 text-white font-medium text-left border-b border-dark-600">
                  {children}
                </th>
              ),
              td: ({ children }) => (
                <td className="px-4 py-2 text-gray-300 border-b border-dark-700">
                  {children}
                </td>
              ),
            }}
          >
            {research.result}
          </ReactMarkdown>
        </div>
      </Card>
      
      <PDFPreviewModal
        isOpen={showPDFPreview}
        onClose={() => setShowPDFPreview(false)}
        pdfUrl={`/api/research/${research.research_id}/download-pdf`}
        researchId={research.research_id}
        onDownload={downloadPDF}
      />
    </motion.div>
  );
};