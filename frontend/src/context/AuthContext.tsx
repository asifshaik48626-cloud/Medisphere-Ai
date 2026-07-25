import React, { createContext, useContext, useState, useEffect } from 'react'

interface User {
  id: string
  email?: string
  phone?: string
  role: string
  status: string
}

interface AuthContextType {
  token: string | null
  user: User | null
  login: (token: str, role: str) => void
  logout: () => void
  isAuthenticated: boolean
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [token, setToken] = useState<string | null>(localStorage.getItem('token'))
  const [user, setUser] = useState<User | null>(null)

  useEffect(() => {
    if (token) {
      // Decode simple base64 JWT payload mock for UI purposes
      try {
        const payload = JSON.parse(atob(token.split('.')[1]))
        setUser({
          id: payload.sub,
          role: payload.role,
          status: 'active'
        })
      } catch (e) {
        console.error("Token decoding failed:", e)
        logout()
      }
    } else {
      setUser(null)
    }
  }, [token])

  const login = (newToken: string, role: string) => {
    localStorage.setItem('token', newToken)
    localStorage.setItem('role', role)
    setToken(newToken)
  }

  const logout = () => {
    localStorage.removeItem('token')
    localStorage.removeItem('role')
    setToken(null)
    setUser(null)
  }

  return (
    <AuthContext.Provider value={{
      token,
      user,
      login,
      logout,
      isAuthenticated: !!token
    }}>
      {children}
    </AuthContext.Provider>
  )
}

export const useAuth = () => {
  const context = useContext(AuthContext)
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider')
  }
  return context
}
