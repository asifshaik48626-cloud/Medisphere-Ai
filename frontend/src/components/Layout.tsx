import React from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import { LogOut, Activity, User as UserIcon } from 'lucide-react'

interface LayoutProps {
  children: React.ReactNode
}

const Layout: React.FC<LayoutProps> = ({ children }) => {
  const { user, logout } = useAuth()
  const navigate = useNavigate()

  const handleLogout = () => {
    logout()
    navigate('/')
  }

  return (
    <div className="min-h-screen bg-neutralGray-50 flex flex-col">
      {/* Top Navbar */}
      <header className="bg-brand-700 text-white shadow-md">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
          <div className="flex items-center space-x-2 cursor-pointer" onClick={() => navigate('/')}>
            <Activity className="h-8 w-8 text-brand-100" />
            <span className="text-xl font-bold tracking-tight">MediSphere AI</span>
          </div>

          <div className="flex items-center space-x-4">
            <div className="flex items-center space-x-2 text-sm bg-brand-500 bg-opacity-30 px-3 py-1.5 rounded-full border border-brand-100 border-opacity-20">
              <UserIcon className="h-4 w-4 text-brand-100" />
              <span className="font-semibold uppercase tracking-wider text-xs">
                {user?.role || 'User'} Dashboard
              </span>
            </div>

            <button 
              onClick={handleLogout}
              className="flex items-center space-x-1.5 bg-transparent hover:bg-brand-500 hover:bg-opacity-20 text-white border border-transparent hover:border-brand-100 hover:border-opacity-30 px-3 py-1.5 rounded-lg text-sm transition-all duration-150"
            >
              <LogOut className="h-4 w-4" />
              <span>Logout</span>
            </button>
          </div>
        </div>
      </header>

      {/* Main Content Area */}
      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {children}
      </main>

      {/* Footer */}
      <footer className="bg-white border-t border-neutralGray-200 py-6 text-center text-sm text-neutralGray-500">
        &copy; {new Date().getFullYear()} MediSphere AI. For research and clinical decision assistance only.
      </footer>
    </div>
  )
}

export default Layout
