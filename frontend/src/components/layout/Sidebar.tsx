import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { 
  Home, 
  Search, 
  Database, 
  History, 
  FileText,
  BarChart3,
  Settings,
  Info
} from 'lucide-react';
import { useLocation, Link } from 'react-router-dom';
import { InfoModal } from '../ui/InfoModal';

const navigation = [
  { name: 'Dashboard', href: '/dashboard', icon: Home },
  { name: 'New Research', href: '/research', icon: Search },
  { name: 'Knowledge Base', href: '/knowledge', icon: Database },
  { name: 'History', href: '/history', icon: History },
  { name: 'Reports', href: '/reports', icon: FileText },
  { name: 'Analytics', href: '/analytics', icon: BarChart3 },
  { name: 'Settings', href: '/settings', icon: Settings },
];

interface SidebarProps {
  onNavigate?: () => void;
}

export const Sidebar: React.FC<SidebarProps> = ({ onNavigate }) => {
  const location = useLocation();
  const [showInfo, setShowInfo] = useState(false);

  return (
    <>
      <motion.aside
        initial={{ x: -20, opacity: 0 }}
        animate={{ x: 0, opacity: 1 }}
        className="w-64 bg-dark-800/50 backdrop-blur-lg border-r border-dark-700 p-6 flex flex-col"
      >
        <nav className="space-y-2 flex-1">
          {navigation.map((item) => {
            const isActive = location.pathname === item.href;
            return (
              <Link
                key={item.name}
                to={item.href}
                onClick={onNavigate}
                className={`flex items-center gap-3 px-4 py-3 rounded-lg transition-all duration-200 ${
                  isActive
                    ? 'bg-primary-500 text-white shadow-lg'
                    : 'text-gray-300 hover:text-white hover:bg-dark-700'
                }`}
              >
                <item.icon className="w-5 h-5" />
                <span className="font-medium">{item.name}</span>
              </Link>
            );
          })}
        </nav>
        
        <button
          onClick={() => setShowInfo(true)}
          className="flex items-center gap-3 px-4 py-3 rounded-lg text-gray-300 hover:text-white hover:bg-dark-700 transition-all duration-200 mt-4"
        >
          <Info className="w-5 h-5" />
          <span className="font-medium">How to Use</span>
        </button>
      </motion.aside>
      
      <InfoModal isOpen={showInfo} onClose={() => setShowInfo(false)} />
    </>
  );
};