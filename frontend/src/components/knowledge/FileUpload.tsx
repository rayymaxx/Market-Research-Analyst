import React, { useCallback } from 'react';
import { motion } from 'framer-motion';
import { Upload, File, X } from 'lucide-react';
import { Card } from '../ui/Card';
import { Button } from '../ui/Button';

interface FileUploadProps {
  onUpload: (file: File) => void;
  isLoading: boolean;
}

export const FileUpload: React.FC<FileUploadProps> = ({ onUpload, isLoading }) => {
  const [dragActive, setDragActive] = React.useState(false);
  const [selectedFile, setSelectedFile] = React.useState<File | null>(null);

  const handleDrag = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true);
    } else if (e.type === 'dragleave') {
      setDragActive(false);
    }
  }, []);

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      setSelectedFile(e.dataTransfer.files[0]);
    }
  }, []);

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setSelectedFile(e.target.files[0]);
    }
  };

  const handleUpload = () => {
    if (selectedFile) {
      onUpload(selectedFile);
      setSelectedFile(null);
    }
  };

  const clearFile = () => {
    setSelectedFile(null);
  };

  return (
    <Card>
      <h3 className="text-lg font-semibold text-white mb-4">Upload Documents</h3>
      
      <div
        className={`border-2 border-dashed rounded-lg p-8 text-center transition-colors ${
          dragActive
            ? 'border-primary-500 bg-primary-500/10'
            : 'border-dark-600 hover:border-dark-500'
        }`}
        onDragEnter={handleDrag}
        onDragLeave={handleDrag}
        onDragOver={handleDrag}
        onDrop={handleDrop}
      >
        {selectedFile ? (
          <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            className="space-y-4"
          >
            <div className="flex items-center justify-center gap-3 p-4 bg-dark-700 rounded-lg">
              <File className="w-6 h-6 text-primary-500" />
              <div className="flex-1 text-left">
                <p className="text-white font-medium">{selectedFile.name}</p>
                <p className="text-gray-400 text-sm">
                  {(selectedFile.size / 1024 / 1024).toFixed(2)} MB
                </p>
              </div>
              <button
                onClick={clearFile}
                className="p-1 hover:bg-dark-600 rounded"
              >
                <X className="w-4 h-4 text-gray-400" />
              </button>
            </div>
            
            <div className="flex gap-2">
              <Button
                onClick={handleUpload}
                isLoading={isLoading}
                className="flex-1"
              >
                <Upload className="w-4 h-4" />
                Upload File
              </Button>
              <Button variant="outline" onClick={clearFile}>
                Cancel
              </Button>
            </div>
          </motion.div>
        ) : (
          <div className="space-y-4">
            <Upload className="w-12 h-12 text-gray-400 mx-auto" />
            <div>
              <p className="text-white font-medium mb-2">
                Drop files here or click to browse
              </p>
              <p className="text-gray-400 text-sm">
                Supports: PDF, DOCX, TXT, MD, JSON, CSV
              </p>
            </div>
            <input
              type="file"
              onChange={handleFileSelect}
              accept=".pdf,.docx,.txt,.md,.json,.csv"
              className="hidden"
              id="file-upload"
            />
            <label htmlFor="file-upload" className="cursor-pointer">
              <div className="inline-flex items-center gap-2 px-6 py-3 border-2 border-primary-500 text-primary-500 hover:bg-primary-500 hover:text-white rounded-lg transition-all duration-200">
                <Upload className="w-4 h-4" />
                Choose File
              </div>
            </label>
          </div>
        )}
      </div>

      <div className="mt-4 text-xs text-gray-400">
        <p>• Files will be processed and added to the knowledge base</p>
        <p>• Maximum file size: 10MB</p>
        <p>• Processing may take a few minutes for large files</p>
      </div>
    </Card>
  );
};