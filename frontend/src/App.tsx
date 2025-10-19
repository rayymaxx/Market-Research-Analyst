import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { Header } from './components/layout/Header';
import { Sidebar } from './components/layout/Sidebar';
import { LandingPage } from './pages/LandingPage';
import { DashboardPage } from './pages/DashboardPage';
import { ResearchPage } from './pages/ResearchPage';
import { KnowledgePage } from './pages/KnowledgePage';
import { HistoryPage } from './pages/HistoryPage';
import { ReportsPage } from './pages/ReportsPage';
import { AnalyticsPage } from './pages/AnalyticsPage';
import { SettingsPage } from './pages/SettingsPage';

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: 1,
      refetchOnWindowFocus: false,
    },
  },
});

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <Router>
        <div className="min-h-screen bg-dark-900 text-white">
          <Routes>
            {/* Landing page without sidebar */}
            <Route path="/" element={<LandingPage />} />
            
            {/* App pages with sidebar layout */}
            <Route
              path="/*"
              element={
                <div className="flex h-screen">
                  <div className="hidden lg:block">
                    <Sidebar />
                  </div>
                  <div className="flex-1 flex flex-col overflow-hidden">
                    <Header />
                    <main className="flex-1 overflow-y-auto">
                      <Routes>
                        <Route path="/dashboard" element={<DashboardPage />} />
                        <Route path="/research" element={<ResearchPage />} />
                        <Route path="/knowledge" element={<KnowledgePage />} />
                        <Route path="/history" element={<HistoryPage />} />
                        <Route path="/reports" element={<ReportsPage />} />
                        <Route path="/analytics" element={<AnalyticsPage />} />
                        <Route path="/settings" element={<SettingsPage />} />
                      </Routes>
                    </main>
                  </div>
                </div>
              }
            />
          </Routes>
        </div>
      </Router>
    </QueryClientProvider>
  );
}

export default App;