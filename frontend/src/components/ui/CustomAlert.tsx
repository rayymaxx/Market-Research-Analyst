import React from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { CheckCircle, AlertTriangle, X } from 'lucide-react';
import { Button } from './Button';

interface CustomAlertProps {
  isOpen: boolean;
  onClose: () => void;
  onConfirm?: () => void;
  title: string;
  message: string;
  type: 'success' | 'warning' | 'confirm';
  confirmText?: string;
  cancelText?: string;
}

export const CustomAlert: React.FC<CustomAlertProps> = ({
  isOpen,
  onClose,
  onConfirm,
  title,
  message,
  type,
  confirmText = 'OK',
  cancelText = 'Cancel'
}) => {
  const handleConfirm = () => {
    if (onConfirm) {
      onConfirm();
    }
    onClose();
  };

  const getIcon = () => {
    switch (type) {
      case 'success':
        return <CheckCircle className="w-6 h-6 text-success-500" />;
      case 'warning':
      case 'confirm':
        return <AlertTriangle className="w-6 h-6 text-yellow-500" />;
      default:
        return null;
    }
  };

  return (
    <AnimatePresence>
      {isOpen && (
        <>
          {/* Backdrop */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 bg-black/50 backdrop-blur-sm z-50"
            onClick={onClose}
          />
          
          {/* Alert Modal */}
          <motion.div
            initial={{ opacity: 0, scale: 0.9, y: 20 }}
            animate={{ opacity: 1, scale: 1, y: 0 }}
            exit={{ opacity: 0, scale: 0.9, y: 20 }}
            className="fixed inset-0 z-50 flex items-center justify-center p-4"
          >
            <div className="bg-gray-800/90 backdrop-blur-xl border border-gray-700/50 rounded-xl p-6 max-w-md w-full shadow-2xl">
              {/* Header */}
              <div className="flex items-center gap-3 mb-4">
                {getIcon()}
                <h3 className="text-lg font-semibold text-white">{title}</h3>
                <button
                  onClick={onClose}
                  className="ml-auto p-1 hover:bg-gray-700/50 rounded-lg transition-colors"
                >
                  <X className="w-4 h-4 text-gray-400" />
                </button>
              </div>
              
              {/* Message */}
              <p className="text-gray-300 mb-6">{message}</p>
              
              {/* Actions */}
              <div className="flex gap-3 justify-end">
                {type === 'confirm' && (
                  <Button variant="outline" onClick={onClose}>
                    {cancelText}
                  </Button>
                )}
                <Button 
                  onClick={handleConfirm}
                  variant={type === 'warning' || type === 'confirm' ? 'primary' : 'primary'}
                >
                  {confirmText}
                </Button>
              </div>
            </div>
          </motion.div>
        </>
      )}
    </AnimatePresence>
  );
};