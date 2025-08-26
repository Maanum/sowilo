import React from 'react';
import type { JobAssessment as JobAssessmentType } from '../types/assessment';

interface Props {
  assessment: JobAssessmentType;
  showOpportunity?: boolean;
  className?: string;
}

const FitScoreBadge: React.FC<{ score: number }> = ({ score }) => {
  const getScoreColor = (score: number) => {
    if (score >= 6) return 'bg-green-100 text-green-800 border-green-200';
    if (score >= 4) return 'bg-yellow-100 text-yellow-800 border-yellow-200';
    return 'bg-red-100 text-red-800 border-red-200';
  };

  const getScoreLabel = (score: number) => {
    if (score >= 6) return 'Excellent Fit';
    if (score >= 4) return 'Good Fit';
    return 'Poor Fit';
  };

  return (
    <div className="flex items-center gap-2">
      <span
        className={`px-3 py-1 rounded-full text-sm font-medium border ${getScoreColor(
          score
        )}`}
      >
        {score}/7
      </span>
      <span className="text-sm text-gray-600">{getScoreLabel(score)}</span>
    </div>
  );
};

export const JobAssessment: React.FC<Props> = ({
  assessment,
  showOpportunity = false,
  className = '',
}) => {
  return (
    <div
      className={`bg-white rounded-lg border border-gray-200 p-6 shadow-sm ${className}`}
    >
      <div className="flex justify-between items-start mb-4">
        <div>
          <h3 className="text-lg font-semibold text-gray-900">
            Job Assessment
          </h3>
          {showOpportunity && (
            <p className="text-sm text-gray-600 mt-1">
              Opportunity ID: {assessment.opportunity_id}
            </p>
          )}
        </div>
        <div className="text-right">
          <FitScoreBadge score={assessment.fit_score} />
          <p className="text-sm text-gray-500 mt-1">
            {new Date(assessment.assessment_date).toLocaleDateString()}
          </p>
        </div>
      </div>

      <div className="space-y-4">
        <div>
          <h4 className="font-medium text-gray-900 mb-2">Summary of Fit</h4>
          <p className="text-gray-700 leading-relaxed">
            {assessment.summary_of_fit}
          </p>
        </div>

        <div>
          <h4 className="font-medium text-gray-900 mb-2">Recommendation</h4>
          <p className="text-gray-700 leading-relaxed">
            {assessment.recommendation}
          </p>
        </div>

        {assessment.profile_version > 1 && (
          <div className="text-sm text-gray-500 border-t pt-3 mt-4">
            <span className="inline-flex items-center gap-1">
              <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                <path
                  fillRule="evenodd"
                  d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z"
                  clipRule="evenodd"
                />
              </svg>
              Based on profile version {assessment.profile_version}
            </span>
          </div>
        )}
      </div>
    </div>
  );
};
