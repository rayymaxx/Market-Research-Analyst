import React, { useEffect, useState } from 'react';
import { motion } from 'framer-motion';
import { FileText, Download, Share, Eye, Calendar } from 'lucide-react';
import { Card } from '../components/ui/Card';
import { Button } from '../components/ui/Button';
import { PDFPreviewModal } from '../components/ui/PDFPreviewModal';
import { useResearchStore } from '../store/useResearchStore';

export const ReportsPage: React.FC = () => {
  const { researchHistory, loadHistory, getStoredReports } = useResearchStore();
  const [selectedReport, setSelectedReport] = useState<string | null>(null);
  const [showPDFPreview, setShowPDFPreview] = useState(false);
  const [currentReportId, setCurrentReportId] = useState<string>('');

  useEffect(() => {
    loadHistory();
  }, [loadHistory]);

  const storedReports = getStoredReports();
  const completedResearch = [...storedReports, ...researchHistory.filter(r => r.status === 'completed' && !storedReports.find(s => s.research_id === r.research_id))];

  const downloadPDF = async (research: any) => {
    try {
      const response = await fetch(`/api/research/${research.research_id}/download-pdf`);
      const blob = await response.blob();
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `${research.reportName || research.research_topic?.replace(/\s+/g, '-') || 'report'}.pdf`;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
      
      const count = parseInt(localStorage.getItem('downloads_count') || '0') + 1;
      localStorage.setItem('downloads_count', count.toString());
    } catch (error) {
      console.error('PDF download failed:', error);
    }
  };

  const previewPDF = (research: any) => {
    setCurrentReportId(research.research_id);
    setShowPDFPreview(true);
  };

  const shareReport = (research: any) => {
    if (navigator.share) {
      navigator.share({
        title: `Market Research: ${research.research_topic}`,
        text: `Check out this market research report on ${research.research_topic}`,
        url: window.location.href,
      });
    } else {
      navigator.clipboard.writeText(window.location.href);
      alert('Report link copied to clipboard!');
    }
  };

  return (
    <div className="max-w-7xl mx-auto p-6 space-y-8">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
      >
        <h1 className="text-3xl font-bold text-white mb-2">Research Reports</h1>
        <p className="text-gray-400">Export and share your completed research</p>
      </motion.div>

      {/* Stats */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <Card>
          <div className="flex items-center gap-4">
            <div className="p-3 bg-primary-500/20 rounded-lg">
              <FileText className="w-6 h-6 text-primary-500" />
            </div>
            <div>
              <p className="text-2xl font-bold text-white">{completedResearch.length}</p>
              <p className="text-gray-400 text-sm">Total Reports</p>
            </div>
          </div>
        </Card>

        <Card>
          <div className="flex items-center gap-4">
            <div className="p-3 bg-success-500/20 rounded-lg">
              <Calendar className="w-6 h-6 text-success-500" />
            </div>
            <div>
              <p className="text-2xl font-bold text-white">
                {completedResearch.filter(r => {
                  const created = new Date(r.created_at);
                  const today = new Date();
                  const diffTime = Math.abs(today.getTime() - created.getTime());
                  const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
                  return diffDays <= 7;
                }).length}
              </p>
              <p className="text-gray-400 text-sm">This Week</p>
            </div>
          </div>
        </Card>

        <Card>
          <div className="flex items-center gap-4">
            <div className="p-3 bg-secondary-500/20 rounded-lg">
              <Download className="w-6 h-6 text-secondary-500" />
            </div>
            <div>
              <p className="text-2xl font-bold text-white">
                {localStorage.getItem('downloads_count') || 0}
              </p>
              <p className="text-gray-400 text-sm">Downloads</p>
            </div>
          </div>
        </Card>
      </div>

      {/* Reports List */}
      <div className="space-y-4">
        {completedResearch.length > 0 ? (
          completedResearch.map((research) => (
            <motion.div
              key={research.research_id}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
            >
              <Card>
                <div className="flex items-center justify-between">
                  <div className="flex-1">
                    <h3 className="text-lg font-semibold text-white mb-2">
                      {(research as any).reportName || research.research_id}
                    </h3>
                    <div className="flex items-center gap-4 text-sm text-gray-400">
                      <span>Created: {new Date(research.created_at).toLocaleDateString()}</span>
                      {research.completed_at && (
                        <span>Completed: {new Date(research.completed_at).toLocaleDateString()}</span>
                      )}
                      <span className="px-2 py-1 bg-success-500/20 text-success-500 rounded">
                        Ready for Export
                      </span>
                    </div>
                  </div>
                  <div className="flex gap-2">
                    <Button
                      variant="ghost"
                      size="sm"
                      onClick={() => setSelectedReport(
                        selectedReport === research.research_id ? null : research.research_id
                      )}
                      title="Toggle Preview"
                    >
                      <Eye className="w-4 h-4" />
                    </Button>
                    <Button
                      variant="ghost"
                      size="sm"
                      onClick={() => previewPDF(research)}
                      title="PDF Preview"
                    >
                      <FileText className="w-4 h-4" />
                    </Button>
                    <Button
                      variant="ghost"
                      size="sm"
                      onClick={() => shareReport(research)}
                    >
                      <Share className="w-4 h-4" />
                    </Button>
                    <Button
                      variant="primary"
                      size="sm"
                      onClick={() => downloadPDF(research)}
                    >
                      <Download className="w-4 h-4" />
                    </Button>
                  </div>
                </div>

                {selectedReport === research.research_id && (
                  <motion.div
                    initial={{ opacity: 0, height: 0 }}
                    animate={{ opacity: 1, height: 'auto' }}
                    className="mt-4 pt-4 border-t border-dark-600"
                  >
                    <div className="bg-dark-700 p-4 rounded-lg">
                      <h4 className="text-white font-medium mb-2">Report Preview</h4>
                      <p className="text-gray-300 text-sm">
                        This report contains comprehensive market analysis for "{(research as any).reportName || research.research_id}" 
                        including competitive landscape, market trends, SWOT analysis, and strategic recommendations.
                      </p>
                      <div className="mt-3 flex gap-2">
                        <span className="px-2 py-1 bg-primary-500/20 text-primary-500 text-xs rounded">
                          Executive Summary
                        </span>
                        <span className="px-2 py-1 bg-secondary-500/20 text-secondary-500 text-xs rounded">
                          SWOT Analysis
                        </span>
                        <span className="px-2 py-1 bg-success-500/20 text-success-500 text-xs rounded">
                          Recommendations
                        </span>
                      </div>
                    </div>
                  </motion.div>
                )}
              </Card>
            </motion.div>
          ))
        ) : (
          <Card>
            <div className="text-center py-8">
              <FileText className="w-12 h-12 text-gray-400 mx-auto mb-4" />
              <p className="text-gray-400">No completed research reports yet.</p>
              <p className="text-gray-500 text-sm mt-2">
                Complete a research session to generate exportable reports.
              </p>
            </div>
          </Card>
        )}
      </div>
      
      <PDFPreviewModal
        isOpen={showPDFPreview}
        onClose={() => setShowPDFPreview(false)}
        pdfUrl={`/api/research/${currentReportId}/download-pdf`}
        researchId={currentReportId}
        onDownload={() => {
          const research = completedResearch.find(r => r.research_id === currentReportId);
          if (research) downloadPDF(research);
        }}
      />
    </div>
  );
};