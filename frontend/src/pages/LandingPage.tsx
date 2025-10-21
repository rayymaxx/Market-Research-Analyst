import React from 'react';
import { motion } from 'framer-motion';
import { 
  Brain, 
  Zap, 
  Users, 
  BarChart3, 
  ArrowRight,
  CheckCircle,
  Sparkles,
  FileText,
  TrendingUp,
  Shield,
  Clock
} from 'lucide-react';
import { Button } from '../components/ui/Button';
import { Card } from '../components/ui/Card';
import { useNavigate } from 'react-router-dom';

const features = [
  {
    icon: Users,
    title: 'Multi-Agent Intelligence',
    description: '4 specialized AI agents collaborate: Research Director orchestrates strategy, Data Gatherer collects market intelligence, Insights Specialist performs deep analysis, and Communications Expert crafts executive reports.',
    stats: '4 AI Agents'
  },
  {
    icon: BarChart3,
    title: 'Comprehensive Analysis',
    description: 'Complete market intelligence including SWOT analysis, competitive benchmarking, market sizing, trend analysis, and strategic recommendations with actionable insights.',
    stats: '8+ Analysis Types'
  },
  {
    icon: Brain,
    title: 'RAG-Enhanced Knowledge',
    description: 'Leverages your proprietary knowledge base with document ingestion, semantic search, and contextual retrieval for personalized market insights.',
    stats: 'Unlimited Documents'
  },
  {
    icon: Zap,
    title: 'Real-time Intelligence',
    description: 'Live progress tracking with agent activity monitoring, task completion status, and real-time report generation with professional PDF export.',
    stats: 'Live Updates'
  },
];

const benefits = [
  {
    icon: Clock,
    title: 'Save 90% Time',
    description: 'Complete market research in minutes, not weeks'
  },
  {
    icon: TrendingUp,
    title: 'Professional Quality',
    description: 'Enterprise-grade reports ready for C-level presentation'
  },
  {
    icon: Shield,
    title: 'Data Security',
    description: 'Your proprietary data stays secure and private'
  },
  {
    icon: FileText,
    title: 'Export Ready',
    description: 'PDF reports with executive summaries and appendices'
  }
];

const steps = [
  'Enter your research topic',
  'Watch AI agents work',
  'Get comprehensive report',
];

export const LandingPage: React.FC = () => {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen gradient-bg">
      {/* Hero Section */}
      <section className="relative overflow-hidden py-12 sm:py-20 lg:py-32 px-4 sm:px-6">
        <div className="absolute inset-0 bg-gradient-to-br from-primary-500/10 via-transparent to-secondary-500/10" />
        <div className="max-w-7xl mx-auto text-center relative">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
          >
            <div className="flex flex-col sm:flex-row items-center justify-center gap-3 sm:gap-4 mb-6 sm:mb-8">
              <div className="p-3 sm:p-4 bg-gradient-to-br from-primary-500 to-primary-600 rounded-xl shadow-lg">
                <Brain className="w-8 h-8 sm:w-10 sm:h-10 text-white" />
              </div>
              <h1 className="text-3xl sm:text-4xl lg:text-6xl font-bold text-white leading-tight">
                Market Research AI
              </h1>
            </div>
            
            <h2 className="text-xl sm:text-2xl lg:text-4xl font-bold text-white mb-4 sm:mb-6 leading-tight">
              AI-Powered Market Intelligence
              <span className="block text-primary-400">in Minutes, Not Weeks</span>
            </h2>
            
            <p className="text-base sm:text-lg lg:text-xl text-gray-300 mb-8 sm:mb-12 max-w-4xl mx-auto leading-relaxed px-4">
              Transform your market research with 4 specialized AI agents that deliver 
              comprehensive analysis, competitor insights, and strategic recommendations 
              using enterprise-grade RAG technology.
            </p>
            
            <div className="flex flex-col sm:flex-row items-center justify-center gap-4 sm:gap-6 px-4">
              <Button
                size="lg"
                onClick={() => navigate('/research')}
                className="w-full sm:w-auto text-base sm:text-lg px-6 sm:px-8 py-3 sm:py-4 bg-gradient-to-r from-primary-500 to-primary-600 hover:from-primary-600 hover:to-primary-700 shadow-lg hover:shadow-xl transition-all duration-300"
              >
                <Sparkles className="w-5 h-5" />
                Start Research Now
                <ArrowRight className="w-5 h-5" />
              </Button>
              
              <Button
                variant="outline"
                size="lg"
                onClick={() => navigate('/dashboard')}
                className="w-full sm:w-auto text-base sm:text-lg px-6 sm:px-8 py-3 sm:py-4 border-2 border-gray-600 hover:border-primary-500 transition-all duration-300"
              >
                View Dashboard
              </Button>
            </div>
            
            <div className="mt-8 sm:mt-12 grid grid-cols-2 sm:grid-cols-4 gap-4 sm:gap-8 max-w-2xl mx-auto px-4">
              <div className="text-center">
                <div className="text-xl sm:text-2xl font-bold text-white">4</div>
                <div className="text-xs sm:text-sm text-gray-400">AI Agents</div>
              </div>
              <div className="text-center">
                <div className="text-xl sm:text-2xl font-bold text-white">90%</div>
                <div className="text-xs sm:text-sm text-gray-400">Time Saved</div>
              </div>
              <div className="text-center">
                <div className="text-xl sm:text-2xl font-bold text-white">8+</div>
                <div className="text-xs sm:text-sm text-gray-400">Analysis Types</div>
              </div>
              <div className="text-center">
                <div className="text-xl sm:text-2xl font-bold text-white">PDF</div>
                <div className="text-xs sm:text-sm text-gray-400">Export Ready</div>
              </div>
            </div>
          </motion.div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-12 sm:py-20 lg:py-32 px-4 sm:px-6 bg-dark-900/50">
        <div className="max-w-7xl mx-auto">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 }}
            className="text-center mb-12 sm:mb-16 lg:mb-20"
          >
            <h3 className="text-2xl sm:text-3xl lg:text-4xl font-bold text-white mb-4 sm:mb-6">
              Enterprise-Grade AI Intelligence
            </h3>
            <p className="text-gray-400 text-base sm:text-lg lg:text-xl max-w-3xl mx-auto leading-relaxed">
              Advanced multi-agent system with RAG technology delivers professional market research 
              that rivals traditional consulting firms
            </p>
          </motion.div>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 sm:gap-8 mb-16 sm:mb-20">
            {features.map((feature, index) => (
              <motion.div
                key={feature.title}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.3 + index * 0.1 }}
              >
                <Card hover className="h-full p-6 sm:p-8 bg-gradient-to-br from-dark-800 to-dark-900 border-dark-600 hover:border-primary-500/50 transition-all duration-300">
                  <div className="flex flex-col sm:flex-row items-start gap-4 sm:gap-6">
                    <div className="p-3 sm:p-4 bg-gradient-to-br from-primary-500/20 to-primary-600/20 rounded-xl">
                      <feature.icon className="w-6 h-6 sm:w-8 sm:h-8 text-primary-400" />
                    </div>
                    <div className="flex-1">
                      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between mb-3">
                        <h4 className="text-lg sm:text-xl font-bold text-white mb-1 sm:mb-0">
                          {feature.title}
                        </h4>
                        <span className="text-sm font-semibold text-primary-400 bg-primary-500/10 px-2 py-1 rounded-full w-fit">
                          {feature.stats}
                        </span>
                      </div>
                      <p className="text-gray-300 text-sm sm:text-base leading-relaxed">
                        {feature.description}
                      </p>
                    </div>
                  </div>
                </Card>
              </motion.div>
            ))}
          </div>
          
          {/* Benefits Grid */}
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 sm:gap-6">
            {benefits.map((benefit, index) => (
              <motion.div
                key={benefit.title}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.5 + index * 0.1 }}
                className="text-center p-4 sm:p-6 bg-dark-800/50 rounded-xl border border-dark-700 hover:border-primary-500/30 transition-all duration-300"
              >
                <div className="p-3 bg-gradient-to-br from-secondary-500/20 to-secondary-600/20 rounded-lg w-fit mx-auto mb-3">
                  <benefit.icon className="w-5 h-5 sm:w-6 sm:h-6 text-secondary-400" />
                </div>
                <h5 className="font-semibold text-white text-sm sm:text-base mb-2">
                  {benefit.title}
                </h5>
                <p className="text-gray-400 text-xs sm:text-sm">
                  {benefit.description}
                </p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* How It Works Section */}
      <section className="py-12 sm:py-20 lg:py-32 px-4 sm:px-6">
        <div className="max-w-6xl mx-auto">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.4 }}
            className="text-center mb-12 sm:mb-16"
          >
            <h3 className="text-2xl sm:text-3xl lg:text-4xl font-bold text-white mb-4 sm:mb-6">
              How It Works
            </h3>
            <p className="text-gray-400 text-base sm:text-lg lg:text-xl max-w-3xl mx-auto">
              Professional market research delivered in minutes through our intelligent AI workflow
            </p>
          </motion.div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 sm:gap-12 relative">
            {steps.map((step, index) => (
              <motion.div
                key={step}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.5 + index * 0.1 }}
                className="text-center relative"
              >
                <div className="w-16 h-16 sm:w-20 sm:h-20 bg-gradient-to-br from-primary-500 to-primary-600 rounded-full flex items-center justify-center text-white font-bold text-xl sm:text-2xl mx-auto mb-4 sm:mb-6 shadow-lg">
                  {index + 1}
                </div>
                <h4 className="text-lg sm:text-xl font-bold text-white mb-3 sm:mb-4">
                  {step}
                </h4>
                <p className="text-gray-400 text-sm sm:text-base">
                  {index === 0 && "Describe your market research needs with specific topics and objectives"}
                  {index === 1 && "Monitor real-time progress as 4 AI agents collaborate on your research"}
                  {index === 2 && "Download professional PDF reports with executive summaries and insights"}
                </p>
                {index < steps.length - 1 && (
                  <ArrowRight className="w-6 h-6 text-primary-400 absolute top-8 sm:top-10 -right-4 sm:-right-6 hidden md:block" />
                )}
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-12 sm:py-20 lg:py-32 px-4 sm:px-6 bg-gradient-to-br from-primary-900/20 via-dark-900 to-secondary-900/20">
        <div className="max-w-4xl mx-auto text-center">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.6 }}
          >
            <h3 className="text-2xl sm:text-3xl lg:text-4xl font-bold text-white mb-6 sm:mb-8">
              Ready to Transform Your Market Research?
            </h3>
            
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-6 sm:gap-8 mb-8 sm:mb-12">
              <div className="flex flex-col sm:flex-row items-center justify-center gap-2 p-4 bg-dark-800/50 rounded-lg">
                <CheckCircle className="w-5 h-5 text-success-500 flex-shrink-0" />
                <span className="text-gray-300 text-sm sm:text-base text-center sm:text-left">Powered by Gemini 2.0</span>
              </div>
              <div className="flex flex-col sm:flex-row items-center justify-center gap-2 p-4 bg-dark-800/50 rounded-lg">
                <CheckCircle className="w-5 h-5 text-success-500 flex-shrink-0" />
                <span className="text-gray-300 text-sm sm:text-base text-center sm:text-left">Enterprise RAG Technology</span>
              </div>
              <div className="flex flex-col sm:flex-row items-center justify-center gap-2 p-4 bg-dark-800/50 rounded-lg">
                <CheckCircle className="w-5 h-5 text-success-500 flex-shrink-0" />
                <span className="text-gray-300 text-sm sm:text-base text-center sm:text-left">No Setup Required</span>
              </div>
            </div>

            <div className="flex flex-col sm:flex-row items-center justify-center gap-4 sm:gap-6">
              <Button
                size="lg"
                onClick={() => navigate('/research')}
                className="w-full sm:w-auto text-base sm:text-lg px-6 sm:px-8 py-3 sm:py-4 bg-gradient-to-r from-primary-500 to-primary-600 hover:from-primary-600 hover:to-primary-700 shadow-lg hover:shadow-xl transition-all duration-300"
              >
                <Sparkles className="w-5 h-5" />
                Start Your Research
                <ArrowRight className="w-5 h-5" />
              </Button>
              
              <Button
                variant="outline"
                size="lg"
                onClick={() => navigate('/dashboard')}
                className="w-full sm:w-auto text-base sm:text-lg px-6 sm:px-8 py-3 sm:py-4"
              >
                Explore Dashboard
              </Button>
            </div>
            
            <p className="text-gray-400 text-sm sm:text-base mt-6 sm:mt-8">
              Join thousands of professionals using AI for market intelligence
            </p>
          </motion.div>
        </div>
      </section>
    </div>
  );
};