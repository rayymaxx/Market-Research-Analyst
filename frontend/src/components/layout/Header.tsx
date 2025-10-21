import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { Brain, Settings, User, Menu, X, Info } from 'lucide-react';
import { Button } from '../ui/Button';
import { useNavigate } from 'react-router-dom';
import { Sidebar } from './Sidebar';
import { InfoModal } from '../ui/InfoModal';

export const Header: React.FC = () => {
  const navigate = useNavigate();
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const [showInfo, setShowInfo] = useState(false);

  return (
    <>
      <motion.header
        initial={{ y: -20, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        className="bg-dark-800/50 backdrop-blur-lg border-b border-dark-700 px-4 sm:px-6 py-4"
      >
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <Button
              variant="ghost"
              size="sm"
              className="lg:hidden"
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            >
              {mobileMenuOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
            </Button>
            <div className="p-2 bg-primary-500 rounded-lg">
              <Brain className="w-6 h-6 text-white" />
            </div>
            <div className="hidden sm:block">
              <h1 className="text-xl font-bold text-white">Market Research AI</h1>
              <p className="text-sm text-gray-400">Powered by Multi-Agent Intelligence</p>
            </div>
          </div>
          
          <div className="flex items-center gap-2">
            <Button variant="ghost" size="sm" onClick={() => setShowInfo(true)}>
              <Info className="w-4 h-4" />
              <span className="hidden md:inline ml-2">Help</span>
            </Button>
            <Button variant="ghost" size="sm" onClick={() => navigate('/settings')} className="hidden sm:flex">
              <Settings className="w-4 h-4" />
              <span className="hidden md:inline ml-2">Settings</span>
            </Button>
            <Button variant="ghost" size="sm" onClick={() => navigate('/settings')}>
              <User className="w-4 h-4" />
              <span className="hidden md:inline ml-2">Profile</span>
            </Button>
          </div>
        </div>
      </motion.header>
      
      {mobileMenuOpen && (
        <div className="lg:hidden fixed inset-0 z-50 bg-black/50" onClick={() => setMobileMenuOpen(false)}>
          <div className="w-64 h-full bg-dark-800 border-r border-dark-700" onClick={(e) => e.stopPropagation()}>
            <Sidebar onNavigate={() => setMobileMenuOpen(false)} />
          </div>
        </div>
      )}
      
      <InfoModal isOpen={showInfo} onClose={() => setShowInfo(false)} />
    </>
  );
};