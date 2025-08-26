import axios from 'axios';
import type { JobAssessment, JobAssessmentCreate } from '../types/assessment';

const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

export const assessmentApi = {
  // Create or update assessment for an opportunity
  createAssessment: async (
    data: JobAssessmentCreate
  ): Promise<JobAssessment> => {
    const response = await axios.post(
      `${API_BASE_URL}/assessments/opportunities/${data.opportunity_id}/assess?profile_id=${data.profile_id}`
    );
    return response.data;
  },

  // Get single assessment for an opportunity
  getOpportunityAssessment: async (
    opportunityId: number
  ): Promise<JobAssessment> => {
    const response = await axios.get(
      `${API_BASE_URL}/assessments/opportunities/${opportunityId}`
    );
    return response.data;
  },

  // Get all assessments for a profile
  getProfileAssessments: async (
    profileId: number
  ): Promise<JobAssessment[]> => {
    const response = await axios.get(
      `${API_BASE_URL}/assessments/profiles/${profileId}`
    );
    return response.data;
  },

  // Delete an assessment
  deleteAssessment: async (assessmentId: number): Promise<void> => {
    await axios.delete(`${API_BASE_URL}/assessments/${assessmentId}`);
  },
};
