import { useState, useCallback } from 'react';

interface AlertState {
  isOpen: boolean;
  title: string;
  message: string;
  type: 'success' | 'warning' | 'confirm';
  onConfirm?: () => void;
  confirmText?: string;
  cancelText?: string;
}

export const useAlert = () => {
  const [alert, setAlert] = useState<AlertState>({
    isOpen: false,
    title: '',
    message: '',
    type: 'success'
  });

  const showAlert = useCallback((config: Omit<AlertState, 'isOpen'>) => {
    setAlert({ ...config, isOpen: true });
  }, []);

  const showSuccess = useCallback((title: string, message: string) => {
    showAlert({ title, message, type: 'success' });
  }, [showAlert]);

  const showWarning = useCallback((title: string, message: string) => {
    showAlert({ title, message, type: 'warning' });
  }, [showAlert]);

  const showConfirm = useCallback((
    title: string, 
    message: string, 
    onConfirm: () => void,
    confirmText = 'Confirm',
    cancelText = 'Cancel'
  ) => {
    showAlert({ 
      title, 
      message, 
      type: 'confirm', 
      onConfirm, 
      confirmText, 
      cancelText 
    });
  }, [showAlert]);

  const closeAlert = useCallback(() => {
    setAlert(prev => ({ ...prev, isOpen: false }));
  }, []);

  return {
    alert,
    showAlert,
    showSuccess,
    showWarning,
    showConfirm,
    closeAlert
  };
};