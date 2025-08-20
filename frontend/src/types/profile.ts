export type ProfileEntryType = "experience" | "education" | "personal";

export interface ProfileEntry {
  id: string;
  type: ProfileEntryType;
  title?: string;
  organization?: string;
  start_date?: string;
  end_date?: string;
  key_notes: string[];
}

export interface ProfileEntryCreate {
  type: ProfileEntryType;
  title?: string;
  organization?: string;
  start_date?: string;
  end_date?: string;
  key_notes: string[];
}

export interface ProfileResponse {
  entries: ProfileEntry[];
}

// Profile Generation types
export interface ProfileGenerationResponse {
  message: string;
  entries: ProfileEntry[];
} 