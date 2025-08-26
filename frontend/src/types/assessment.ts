export interface JobAssessment {
  id: number;
  opportunity_id: number;
  profile_id: number;
  profile_version: number;
  summary_of_fit: string;
  fit_score: number; // 1-7
  recommendation: string;
  created_at: string;
  updated_at: string;
  assessment_date: string;
}

export interface JobAssessmentCreate {
  opportunity_id: number;
  profile_id: number;
}
