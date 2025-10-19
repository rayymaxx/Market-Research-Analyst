import React from 'react';
import { motion } from 'framer-motion';
import { 
  Brain, 
  Zap, 
  Users, 
  BarChart3, 
  ArrowRight,
  CheckCircle,
  Sparkles
} from 'lucide-react';
import { Button } from '../components/ui/Button';
import { Card } from '../components/ui/Card';
import { useNavigate } from 'react-router-dom';

const features = [
  {
    icon: Users,
    title: 'Multi-Agent Intelligence',
    description: '4 specialized AI agents work together - Research Director, Data Gatherer, Insights Specialist, Communications Expert',
  },
  {
    icon: BarChart3,
    title: 'Comprehensive Analysis',
    description: 'SWOT analysis, competitive benchmarking, market trends, strategic recommendations',
  },
  {
    icon: Brain,
    title: 'RAG-Enhanced',
    description: 'Leverages your knowledge base with 5+ documents for contextual insights',
  },
  {
    icon: Zap,
    title: 'Real-time Processing',
    description: 'Watch your research unfold with live agent activity and progress tracking',
  },
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
      <section className="relative overflow-hidden py-20 px-6">
        <div className="max-w-6xl mx-auto text-center">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
          >
            <div className="flex items-center justify-center gap-3 mb-6">
              <div className="p-3 bg-primary-500 rounded-xl">
                <Brain className="w-8 h-8 text-white" />
              </div>
              <h1 className="text-5xl font-bold text-white">
                Market Research AI
              </h1>
            </div>
            
            <h2 className="text-3xl font-bold text-white mb-6">
              AI-Powered Market Research in Minutes
            </h2>
            
            <p className="text-xl text-gray-300 mb-8 max-w-3xl mx-auto">
              Get comprehensive market analysis, competitor insights, and strategic 
              recommendations using advanced RAG-enhanced AI agents
            </p>
            
            <div className="flex items-center justify-center gap-4">
              <Button
                size="lg"
                onClick={() => navigate('/research')}
                className="text-lg px-8 py-4"
              >
                <Sparkles className="w-5 h-5" />
                Start Research
                <ArrowRight className="w-5 h-5" />
              </Button>
              
              <Button
                variant="outline"
                size="lg"
                onClick={() => navigate('/demo')}
                className="text-lg px-8 py-4"
              >
                Try Sample Research
              </Button>
            </div>
          </motion.div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20 px-6">
        <div className="max-w-6xl mx-auto">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 }}
            className="text-center mb-16"
          >
            <h3 className="text-3xl font-bold text-white mb-4">
              Powered by Advanced AI
            </h3>
            <p className="text-gray-400 text-lg">
              Enterprise-grade market intelligence at your fingertips
            </p>
          </motion.div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            {features.map((feature, index) => (
              <motion.div
                key={feature.title}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.3 + index * 0.1 }}
              >
                <Card hover className="h-full">
                  <div className="flex items-start gap-4">
                    <div className="p-3 bg-primary-500/20 rounded-lg">
                      <feature.icon className="w-6 h-6 text-primary-500" />
                    </div>
                    <div>
                      <h4 className="text-xl font-semibold text-white mb-2">
                        {feature.title}
                      </h4>
                      <p className="text-gray-400">
                        {feature.description}
                      </p>
                    </div>
                  </div>
                </Card>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Demo Section */}
      <section className="py-20 px-6 bg-dark-800/50">
        <div className="max-w-4xl mx-auto">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.4 }}
            className="text-center mb-12"
          >
            <h3 className="text-3xl font-bold text-white mb-4">
              How It Works
            </h3>
            <p className="text-gray-400 text-lg">
              Get professional market research in 3 simple steps
            </p>
          </motion.div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {steps.map((step, index) => (
              <motion.div
                key={step}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.5 + index * 0.1 }}
                className="text-center"
              >
                <div className="w-12 h-12 bg-primary-500 rounded-full flex items-center justify-center text-white font-bold text-lg mx-auto mb-4">
                  {index + 1}
                </div>
                <h4 className="text-lg font-semibold text-white mb-2">
                  {step}
                </h4>
                {index < steps.length - 1 && (
                  <ArrowRight className="w-6 h-6 text-gray-400 mx-auto mt-4 hidden md:block" />
                )}
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Trust Section */}
      <section className="py-20 px-6">
        <div className="max-w-4xl mx-auto text-center">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.6 }}
          >
            <h3 className="text-3xl font-bold text-white mb-8">
              Enterprise-Grade Intelligence
            </h3>
            
            <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-12">
              <div className="flex items-center justify-center gap-2">
                <CheckCircle className="w-5 h-5 text-success-500" />
                <span className="text-gray-300">Powered by Gemini 2.0</span>
              </div>
              <div className="flex items-center justify-center gap-2">
                <CheckCircle className="w-5 h-5 text-success-500" />
                <span className="text-gray-300">Enterprise-grade RAG</span>
              </div>
              <div className="flex items-center justify-center gap-2">
                <CheckCircle className="w-5 h-5 text-success-500" />
                <span className="text-gray-300">No setup required</span>
              </div>
            </div>

            <Button
              size="lg"
              onClick={() => navigate('/research')}
              className="text-lg px-8 py-4"
            >
              <Sparkles className="w-5 h-5" />
              Get Started Now
            </Button>
          </motion.div>
        </div>
      </section>
    </div>
  );
};