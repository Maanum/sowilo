import { AlertTriangle, RefreshCw, X } from 'lucide-react';
import React, { useState } from 'react';
import { assessmentApi } from '../api/assessment';
import { useAssessment } from '../contexts/AssessmentContext';
import type { JobAssessment } from '../types/assessment';
import { Button } from './ui/button';

interface AssessmentDrawerProps {
  currentProfileVersion?: number;
  onAssessmentUpdated?: (assessment: JobAssessment) => void;
}

export const AssessmentDrawer: React.FC<AssessmentDrawerProps> = ({
  currentProfileVersion = 1,
  onAssessmentUpdated,
}) => {
  const { isDrawerOpen, selectedAssessment, closeAssessmentDrawer } =
    useAssessment();
  const [isRegenerating, setIsRegenerating] = useState(false);

  if (!isDrawerOpen || !selectedAssessment) {
    return null;
  }

  const isOutdated =
    selectedAssessment.profile_version !== currentProfileVersion;

  const getScoreColor = (score: number) => {
    if (score >= 6) return 'text-green-600';
    if (score >= 4) return 'text-yellow-600';
    return 'text-red-600';
  };

  const getScoreLabel = (score: number) => {
    if (score >= 6) return 'Excellent Fit';
    if (score >= 4) return 'Good Fit';
    return 'Poor Fit';
  };

  const handleRegenerate = async () => {
    if (!selectedAssessment) return;

    setIsRegenerating(true);
    try {
      const updatedAssessment = await assessmentApi.createAssessment({
        opportunity_id: selectedAssessment.opportunity_id,
        profile_id: selectedAssessment.profile_id,
      });

      if (onAssessmentUpdated) {
        onAssessmentUpdated(updatedAssessment);
      }
    } catch (error) {
      console.error('Failed to regenerate assessment:', error);
    } finally {
      setIsRegenerating(false);
    }
  };

  return (
    <>
      {/* Backdrop */}
      <div
        className="fixed inset-0 bg-black bg-opacity-50 z-40"
        onClick={closeAssessmentDrawer}
      />

      {/* Drawer */}
      <div className="fixed right-0 top-0 h-full w-96 bg-white shadow-xl z-50 transform transition-transform duration-300 ease-in-out">
        <div className="flex flex-col h-full">
          {/* Header */}
          <div className="flex items-center justify-between p-6 border-b">
            <h2 className="text-xl font-semibold text-gray-900">
              Job Assessment
            </h2>
            <Button
              variant="ghost"
              size="icon"
              onClick={closeAssessmentDrawer}
              className="h-8 w-8"
            >
              <X className="h-4 w-4" />
            </Button>
          </div>

          {/* Content */}
          <div className="flex-1 overflow-y-auto p-6">
            {/* Outdated Warning */}
            {isOutdated && (
              <div className="mb-6 p-4 bg-amber-50 border border-amber-200 rounded-lg">
                <div className="flex items-start gap-3">
                  <AlertTriangle className="h-5 w-5 text-amber-600 mt-0.5 flex-shrink-0" />
                  <div>
                    <h3 className="text-sm font-medium text-amber-800">
                      Assessment Outdated
                    </h3>
                    <p className="text-sm text-amber-700 mt-1">
                      This assessment was generated with an older version of
                      your profile. Consider regenerating it for the most
                      accurate results.
                    </p>
                  </div>
                </div>
              </div>
            )}

            {/* Fit Score */}
            <div className="text-center mb-8">
              <div
                className={`text-6xl font-bold ${getScoreColor(
                  selectedAssessment.fit_score
                )}`}
              >
                {selectedAssessment.fit_score}/7
              </div>
              <div className="text-lg font-medium text-gray-900 mt-2">
                {getScoreLabel(selectedAssessment.fit_score)}
              </div>
            </div>

            {/* Summary of Fit */}
            <div className="mb-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-3">
                Summary of Fit
              </h3>
              <p className="text-gray-700 leading-relaxed">
                {selectedAssessment.summary_of_fit}
              </p>
            </div>

            {/* Recommendation */}
            <div className="mb-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-3">
                Recommendation
              </h3>
              <p className="text-gray-700 leading-relaxed">
                {selectedAssessment.recommendation}
              </p>
            </div>

            {/* Metadata */}
            <div className="border-t pt-6">
              <div className="space-y-2 text-sm text-gray-500">
                <div className="flex justify-between">
                  <span>Assessment Date:</span>
                  <span>
                    {new Date(
                      selectedAssessment.assessment_date
                    ).toLocaleDateString()}
                  </span>
                </div>
                <div className="flex justify-between">
                  <span>Profile Version:</span>
                  <span>{selectedAssessment.profile_version}</span>
                </div>
                <div className="flex justify-between">
                  <span>Last Updated:</span>
                  <span>
                    {new Date(
                      selectedAssessment.updated_at
                    ).toLocaleDateString()}
                  </span>
                </div>
              </div>
            </div>
          </div>

          {/* Footer */}
          <div className="p-6 border-t">
            <Button
              onClick={handleRegenerate}
              disabled={isRegenerating}
              className="w-full"
              variant={isOutdated ? 'default' : 'outline'}
            >
              {isRegenerating ? (
                <span className="flex items-center gap-2">
                  <RefreshCw className="h-4 w-4 animate-spin" />
                  Regenerating...
                </span>
              ) : (
                <span className="flex items-center gap-2">
                  <RefreshCw className="h-4 w-4" />
                  Generate New Assessment
                  {isOutdated && (
                    <div className="w-2 h-2 bg-red-500 rounded-full"></div>
                  )}
                </span>
              )}
            </Button>
          </div>
        </div>
      </div>
    </>
  );
};
