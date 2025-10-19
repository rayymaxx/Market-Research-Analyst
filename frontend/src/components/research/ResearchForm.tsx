import React from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { motion } from 'framer-motion';
import { Search, Sparkles } from 'lucide-react';
import { Button } from '../ui/Button';
import { Input } from '../ui/Input';
import { Card } from '../ui/Card';
import { useResearchStore } from '../../store/useResearchStore';

const researchSchema = z.object({
  research_topic: z.string().min(3, 'Topic must be at least 3 characters'),
  research_request: z.string().min(10, 'Request must be at least 10 characters'),
});

type ResearchFormData = z.infer<typeof researchSchema>;

const sampleTopics = [
  'Electric vehicle charging infrastructure',
  'AI-powered healthcare diagnostics',
  'Sustainable packaging solutions',
  'Remote work productivity tools',
];

export const ResearchForm: React.FC = () => {
  const { startResearch, isLoading } = useResearchStore();
  
  const {
    register,
    handleSubmit,
    setValue,
    formState: { errors },
  } = useForm<ResearchFormData>({
    resolver: zodResolver(researchSchema),
  });

  const onSubmit = async (data: ResearchFormData) => {
    await startResearch(data);
  };

  const fillSample = (topic: string) => {
    setValue('research_topic', topic);
    setValue('research_request', `Analyze the competitive landscape, market trends, and growth opportunities in the ${topic} market`);
  };

  return (
    <Card className="max-w-2xl mx-auto">
      <div className="text-center mb-8">
        <div className="flex items-center justify-center gap-2 mb-4">
          <Search className="w-8 h-8 text-primary-500" />
          <h2 className="text-2xl font-bold text-white">Start New Research</h2>
        </div>
        <p className="text-gray-400">
          Let our AI agents conduct comprehensive market research for you
        </p>
      </div>

      <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
        <Input
          label="Research Topic"
          placeholder="e.g., Electric vehicle charging infrastructure"
          {...register('research_topic')}
          error={errors.research_topic?.message}
        />

        <div className="space-y-2">
          <label className="block text-sm font-medium text-gray-300">
            Research Request
          </label>
          <textarea
            className="input-field w-full h-32 resize-none"
            placeholder="Describe what specific insights you're looking for..."
            {...register('research_request')}
          />
          {errors.research_request && (
            <p className="text-red-400 text-sm">{errors.research_request.message}</p>
          )}
        </div>

        <div className="space-y-3">
          <p className="text-sm font-medium text-gray-300">Quick Start Templates:</p>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
            {sampleTopics.map((topic) => (
              <motion.button
                key={topic}
                type="button"
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
                onClick={() => fillSample(topic)}
                className="text-left p-3 bg-dark-700 hover:bg-dark-600 rounded-lg text-sm text-gray-300 hover:text-white transition-colors"
              >
                {topic}
              </motion.button>
            ))}
          </div>
        </div>

        <Button
          type="submit"
          size="lg"
          isLoading={isLoading}
          className="w-full"
        >
          <Sparkles className="w-5 h-5" />
          Start AI Research
        </Button>
      </form>
    </Card>
  );
};