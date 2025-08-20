import { useState, useEffect } from 'react'
import { BrowserRouter as Router, Routes, Route, Link, useLocation } from 'react-router-dom'
import { Moon, Sun, Briefcase, User } from 'lucide-react'
import { Button } from './components/ui/button'
import { Opportunities } from './pages/Opportunities'
import { Profile } from './pages/Profile'

function App() {
  const [isDark, setIsDark] = useState(false)

  useEffect(() => {
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

  return (
    <Router>
      <div className="min-h-screen bg-background">
        <div className="flex">
          {/* Sidebar */}
          <Sidebar toggleTheme={toggleTheme} isDark={isDark} />
          
          {/* Main Content */}
          <div className="flex-1">
            <Routes>
              <Route path="/" element={<Opportunities />} />
              <Route path="/opportunities" element={<Opportunities />} />
              <Route path="/profile" element={<Profile />} />
            </Routes>
          </div>
        </div>
      </div>
    </Router>
  )
}

interface SidebarProps {
  toggleTheme: () => void
  isDark: boolean
}

function Sidebar({ toggleTheme, isDark }: SidebarProps) {
  const location = useLocation()

  const navItems = [
    { path: '/opportunities', label: 'Opportunities', icon: Briefcase },
    { path: '/profile', label: 'Profile', icon: User },
  ]

  return (
    <div className="w-64 bg-card border-r border-border min-h-screen p-4">
      <div className="flex items-center justify-between mb-8">
        <h1 className="text-xl font-bold">Sowilo</h1>
        <Button
          variant="outline"
          size="icon"
          onClick={toggleTheme}
          className="h-8 w-8"
        >
          {isDark ? <Sun className="h-4 w-4" /> : <Moon className="h-4 w-4" />}
        </Button>
      </div>
      
      <nav className="space-y-2">
        {navItems.map((item) => {
          const Icon = item.icon
          const isActive = location.pathname === item.path
          
          return (
            <Link
              key={item.path}
              to={item.path}
              className={`flex items-center gap-3 px-3 py-2 rounded-md text-sm font-medium transition-colors ${
                isActive
                  ? 'bg-primary text-primary-foreground'
                  : 'text-muted-foreground hover:text-foreground hover:bg-accent'
              }`}
            >
              <Icon className="h-4 w-4" />
              {item.label}
            </Link>
          )
        })}
      </nav>
    </div>
  )
}

export default App
