import React, { useEffect, useState } from 'react';
import { profileApi } from '../api/profile';
import { AddProfileEntryDialog } from '../components/AddProfileEntryDialog';
import { GenerateProfileDialog } from '../components/GenerateProfileDialog';
import { ProfileEntryCard } from '../components/ProfileEntryCard';
import { Card, CardContent } from '../components/ui/card';
import type { ProfileEntry, ProfileEntryCreate, ProfileEntryType } from '../types/profile';

const ENTRY_TYPE_LABELS: Record<ProfileEntryType, string> = {
  experience: 'Experience',
  education: 'Education',
  personal: 'Personal'
};

export const Profile: React.FC = () => {
  const [entries, setEntries] = useState<ProfileEntry[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchProfile();
  }, []);

  const fetchProfile = async () => {
    try {
      setLoading(true);
      const response = await profileApi.getProfile();
      setEntries(response.entries);
    } catch (error) {
      console.error('Error fetching profile:', error);
      setError('Failed to load profile');
    } finally {
      setLoading(false);
    }
  };

  const handleAddEntry = async (entryData: ProfileEntryCreate) => {
    try {
      const newEntry = await profileApi.createEntry(entryData);
      setEntries(prev => [...prev, newEntry]);
    } catch (error) {
      console.error('Error adding entry:', error);
      throw error;
    }
  };

  const handleUpdateEntry = async (id: string, entryData: ProfileEntryCreate) => {
    try {
      const updatedEntry = await profileApi.updateEntry(id, entryData);
      setEntries(prev => prev.map(entry => entry.id === id ? updatedEntry : entry));
    } catch (error) {
      console.error('Error updating entry:', error);
      throw error;
    }
  };

  const handleDeleteEntry = async (id: string) => {
    try {
      await profileApi.deleteEntry(id);
      setEntries(prev => prev.filter(entry => entry.id !== id));
    } catch (error) {
      console.error('Error deleting entry:', error);
      throw error;
    }
  };

  const handleGenerateProfile = async (formData: FormData) => {
    try {
      const response = await profileApi.generateProfile(formData);
      // Refresh the profile to show the newly generated entries
      await fetchProfile();
      // You could also show a success message here
      console.log('Profile generated successfully:', response.message);
    } catch (error) {
      console.error('Error generating profile:', error);
      throw error;
    }
  };

  const groupEntriesByType = () => {
    const grouped: Record<ProfileEntryType, ProfileEntry[]> = {
      experience: [],
      education: [],
      personal: []
    };

    entries.forEach(entry => {
      grouped[entry.type].push(entry);
    });

    return grouped;
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-lg">Loading profile...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-lg text-red-600">{error}</div>
      </div>
    );
  }

  const groupedEntries = groupEntriesByType();

  return (
    <div className="p-8">
      <div className="max-w-6xl mx-auto">
        <div className="flex items-center justify-between mb-8">
          <h1 className="text-3xl font-bold">Profile</h1>
          <div className="flex gap-3">
            <GenerateProfileDialog onGenerate={handleGenerateProfile} />
            <AddProfileEntryDialog onAdd={handleAddEntry} />
          </div>
        </div>

        {entries.length === 0 ? (
          <Card>
            <CardContent className="flex flex-col items-center justify-center py-12">
              <p className="text-muted-foreground text-lg mb-4">
                No profile entries yet. Generate a new profile or add your first entry to get started!
              </p>
              <div className="flex gap-3">
                <GenerateProfileDialog onGenerate={handleGenerateProfile} />
                <AddProfileEntryDialog onAdd={handleAddEntry} />
              </div>
            </CardContent>
          </Card>
        ) : (
          <div className="space-y-8">
            {Object.entries(groupedEntries).map(([type, typeEntries]) => {
              if (typeEntries.length === 0) return null;
              
              return (
                <div key={type}>
                  <h2 className="text-2xl font-semibold mb-4">
                    {ENTRY_TYPE_LABELS[type as ProfileEntryType]}
                  </h2>
                  <div className="space-y-4">
                    {typeEntries.map(entry => (
                      <ProfileEntryCard
                        key={entry.id}
                        entry={entry}
                        onUpdate={handleUpdateEntry}
                        onDelete={handleDeleteEntry}
                      />
                    ))}
                  </div>
                </div>
              );
            })}
          </div>
        )}
      </div>
    </div>
  );
}; 