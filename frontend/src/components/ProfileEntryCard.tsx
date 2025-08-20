import React, { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Label } from './ui/label';
import { Trash2, Edit, Save, X } from 'lucide-react';
import type { ProfileEntry, ProfileEntryCreate, ProfileEntryType } from '../types/profile';

interface ProfileEntryCardProps {
  entry: ProfileEntry;
  onUpdate: (id: string, data: ProfileEntryCreate) => Promise<void>;
  onDelete: (id: string) => Promise<void>;
}

const ENTRY_TYPE_LABELS: Record<ProfileEntryType, string> = {
  experience: 'Experience',
  education: 'Education',
  personal: 'Personal'
};

export const ProfileEntryCard: React.FC<ProfileEntryCardProps> = ({
  entry,
  onUpdate,
  onDelete
}) => {
  const [isEditing, setIsEditing] = useState(false);
  const [formData, setFormData] = useState<ProfileEntryCreate>({
    type: entry.type,
    title: entry.title || '',
    organization: entry.organization || '',
    start_date: entry.start_date || '',
    end_date: entry.end_date || '',
    key_notes: [...entry.key_notes]
  });
  const [isLoading, setIsLoading] = useState(false);

  const handleSave = async () => {
    setIsLoading(true);
    try {
      await onUpdate(entry.id, formData);
      setIsEditing(false);
    } catch (error) {
      console.error('Error updating entry:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleCancel = () => {
    setFormData({
      type: entry.type,
      title: entry.title || '',
      organization: entry.organization || '',
      start_date: entry.start_date || '',
      end_date: entry.end_date || '',
      key_notes: [...entry.key_notes]
    });
    setIsEditing(false);
  };

  const handleDelete = async () => {
    if (window.confirm('Are you sure you want to delete this entry?')) {
      setIsLoading(true);
      try {
        await onDelete(entry.id);
      } catch (error) {
        console.error('Error deleting entry:', error);
      } finally {
        setIsLoading(false);
      }
    }
  };

  const addKeyNote = () => {
    setFormData(prev => ({
      ...prev,
      key_notes: [...prev.key_notes, '']
    }));
  };

  const updateKeyNote = (index: number, value: string) => {
    setFormData(prev => ({
      ...prev,
      key_notes: prev.key_notes.map((note, i) => i === index ? value : note)
    }));
  };

  const removeKeyNote = (index: number) => {
    setFormData(prev => ({
      ...prev,
      key_notes: prev.key_notes.filter((_, i) => i !== index)
    }));
  };

  if (isEditing) {
    return (
      <Card className="mb-4">
        <CardHeader>
          <div className="flex items-center justify-between">
            <CardTitle className="text-sm font-medium text-muted-foreground">
              {ENTRY_TYPE_LABELS[entry.type]}
            </CardTitle>
            <div className="flex gap-2">
              <Button
                size="sm"
                onClick={handleSave}
                disabled={isLoading}
                className="h-8"
              >
                <Save className="h-4 w-4" />
              </Button>
              <Button
                size="sm"
                variant="outline"
                onClick={handleCancel}
                disabled={isLoading}
                className="h-8"
              >
                <X className="h-4 w-4" />
              </Button>
            </div>
          </div>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <Label htmlFor="title">Title</Label>
              <Input
                id="title"
                value={formData.title}
                onChange={(e) => setFormData(prev => ({ ...prev, title: e.target.value }))}
                placeholder="Enter title"
              />
            </div>
            <div>
              <Label htmlFor="organization">Organization</Label>
              <Input
                id="organization"
                value={formData.organization}
                onChange={(e) => setFormData(prev => ({ ...prev, organization: e.target.value }))}
                placeholder="Enter organization"
              />
            </div>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <Label htmlFor="start_date">Start Date</Label>
              <Input
                id="start_date"
                type="date"
                value={formData.start_date}
                onChange={(e) => setFormData(prev => ({ ...prev, start_date: e.target.value }))}
              />
            </div>
            <div>
              <Label htmlFor="end_date">End Date</Label>
              <Input
                id="end_date"
                type="date"
                value={formData.end_date}
                onChange={(e) => setFormData(prev => ({ ...prev, end_date: e.target.value }))}
              />
            </div>
          </div>

          <div>
            <div className="flex items-center justify-between mb-2">
              <Label>Key Notes</Label>
              <Button
                type="button"
                variant="outline"
                size="sm"
                onClick={addKeyNote}
                className="h-7"
              >
                Add Note
              </Button>
            </div>
            <div className="space-y-2">
              {formData.key_notes.map((note, index) => (
                <div key={index} className="flex gap-2">
                  <Input
                    value={note}
                    onChange={(e) => updateKeyNote(index, e.target.value)}
                    placeholder="Enter key note"
                  />
                  <Button
                    type="button"
                    variant="outline"
                    size="sm"
                    onClick={() => removeKeyNote(index)}
                    className="h-10 w-10 p-0"
                  >
                    <X className="h-4 w-4" />
                  </Button>
                </div>
              ))}
            </div>
          </div>
        </CardContent>
      </Card>
    );
  }

  return (
    <Card className="mb-4">
      <CardHeader>
        <div className="flex items-center justify-between">
          <CardTitle className="text-sm font-medium text-muted-foreground">
            {ENTRY_TYPE_LABELS[entry.type]}
          </CardTitle>
          <div className="flex gap-2">
            <Button
              size="sm"
              variant="outline"
              onClick={() => setIsEditing(true)}
              className="h-8"
            >
              <Edit className="h-4 w-4" />
            </Button>
            <Button
              size="sm"
              variant="outline"
              onClick={handleDelete}
              disabled={isLoading}
              className="h-8 text-red-600 hover:text-red-700"
            >
              <Trash2 className="h-4 w-4" />
            </Button>
          </div>
        </div>
      </CardHeader>
      <CardContent className="space-y-3">
        {entry.title && (
          <div>
            <h3 className="font-semibold text-lg">{entry.title}</h3>
          </div>
        )}
        
        {entry.organization && (
          <div>
            <p className="text-muted-foreground">{entry.organization}</p>
          </div>
        )}
        
        {(entry.start_date || entry.end_date) && (
          <div className="text-sm text-muted-foreground">
            {entry.start_date && entry.end_date 
              ? `${entry.start_date} - ${entry.end_date}`
              : entry.start_date 
                ? `Started ${entry.start_date}`
                : `Ended ${entry.end_date}`
            }
          </div>
        )}
        
        {entry.key_notes.length > 0 && (
          <div>
            <ul className="list-disc list-inside space-y-1 text-sm">
              {entry.key_notes.map((note, index) => (
                <li key={index}>{note}</li>
              ))}
            </ul>
          </div>
        )}
      </CardContent>
    </Card>
  );
}; 