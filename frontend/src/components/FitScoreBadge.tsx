import React from 'react';
import type { JobAssessment } from '../types/assessment';

interface FitScoreBadgeProps {
  assessment?: JobAssessment | null;
  currentProfileVersion?: number;
  onClick?: () => void;
  className?: string;
}

export const FitScoreBadge: React.FC<FitScoreBadgeProps> = ({
  assessment,
  currentProfileVersion = 1,
  onClick,
  className = '',
}) => {
  const isOutdated =
    assessment && assessment.profile_version !== currentProfileVersion;

  const getScoreColor = (score: number) => {
    if (score >= 6) return 'bg-green-100 text-green-800 border-green-200';
    if (score >= 4) return 'bg-yellow-100 text-yellow-800 border-yellow-200';
    return 'bg-red-100 text-red-800 border-red-200';
  };

  const getScoreLabel = (score: number) => {
    if (score >= 6) return 'Excellent';
    if (score >= 4) return 'Good';
    return 'Poor';
  };

  if (!assessment) {
    return (
      <div
        className={`inline-flex items-center px-3 py-1 rounded-full text-sm font-medium border bg-gray-100 text-gray-500 border-gray-200 cursor-pointer hover:bg-gray-200 transition-colors ${className}`}
        onClick={onClick}
      >
        —
      </div>
    );
  }

  return (
    <div className="relative">
      <div
        className={`inline-flex items-center px-3 py-1 rounded-full text-sm font-medium border cursor-pointer hover:opacity-80 transition-opacity ${getScoreColor(
          assessment.fit_score
        )} ${className}`}
        onClick={onClick}
      >
        {assessment.fit_score}/7
        {isOutdated && (
          <div className="absolute -top-1 -right-1 w-3 h-3 bg-red-500 rounded-full border-2 border-white"></div>
        )}
      </div>
      {isOutdated && (
        <div className="absolute -top-1 -right-1 w-3 h-3 bg-red-500 rounded-full border-2 border-white"></div>
      )}
    </div>
  );
};
