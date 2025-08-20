import axios from 'axios';
import type {
  ProfileEntry,
  ProfileEntryCreate,
  ProfileGenerationResponse,
  ProfileResponse,
} from '../types/profile';

const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

export const profileApi = {
  // Get all profile entries
  getProfile: async (): Promise<ProfileResponse> => {
    const response = await axios.get(`${API_BASE_URL}/profile`);
    return response.data;
  },

  // Create a new profile entry
  createEntry: async (entry: ProfileEntryCreate): Promise<ProfileEntry> => {
    const response = await axios.post(`${API_BASE_URL}/profile/entry`, entry);
    return response.data;
  },

  // Update an existing profile entry
  updateEntry: async (
    id: string,
    entry: ProfileEntryCreate
  ): Promise<ProfileEntry> => {
    const response = await axios.put(
      `${API_BASE_URL}/profile/entry/${id}`,
      entry
    );
    return response.data;
  },

  // Delete a profile entry
  deleteEntry: async (id: string): Promise<void> => {
    await axios.delete(`${API_BASE_URL}/profile/entry/${id}`);
  },

  // Generate a new profile
  generateProfile: async (
    formData: FormData
  ): Promise<ProfileGenerationResponse> => {
    const response = await axios.post(
      `${API_BASE_URL}/profile/generate`,
      formData,
      {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      }
    );
    return response.data;
  },
};
