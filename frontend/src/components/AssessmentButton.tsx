import React, { useState } from 'react';
import { assessmentApi } from '../api/assessment';
import type { JobAssessment } from '../types/assessment';

interface Props {
  opportunityId: number;
  profileId: number;
  onAssessmentCreated?: (assessment: JobAssessment) => void;
  disabled?: boolean;
  className?: string;
}

export const AssessmentButton: React.FC<Props> = ({
  opportunityId,
  profileId,
  onAssessmentCreated,
  disabled = false,
  className = '',
}) => {
  const [loading, setLoading] = useState(false);

  const handleCreateAssessment = async () => {
    if (loading || disabled) return;

    setLoading(true);
    try {
      const assessment = await assessmentApi.createAssessment({
        opportunity_id: opportunityId,
        profile_id: profileId,
      });
      onAssessmentCreated?.(assessment);
    } catch (error) {
      console.error('Failed to create assessment:', error);
      // Add toast notification here
    } finally {
      setLoading(false);
    }
  };

  return (
    <button
      onClick={handleCreateAssessment}
      disabled={loading || disabled}
      className={`
        inline-flex items-center gap-2 px-4 py-2 
        bg-blue-600 hover:bg-blue-700 disabled:bg-gray-400
        text-white font-medium rounded-lg
        transition-colors duration-200
        ${className}
      `}
    >
      {loading ? (
        <>
          <svg className="animate-spin h-4 w-4" fill="none" viewBox="0 0 24 24">
            <circle
              className="opacity-25"
              cx="12"
              cy="12"
              r="10"
              stroke="currentColor"
              strokeWidth="4"
            />
            <path
              className="opacity-75"
              fill="currentColor"
              d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
            />
          </svg>
          Assessing...
        </>
      ) : (
        <>
          <svg
            className="w-4 h-4"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth="2"
              d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4"
            />
          </svg>
          Generate Assessment
        </>
      )}
    </button>
  );
};
