import { useState, useEffect } from 'react'
import axios from 'axios'
import { Moon, Sun, Plus, Trash2, ExternalLink } from 'lucide-react'
import { Button } from './components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './components/ui/card'
import { Input } from './components/ui/input'
import { Label } from './components/ui/label'
import { Dialog, DialogContent, DialogDescription, DialogFooter, DialogHeader, DialogTitle, DialogTrigger } from './components/ui/dialog'

const API_BASE_URL = 'http://localhost:8000'

const STATUS_OPTIONS = [
  'Applied',
  'Screening',
  'Rejected',
  'Did Not Apply',
  'Interviewing',
  'To Apply',
]

type Status = typeof STATUS_OPTIONS[number]

interface Opportunity {
  id: number
  title: string
  company: string
  level: string | null
  min_salary: number | null
  max_salary: number | null
  posting_link: string | null
  resume_link: string | null
  cover_letter_link: string | null
  status: Status
}

interface FormData {
  title: string
  company: string
  level: string
  min_salary: string
  max_salary: string
  posting_link: string
  resume_link: string
  cover_letter_link: string
  status: Status
}

function App() {
  const [opportunities, setOpportunities] = useState<Opportunity[]>([])
  const [formData, setFormData] = useState<FormData>({
    title: '',
    company: '',
    level: '',
    min_salary: '',
    max_salary: '',
    posting_link: '',
    resume_link: '',
    cover_letter_link: '',
    status: 'To Apply',
  })
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [isDark, setIsDark] = useState(false)
  const [isDialogOpen, setIsDialogOpen] = useState(false)
  const [modalMode, setModalMode] = useState<'url' | 'manual'>('url')
  const [urlInput, setUrlInput] = useState('')
  const [enriching, setEnriching] = useState(false)

  useEffect(() => {
    fetchOpportunities()
    // Check for saved theme preference
    const savedTheme = localStorage.getItem('theme')
    if (savedTheme === 'dark' || (!savedTheme && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
      setIsDark(true)
      document.documentElement.classList.add('dark')
    }
  }, [])

  const toggleTheme = () => {
    setIsDark(!isDark)
    if (isDark) {
      document.documentElement.classList.remove('dark')
      localStorage.setItem('theme', 'light')
    } else {
      document.documentElement.classList.add('dark')
      localStorage.setItem('theme', 'dark')
    }
  }

  const fetchOpportunities = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/opportunities`)
      setOpportunities(response.data)
    } catch (error) {
      console.error('Error fetching opportunities:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target
    setFormData(prev => ({
      ...prev,
      [name]: value
    }))
  }

  const handleModeToggle = () => {
    setModalMode((prev) => (prev === 'url' ? 'manual' : 'url'))
    setFormData({
      title: '',
      company: '',
      level: '',
      min_salary: '',
      max_salary: '',
      posting_link: '',
      resume_link: '',
      cover_letter_link: '',
      status: 'To Apply',
    })
    setUrlInput('')
    setError('')
  }

  const handleUrlInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setUrlInput(e.target.value)
  }

  const handleUrlSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError('')
    if (!urlInput.trim()) {
      setError('Please enter a job posting URL.')
      return
    }
    setEnriching(true)
    try {
      const response = await axios.post(`${API_BASE_URL}/opportunities/from-link`, { link: urlInput })
      setOpportunities((prev) => [...prev, response.data])
      setUrlInput('')
      setIsDialogOpen(false)
    } catch (error) {
      setError('Failed to enrich opportunity from link. Please try again.')
    } finally {
      setEnriching(false)
    }
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError('')
    
    try {
      const cleanedData = {
        title: formData.title,
        company: formData.company,
        level: formData.level || null,
        min_salary: formData.min_salary ? parseInt(formData.min_salary) : null,
        max_salary: formData.max_salary ? parseInt(formData.max_salary) : null,
        posting_link: formData.posting_link || null,
        resume_link: formData.resume_link || null,
        cover_letter_link: formData.cover_letter_link || null,
        status: formData.status || 'To Apply',
      }
      
      const response = await axios.post(`${API_BASE_URL}/opportunities`, cleanedData)
      setOpportunities(prev => [...prev, response.data])
      setFormData({
        title: '',
        company: '',
        level: '',
        min_salary: '',
        max_salary: '',
        posting_link: '',
        resume_link: '',
        cover_letter_link: '',
        status: 'To Apply',
      })
      setIsDialogOpen(false)
    } catch (error) {
      console.error('Error creating opportunity:', error)
      setError('Failed to create opportunity. Please try again.')
    }
  }

  const handleDelete = async (id: number) => {
    if (window.confirm('Are you sure you want to delete this opportunity?')) {
      try {
        await axios.delete(`${API_BASE_URL}/opportunities/${id}`)
        setOpportunities(prev => prev.filter(opp => opp.id !== id))
      } catch (error) {
        console.error('Error deleting opportunity:', error)
      }
    }
  }

  const formatSalary = (min: number | null, max: number | null) => {
    if (min && max) {
      return `$${min.toLocaleString()} - $${max.toLocaleString()}`
    } else if (min) {
      return `$${min.toLocaleString()}+`
    } else if (max) {
      return `Up to $${max.toLocaleString()}`
    }
    return 'Not specified'
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary mx-auto mb-4"></div>
          <p className="text-muted-foreground">Loading opportunities...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-background">
      <div className="container mx-auto px-4 py-8 max-w-4xl">
        {/* Header */}
        <div className="flex justify-between items-center mb-8">
          <div>
            <h1 className="text-3xl font-bold text-foreground">Job Opportunities Tracker</h1>
            <p className="text-muted-foreground mt-2">Manage your job applications and opportunities</p>
          </div>
          <div className="flex items-center gap-4">
            <Button
              variant="outline"
              size="icon"
              onClick={toggleTheme}
              className="h-10 w-10"
            >
              {isDark ? <Sun className="h-4 w-4" /> : <Moon className="h-4 w-4" />}
            </Button>
            <Dialog open={isDialogOpen} onOpenChange={setIsDialogOpen}>
              <DialogTrigger asChild>
                <Button>
                  <Plus className="h-4 w-4 mr-2" />
                  New Opportunity
                </Button>
              </DialogTrigger>
              <DialogContent className="sm:max-w-[600px]">
                <DialogHeader>
                  <DialogTitle>Add New Opportunity</DialogTitle>
                  <DialogDescription>
                    {modalMode === 'url'
                      ? 'Paste a job posting URL and let us enrich the details for you.'
                      : 'Fill in the details for your new job opportunity.'}
                  </DialogDescription>
                </DialogHeader>
                <div className="flex justify-end mb-2">
                  <button
                    type="button"
                    className="text-sm text-primary underline hover:no-underline focus:outline-none"
                    onClick={handleModeToggle}
                  >
                    {modalMode === 'url' ? 'Switch to manual entry' : 'Paste a job posting URL instead'}
                  </button>
                </div>
                {modalMode === 'url' ? (
                  <form onSubmit={handleUrlSubmit} className="space-y-4">
                    <div className="space-y-2">
                      <Label htmlFor="job_url">Job Posting URL</Label>
                      <Input
                        id="job_url"
                        name="job_url"
                        type="url"
                        value={urlInput}
                        onChange={handleUrlInputChange}
                        placeholder="https://..."
                        required
                        disabled={enriching}
                      />
                    </div>
                    {error && (
                      <div className="text-sm text-destructive bg-destructive/10 p-3 rounded-md">
                        {error}
                      </div>
                    )}
                    <DialogFooter>
                      <Button type="button" variant="outline" onClick={() => setIsDialogOpen(false)} disabled={enriching}>
                        Cancel
                      </Button>
                      <Button type="submit" disabled={enriching || !urlInput.trim()}>
                        {enriching ? (
                          <span className="flex items-center gap-2">
                            <span className="animate-spin rounded-full h-4 w-4 border-b-2 border-primary"></span>
                            Enriching...
                          </span>
                        ) : (
                          'Add Opportunity'
                        )}
                      </Button>
                    </DialogFooter>
                  </form>
                ) : (
                  <form onSubmit={handleSubmit} className="space-y-4">
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      <div className="space-y-2">
                        <Label htmlFor="title">Title *</Label>
                        <Input
                          id="title"
                          name="title"
                          value={formData.title}
                          onChange={handleInputChange}
                          required
                          placeholder="e.g., Senior Software Engineer"
                        />
                      </div>
                      <div className="space-y-2">
                        <Label htmlFor="company">Company *</Label>
                        <Input
                          id="company"
                          name="company"
                          value={formData.company}
                          onChange={handleInputChange}
                          required
                          placeholder="e.g., Tech Corp"
                        />
                      </div>
                    </div>
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                      <div className="space-y-2">
                        <Label htmlFor="level">Level</Label>
                        <Input
                          id="level"
                          name="level"
                          value={formData.level}
                          onChange={handleInputChange}
                          placeholder="e.g., Senior, Junior"
                        />
                      </div>
                      <div className="space-y-2">
                        <Label htmlFor="min_salary">Min Salary</Label>
                        <Input
                          id="min_salary"
                          name="min_salary"
                          type="number"
                          value={formData.min_salary}
                          onChange={handleInputChange}
                          placeholder="e.g., 80000"
                        />
                      </div>
                      <div className="space-y-2">
                        <Label htmlFor="max_salary">Max Salary</Label>
                        <Input
                          id="max_salary"
                          name="max_salary"
                          type="number"
                          value={formData.max_salary}
                          onChange={handleInputChange}
                          placeholder="e.g., 120000"
                        />
                      </div>
                    </div>
                    <div className="space-y-2">
                      <Label htmlFor="status">Status</Label>
                      <select
                        id="status"
                        name="status"
                        value={formData.status}
                        onChange={handleInputChange}
                        className="block w-full h-10 rounded-md border border-input bg-background px-3 py-2 text-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2"
                      >
                        {STATUS_OPTIONS.map((option) => (
                          <option key={option} value={option}>{option}</option>
                        ))}
                      </select>
                    </div>
                    <div className="space-y-2">
                      <Label htmlFor="posting_link">Job Posting Link</Label>
                      <Input
                        id="posting_link"
                        name="posting_link"
                        type="url"
                        value={formData.posting_link}
                        onChange={handleInputChange}
                        placeholder="https://..."
                      />
                    </div>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      <div className="space-y-2">
                        <Label htmlFor="resume_link">Resume Link</Label>
                        <Input
                          id="resume_link"
                          name="resume_link"
                          type="url"
                          value={formData.resume_link}
                          onChange={handleInputChange}
                          placeholder="https://..."
                        />
                      </div>
                      <div className="space-y-2">
                        <Label htmlFor="cover_letter_link">Cover Letter Link</Label>
                        <Input
                          id="cover_letter_link"
                          name="cover_letter_link"
                          type="url"
                          value={formData.cover_letter_link}
                          onChange={handleInputChange}
                          placeholder="https://..."
                        />
                      </div>
                    </div>
                    {error && (
                      <div className="text-sm text-destructive bg-destructive/10 p-3 rounded-md">
                        {error}
                      </div>
                    )}
                    <DialogFooter>
                      <Button type="button" variant="outline" onClick={() => setIsDialogOpen(false)}>
                        Cancel
                      </Button>
                      <Button type="submit">Add Opportunity</Button>
                    </DialogFooter>
                  </form>
                )}
              </DialogContent>
            </Dialog>
          </div>
        </div>

        {/* Opportunities List */}
        <div className="space-y-4">
          <div className="flex justify-between items-center">
            <h2 className="text-2xl font-semibold text-foreground">
              Opportunities ({opportunities.length})
            </h2>
          </div>
          
          {opportunities.length === 0 ? (
            <Card>
              <CardContent className="flex flex-col items-center justify-center py-12">
                <div className="text-muted-foreground text-center">
                  <p className="text-lg mb-2">No opportunities yet</p>
                  <p className="text-sm">Click "New Opportunity" to add your first one!</p>
                </div>
              </CardContent>
            </Card>
          ) : (
            <div className="grid gap-4">
              {opportunities.map((opportunity) => (
                <Card key={opportunity.id} className="hover:shadow-md transition-shadow">
                  <CardHeader>
                    <div className="flex justify-between items-start">
                      <div className="flex-1">
                        <CardTitle className="text-xl">{opportunity.title}</CardTitle>
                        <CardDescription className="text-base font-medium text-foreground">
                          {opportunity.company}
                        </CardDescription>
                        <div className="mt-1">
                          <span className="inline-block px-2 py-1 text-xs rounded bg-muted text-muted-foreground">
                            {opportunity.status}
                          </span>
                        </div>
                      </div>
                      <Button
                        variant="destructive"
                        size="icon"
                        onClick={() => handleDelete(opportunity.id)}
                        className="h-8 w-8"
                      >
                        <Trash2 className="h-4 w-4" />
                      </Button>
                    </div>
                  </CardHeader>
                  <CardContent>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
                      <div>
                        <p className="text-muted-foreground">Level</p>
                        <p className="font-medium">{opportunity.level || 'Not specified'}</p>
                      </div>
                      <div>
                        <p className="text-muted-foreground">Salary Range</p>
                        <p className="font-medium">{formatSalary(opportunity.min_salary, opportunity.max_salary)}</p>
                      </div>
                    </div>
                    <div className="mt-4 flex flex-wrap gap-2">
                      {opportunity.posting_link && (
                        <Button variant="outline" size="sm" asChild>
                          <a href={opportunity.posting_link} target="_blank" rel="noopener noreferrer">
                            <ExternalLink className="h-3 w-3 mr-1" />
                            Job Posting
                          </a>
                        </Button>
                      )}
                      {opportunity.resume_link && (
                        <Button variant="outline" size="sm" asChild>
                          <a href={opportunity.resume_link} target="_blank" rel="noopener noreferrer">
                            <ExternalLink className="h-3 w-3 mr-1" />
                            Resume
                          </a>
                        </Button>
                      )}
                      {opportunity.cover_letter_link && (
                        <Button variant="outline" size="sm" asChild>
                          <a href={opportunity.cover_letter_link} target="_blank" rel="noopener noreferrer">
                            <ExternalLink className="h-3 w-3 mr-1" />
                            Cover Letter
                          </a>
                        </Button>
                      )}
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

export default App
