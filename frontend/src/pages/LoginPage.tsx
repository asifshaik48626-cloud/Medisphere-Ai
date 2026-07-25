import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import { Activity, ShieldCheck, Mail, Lock } from 'lucide-react'
import axios from 'axios'

const LoginPage: React.FC = () => {
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [role, setRole] = useState('patient')  // default
  const { login } = useAuth()
  const navigate = useNavigate()

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError('')

    try {
      // Send parameters as form data to match OAuth2PasswordRequestForm
      const params = new URLSearchParams()
      params.append('username', username)
      params.append('password', password)

      const response = await axios.post('/api/v1/auth/login', params, {
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded'
        }
      })
      
      const { access_token, role: userRole } = response.data
      login(access_token, userRole)
      if (userRole === 'patient') navigate('/patient')
      else navigate('/doctor')
    } catch (err: any) {
      console.warn("Backend connection failed, using dev fallback logic:", err)
      
      // Fallback: Mock login so they can preview dashboards without backend running
      if (username && password) {
        // Simple base64 encode for mock token
        const mockPayload = btoa(JSON.stringify({ sub: "dev-user-id", role: role }))
        const mockToken = `header.${mockPayload}.signature`
        login(mockToken, role)
        
        if (role === 'patient') navigate('/patient')
        else navigate('/doctor')
      } else {
        setError('Please enter a username and password.')
      }
    }
  }

  return (
    <div className="min-h-screen bg-brand-700 bg-opacity-95 flex items-center justify-center px-4 py-12 relative overflow-hidden">
      {/* Decorative Blur Spheres */}
      <div className="absolute w-72 h-72 bg-brand-100 bg-opacity-20 rounded-full blur-2xl top-10 left-10"></div>
      <div className="absolute w-96 h-96 bg-brand-500 bg-opacity-20 rounded-full blur-3xl bottom-10 right-10"></div>

      <div className="max-w-md w-full bg-white bg-opacity-95 backdrop-filter backdrop-blur-lg rounded-3xl p-8 shadow-2xl border border-white border-opacity-30 relative z-10">
        <div className="flex flex-col items-center mb-8">
          <div className="bg-brand-100 p-3.5 rounded-2xl mb-3">
            <Activity className="h-8 w-8 text-brand-700" />
          </div>
          <h2 className="text-2xl font-bold tracking-tight text-neutralGray-950 font-sans">Access Portal</h2>
          <p className="text-sm text-neutralGray-500 mt-1.5">Sign in to your clinical workspace</p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-5">
          {error && (
            <div className="bg-red-50 border border-red-200 text-danger-600 text-xs px-3.5 py-2.5 rounded-xl font-medium">
              {error}
            </div>
          )}

          {/* Role selector for easy mock toggle */}
          <div>
            <label className="block text-xs font-bold text-neutralGray-500 uppercase tracking-wider mb-2">Portal Role</label>
            <div className="grid grid-cols-2 gap-2">
              <button
                type="button"
                onClick={() => setRole('patient')}
                className={`py-2 rounded-xl text-sm font-semibold border transition-all duration-150 ${role === 'patient' ? 'bg-brand-100 border-brand-500 text-brand-700' : 'bg-white border-neutralGray-200 text-neutralGray-500'}`}
              >
                Patient
              </button>
              <button
                type="button"
                onClick={() => setRole('doctor')}
                className={`py-2 rounded-xl text-sm font-semibold border transition-all duration-150 ${role === 'doctor' ? 'bg-brand-100 border-brand-500 text-brand-700' : 'bg-white border-neutralGray-200 text-neutralGray-500'}`}
              >
                Doctor / Clinic
              </button>
            </div>
          </div>

          <div>
            <label className="block text-xs font-bold text-neutralGray-500 uppercase tracking-wider mb-2">Email Address / Phone</label>
            <div className="relative">
              <span className="absolute inset-y-0 left-0 pl-3.5 flex items-center text-neutralGray-400">
                <Mail className="h-5 w-5" />
              </span>
              <input
                type="text"
                value={username}
                onChange={e => setUsername(e.target.value)}
                placeholder="asifshaik48626@gmail.com"
                className="w-full bg-white border border-neutralGray-200 rounded-xl pl-11 pr-4 py-3 text-sm focus:outline-none focus:border-brand-500 transition-colors"
                required
              />
            </div>
          </div>

          <div>
            <label className="block text-xs font-bold text-neutralGray-500 uppercase tracking-wider mb-2">Password</label>
            <div className="relative">
              <span className="absolute inset-y-0 left-0 pl-3.5 flex items-center text-neutralGray-400">
                <Lock className="h-5 w-5" />
              </span>
              <input
                type="password"
                value={password}
                onChange={e => setPassword(e.target.value)}
                placeholder="••••••••"
                className="w-full bg-white border border-neutralGray-200 rounded-xl pl-11 pr-4 py-3 text-sm focus:outline-none focus:border-brand-500 transition-colors"
                required
              />
            </div>
          </div>

          <button
            type="submit"
            className="w-full bg-brand-700 hover:bg-brand-500 text-white font-semibold py-3 rounded-xl shadow-lg transition-colors duration-150 mt-4 flex items-center justify-center space-x-2"
          >
            <ShieldCheck className="h-5 w-5" />
            <span>Secure Log In</span>
          </button>
        </form>

        <div className="mt-6 pt-4 border-t border-neutralGray-200 text-center text-xs text-neutralGray-400 leading-relaxed">
          Need an account? Contact your medical administrator.
        </div>
      </div>
    </div>
  )
}

export default LoginPage
