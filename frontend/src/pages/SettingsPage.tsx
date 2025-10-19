import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { Save, RefreshCw, Database, Bell, User } from 'lucide-react';
import { Card } from '../components/ui/Card';
import { Button } from '../components/ui/Button';
import { Input } from '../components/ui/Input';

export const SettingsPage: React.FC = () => {
  const [settings, setSettings] = useState({
    apiUrl: localStorage.getItem('api_url') || 'http://localhost:8000',
    autoRefresh: localStorage.getItem('auto_refresh') === 'true',
    notifications: localStorage.getItem('notifications') !== 'false',
    username: localStorage.getItem('username') || 'Developer',
    email: localStorage.getItem('email') || 'dev@example.com',
  });

  const handleSave = () => {
    localStorage.setItem('api_url', settings.apiUrl);
    localStorage.setItem('auto_refresh', settings.autoRefresh.toString());
    localStorage.setItem('notifications', settings.notifications.toString());
    localStorage.setItem('username', settings.username);
    localStorage.setItem('email', settings.email);
    alert('Settings saved successfully!');
  };

  const handleReset = () => {
    const defaultSettings = {
      apiUrl: 'http://localhost:8000',
      autoRefresh: true,
      notifications: true,
      username: 'Developer',
      email: 'dev@example.com',
    };
    setSettings(defaultSettings);
  };

  const clearHistory = () => {
    if (window.confirm('Are you sure you want to clear all research history?')) {
      localStorage.removeItem('research_history');
      alert('Research history cleared!');
    }
  };

  return (
    <div className="max-w-4xl mx-auto p-6 space-y-8">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
      >
        <h1 className="text-3xl font-bold text-white mb-2">Settings</h1>
        <p className="text-gray-400">Configure your application preferences</p>
      </motion.div>

      {/* API Configuration */}
      <Card>
        <div className="flex items-center gap-3 mb-4">
          <Database className="w-5 h-5 text-primary-500" />
          <h3 className="text-xl font-semibold text-white">API Configuration</h3>
        </div>
        <div className="space-y-4">
          <Input
            label="API Base URL"
            value={settings.apiUrl}
            onChange={(e) => setSettings({...settings, apiUrl: e.target.value})}
            placeholder="http://localhost:8000"
          />
          <div className="flex items-center gap-2">
            <input
              type="checkbox"
              id="autoRefresh"
              checked={settings.autoRefresh}
              onChange={(e) => setSettings({...settings, autoRefresh: e.target.checked})}
              className="rounded"
            />
            <label htmlFor="autoRefresh" className="text-gray-300">
              Auto-refresh research progress
            </label>
          </div>
        </div>
      </Card>

      {/* User Profile */}
      <Card>
        <div className="flex items-center gap-3 mb-4">
          <User className="w-5 h-5 text-secondary-500" />
          <h3 className="text-xl font-semibold text-white">User Profile</h3>
        </div>
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <Input
            label="Username"
            value={settings.username}
            onChange={(e) => setSettings({...settings, username: e.target.value})}
          />
          <Input
            label="Email"
            type="email"
            value={settings.email}
            onChange={(e) => setSettings({...settings, email: e.target.value})}
          />
        </div>
      </Card>

      {/* Notifications */}
      <Card>
        <div className="flex items-center gap-3 mb-4">
          <Bell className="w-5 h-5 text-success-500" />
          <h3 className="text-xl font-semibold text-white">Notifications</h3>
        </div>
        <div className="flex items-center gap-2">
          <input
            type="checkbox"
            id="notifications"
            checked={settings.notifications}
            onChange={(e) => setSettings({...settings, notifications: e.target.checked})}
            className="rounded"
          />
          <label htmlFor="notifications" className="text-gray-300">
            Enable browser notifications for research completion
          </label>
        </div>
      </Card>

      {/* Data Management */}
      <Card>
        <h3 className="text-xl font-semibold text-white mb-4">Data Management</h3>
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-white font-medium">Clear Research History</p>
              <p className="text-gray-400 text-sm">Remove all stored research sessions</p>
            </div>
            <Button variant="outline" onClick={clearHistory}>
              Clear History
            </Button>
          </div>
        </div>
      </Card>

      {/* Actions */}
      <div className="flex gap-4">
        <Button onClick={handleSave}>
          <Save className="w-4 h-4" />
          Save Settings
        </Button>
        <Button variant="outline" onClick={handleReset}>
          <RefreshCw className="w-4 h-4" />
          Reset to Defaults
        </Button>
      </div>
    </div>
  );
};