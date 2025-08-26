import React, { createContext, ReactNode, useContext, useState } from 'react';
import type { JobAssessment } from '../types/assessment';

interface AssessmentContextType {
  isDrawerOpen: boolean;
  selectedAssessment: JobAssessment | null;
  openAssessmentDrawer: (assessment: JobAssessment) => void;
  closeAssessmentDrawer: () => void;
}

const AssessmentContext = createContext<AssessmentContextType | undefined>(
  undefined
);

interface AssessmentProviderProps {
  children: ReactNode;
}

export const AssessmentProvider: React.FC<AssessmentProviderProps> = ({
  children,
}) => {
  const [isDrawerOpen, setIsDrawerOpen] = useState(false);
  const [selectedAssessment, setSelectedAssessment] =
    useState<JobAssessment | null>(null);

  const openAssessmentDrawer = (assessment: JobAssessment) => {
    setSelectedAssessment(assessment);
    setIsDrawerOpen(true);
  };

  const closeAssessmentDrawer = () => {
    setIsDrawerOpen(false);
    setSelectedAssessment(null);
  };

  const value: AssessmentContextType = {
    isDrawerOpen,
    selectedAssessment,
    openAssessmentDrawer,
    closeAssessmentDrawer,
  };

  return (
    <AssessmentContext.Provider value={value}>
      {children}
    </AssessmentContext.Provider>
  );
};

export const useAssessment = (): AssessmentContextType => {
  const context = useContext(AssessmentContext);
  if (context === undefined) {
    throw new Error('useAssessment must be used within an AssessmentProvider');
  }
  return context;
};
