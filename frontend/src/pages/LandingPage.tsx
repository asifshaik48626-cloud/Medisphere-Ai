import React from 'react'
import { useNavigate } from 'react-router-dom'
import { Activity, ShieldCheck, FileText, Globe, CheckCircle } from 'lucide-react'

const LandingPage: React.FC = () => {
  const navigate = useNavigate()

  return (
    <div className="min-h-screen bg-neutralGray-50 flex flex-col justify-between">
      {/* Header */}
      <nav className="bg-white border-b border-neutralGray-200 h-16 shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-full flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <Activity className="h-8 w-8 text-brand-500" />
            <span className="text-xl font-bold tracking-tight text-brand-700">MediSphere AI</span>
          </div>
          <button 
            onClick={() => navigate('/login')}
            className="bg-brand-500 hover:bg-brand-700 text-white font-medium px-5 py-2.5 rounded-xl shadow transition-colors duration-150"
          >
            Login Portal
          </button>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-16 flex-1 flex flex-col lg:flex-row items-center justify-between gap-12">
        <div className="max-w-xl space-y-6">
          <h1 className="text-4xl sm:text-5xl font-extrabold tracking-tight text-neutralGray-950 font-sans leading-tight">
            Multilingual Clinical Intelligence & <span className="text-brand-500">Doctor-Assisted</span> Guidance
          </h1>
          <p className="text-neutralGray-500 text-lg sm:text-xl leading-relaxed">
            MediSphere AI is a clinician decision-support and patient-guidance platform. We structure symptom reports, flag clinical emergency warnings deterministically, and provide evidence-linked summaries reviewed by medical professionals.
          </p>
          <div className="flex flex-wrap gap-4 pt-4">
            <button 
              onClick={() => navigate('/login')}
              className="bg-brand-700 hover:bg-brand-500 text-white font-semibold px-6 py-3 rounded-xl shadow-lg transition-colors duration-150"
            >
              Start Symptom Assessment
            </button>
            <button 
              onClick={() => navigate('/login')}
              className="bg-white hover:bg-neutralGray-50 text-neutralGray-700 border border-neutralGray-200 font-semibold px-6 py-3 rounded-xl shadow-sm transition-colors duration-150"
            >
              Doctor Workspace
            </button>
          </div>
        </div>
        
        {/* Features Card List */}
        <div className="w-full lg:max-w-md bg-white border border-neutralGray-200 rounded-3xl p-8 shadow-md space-y-6">
          <h3 className="text-xl font-bold text-neutralGray-900 tracking-tight">Core Safety Standards</h3>
          <div className="space-y-4">
            <div className="flex items-start space-x-3">
              <ShieldCheck className="h-6 w-6 text-success-600 flex-shrink-0 mt-0.5" />
              <div>
                <h4 className="font-semibold text-sm text-neutralGray-900">Deterministic Safety Engine</h4>
                <p className="text-xs text-neutralGray-500 mt-0.5">Emergency signals and red flags bypass AI to prevent delayed urgent care.</p>
              </div>
            </div>
            <div className="flex items-start space-x-3">
              <FileText className="h-6 w-6 text-brand-500 flex-shrink-0 mt-0.5" />
              <div>
                <h4 className="font-semibold text-sm text-neutralGray-900">Three-Column Care Recommendations</h4>
                <p className="text-xs text-neutralGray-500 mt-0.5">Exercises, complementary wellness, and medicines are strictly structured.</p>
              </div>
            </div>
            <div className="flex items-start space-x-3">
              <Globe className="h-6 w-6 text-customBlue-600 flex-shrink-0 mt-0.5" />
              <div>
                <h4 className="font-semibold text-sm text-neutralGray-900">Verified Multilingual Access</h4>
                <p className="text-xs text-neutralGray-500 mt-0.5">Patients can record or text descriptions in their local languages.</p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Disclaimers & Safety Footer */}
      <section className="bg-white border-t border-neutralGray-200 py-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="bg-amber-50 border border-amber-200 p-6 rounded-2xl">
            <h4 className="text-sm font-bold text-warning-600 tracking-wide uppercase">Important Medical Disclaimer</h4>
            <p className="text-xs text-amber-800 leading-relaxed mt-2">
              MediSphere AI is a decision assistance utility for educational purposes. It does not replace doctors, confirm diagnoses independently, prescribe medications automatically, or offer treatment guarantees. If you are experiencing symptoms of a medical emergency (such as severe chest pain, shortness of breath, or sudden severe numbness), please contact your local emergency services immediately.
            </p>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-neutralGray-950 text-neutralGray-500 py-8 text-center text-xs">
        &copy; {new Date().getFullYear()} MediSphere AI. All Rights Reserved. Built with safety and trust.
      </footer>
    </div>
  )
}

export default LandingPage
