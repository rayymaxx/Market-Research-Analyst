export interface ResearchRequest {
  research_topic: string;
  research_request: string;
  user_id?: string;
}

export interface TaskProgress {
  task_name: string;
  status: 'waiting' | 'running' | 'completed' | 'failed';
  agent: string;
  start_time?: string;
  end_time?: string;
  tools_used: string[];
  output?: string;
}

export interface ResearchProgress {
  current_phase: string;
  completed_tasks: string[];
  active_task?: string;
  tasks: TaskProgress[];
  progress_percentage: number;
}

export interface ResearchResponse {
  research_id: string;
  status: 'pending' | 'running' | 'completed' | 'failed';
  result?: string;
  progress?: ResearchProgress;
  error?: string;
  created_at: string;
  completed_at?: string;
}

export interface KnowledgeStats {
  total_documents: number;
  company_profiles: number;
  industry_reports: number;
  market_data: number;
  user_preferences: number;
  last_updated: string;
}

export interface UploadResponse {
  message: string;
  file_path: string;
  size: number;
  processed: boolean;
}

export interface UserProfile {
  user_id: string;
  username: string;
  email?: string;
  created_at: string;
}

export interface ResearchHistoryItem {
  research_id: string;
  research_topic: string;
  status: 'pending' | 'running' | 'completed' | 'failed';
  created_at: string;
  completed_at?: string;
}

export interface ApiError {
  detail: string;
  status_code: number;
}