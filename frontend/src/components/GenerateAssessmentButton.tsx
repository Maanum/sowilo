import { RefreshCw } from 'lucide-react';
import React, { useState } from 'react';
import { assessmentApi } from '../api/assessment';
import type { JobAssessment } from '../types/assessment';
import { Button } from './ui/button';

interface GenerateAssessmentButtonProps {
  opportunityId: number;
  profileId?: number;
  onAssessmentCreated?: (assessment: JobAssessment) => void;
  className?: string;
  variant?:
    | 'default'
    | 'outline'
    | 'secondary'
    | 'ghost'
    | 'link'
    | 'destructive';
  size?: 'default' | 'sm' | 'lg' | 'icon';
}

export const GenerateAssessmentButton: React.FC<
  GenerateAssessmentButtonProps
> = ({
  opportunityId,
  profileId = 1, // Default profile ID
  onAssessmentCreated,
  className = '',
  variant = 'outline',
  size = 'sm',
}) => {
  const [isGenerating, setIsGenerating] = useState(false);

  const handleGenerate = async () => {
    setIsGenerating(true);
    try {
      const assessment = await assessmentApi.createAssessment({
        opportunity_id: opportunityId,
        profile_id: profileId,
      });

      if (onAssessmentCreated) {
        onAssessmentCreated(assessment);
      }
    } catch (error) {
      console.error('Failed to generate assessment:', error);
      // You could add toast notification here
    } finally {
      setIsGenerating(false);
    }
  };

  return (
    <Button
      onClick={handleGenerate}
      disabled={isGenerating}
      variant={variant}
      size={size}
      className={className}
    >
      {isGenerating ? (
        <span className="flex items-center gap-2">
          <RefreshCw className="h-4 w-4 animate-spin" />
          Generating...
        </span>
      ) : (
        <span className="flex items-center gap-2">
          <RefreshCw className="h-4 w-4" />
          Generate Assessment
        </span>
      )}
    </Button>
  );
};
