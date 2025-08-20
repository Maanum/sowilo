import React, { useState } from 'react';
import { Dialog, DialogContent, DialogDescription, DialogFooter, DialogHeader, DialogTitle, DialogTrigger } from './ui/dialog';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Label } from './ui/label';
import { Plus, X } from 'lucide-react';
import type { ProfileEntryCreate, ProfileEntryType } from '../types/profile';

interface AddProfileEntryDialogProps {
  onAdd: (entry: ProfileEntryCreate) => Promise<void>;
}

const ENTRY_TYPE_OPTIONS: { value: ProfileEntryType; label: string }[] = [
  { value: 'experience', label: 'Experience' },
  { value: 'education', label: 'Education' },
  { value: 'personal', label: 'Personal' }
];

export const AddProfileEntryDialog: React.FC<AddProfileEntryDialogProps> = ({ onAdd }) => {
  const [isOpen, setIsOpen] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [formData, setFormData] = useState<ProfileEntryCreate>({
    type: 'experience',
    title: '',
    organization: '',
    start_date: '',
    end_date: '',
    key_notes: ['']
  });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    
    try {
      // Filter out empty key notes
      const filteredKeyNotes = formData.key_notes.filter(note => note.trim() !== '');
      
      await onAdd({
        ...formData,
        key_notes: filteredKeyNotes
      });
      
      // Reset form and close dialog
      setFormData({
        type: 'experience',
        title: '',
        organization: '',
        start_date: '',
        end_date: '',
        key_notes: ['']
      });
      setIsOpen(false);
    } catch (error) {
      console.error('Error adding entry:', error);
    } finally {
      setIsLoading(false);
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

  const handleOpenChange = (open: boolean) => {
    setIsOpen(open);
    if (!open) {
      // Reset form when closing
      setFormData({
        type: 'experience',
        title: '',
        organization: '',
        start_date: '',
        end_date: '',
        key_notes: ['']
      });
    }
  };

  return (
    <Dialog open={isOpen} onOpenChange={handleOpenChange}>
      <DialogTrigger asChild>
        <Button>
          <Plus className="h-4 w-4 mr-2" />
          Add Entry
        </Button>
      </DialogTrigger>
      <DialogContent className="max-w-2xl max-h-[90vh] overflow-y-auto">
        <DialogHeader>
          <DialogTitle>Add Profile Entry</DialogTitle>
          <DialogDescription>
            Add a new experience, education, or personal entry to your profile.
          </DialogDescription>
        </DialogHeader>
        
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <Label htmlFor="type">Type</Label>
            <select
              id="type"
              value={formData.type}
              onChange={(e) => setFormData(prev => ({ ...prev, type: e.target.value as ProfileEntryType }))}
              className="w-full p-2 border border-gray-300 rounded-md dark:border-gray-600 dark:bg-gray-800"
            >
              {ENTRY_TYPE_OPTIONS.map(option => (
                <option key={option.value} value={option.value}>
                  {option.label}
                </option>
              ))}
            </select>
          </div>

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
                  {formData.key_notes.length > 1 && (
                    <Button
                      type="button"
                      variant="outline"
                      size="sm"
                      onClick={() => removeKeyNote(index)}
                      className="h-10 w-10 p-0"
                    >
                      <X className="h-4 w-4" />
                    </Button>
                  )}
                </div>
              ))}
            </div>
          </div>

          <DialogFooter>
            <Button
              type="button"
              variant="outline"
              onClick={() => setIsOpen(false)}
              disabled={isLoading}
            >
              Cancel
            </Button>
            <Button type="submit" disabled={isLoading}>
              {isLoading ? 'Adding...' : 'Add Entry'}
            </Button>
          </DialogFooter>
        </form>
      </DialogContent>
    </Dialog>
  );
}; 