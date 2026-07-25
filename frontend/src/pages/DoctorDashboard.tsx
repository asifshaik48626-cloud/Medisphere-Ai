import React, { useState } from 'react'
import Layout from '../components/Layout'
import { Check, ClipboardList, AlertOctagon, User, FileText, ChevronRight, MessageCircle } from 'lucide-react'

interface Case {
  id: string
  patientName: string
  age: number
  complaint: string
  urgency: string
  status: string
  date: string
  symptoms: string[]
}

const INITIAL_CASES: Case[] = [
  {
    id: '1',
    patientName: 'Shaik Asif',
    age: 21,
    complaint: 'Severe headache and neck stiffness',
    urgency: 'emergency',
    status: 'pending',
    date: '2026-07-26',
    symptoms: ['Headache (Severity 9)', 'Neck stiffness', 'Mild fever']
  },
  {
    id: '2',
    patientName: 'Jane Smith',
    age: 45,
    complaint: 'Fever and body pain',
    urgency: 'urgent',
    status: 'pending',
    date: '2026-07-25',
    symptoms: ['Fever (Severity 7)', 'Chills', 'Joint pain']
  },
  {
    id: '3',
    patientName: 'Robert Johnson',
    age: 62,
    complaint: 'Chronic back pain flare up',
    urgency: 'routine',
    status: 'pending',
    date: '2026-07-25',
    symptoms: ['Lower back pain (Severity 5)']
  }
]

const DoctorDashboard: React.FC = () => {
  const [cases, setCases] = useState<Case[]>(INITIAL_CASES)
  const [selectedCase, setSelectedCase] = useState<Case | null>(INITIAL_CASES[0])
  const [reviewNote, setReviewNote] = useState('')
  const [successMsg, setSuccessMsg] = useState('')

  const handleApprove = (caseId: string) => {
    setCases(cases.map(c => c.id === caseId ? { ...c, status: 'approved' } : c))
    setSuccessMsg('Care plan has been successfully approved!')
    setTimeout(() => setSuccessMsg(''), 4000)
    
    // Auto-select another if available
    const remaining = cases.filter(c => c.id !== caseId && c.status === 'pending')
    if (remaining.length > 0) {
      setSelectedCase(remaining[0])
    } else {
      setSelectedCase(null)
    }
  }

  const handleRequestChanges = (caseId: string) => {
    setCases(cases.map(c => c.id === caseId ? { ...c, status: 'changes_requested' } : c))
    setSuccessMsg('Revision requests sent successfully.')
    setTimeout(() => setSuccessMsg(''), 4000)
  }

  return (
    <Layout>
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Left Side: Cases Queue List */}
        <div className="lg:col-span-1 space-y-6">
          <div>
            <h3 className="text-xl font-bold text-neutralGray-900 tracking-tight flex items-center space-x-2">
              <ClipboardList className="h-6 w-6 text-brand-700" />
              <span>Review Queue</span>
            </h3>
            <p className="text-xs text-neutralGray-500 mt-1">Pending patient intakes awaiting approval</p>
          </div>

          <div className="space-y-4">
            {cases.filter(c => c.status === 'pending').length === 0 ? (
              <div className="bg-white border border-neutralGray-200 rounded-2xl p-6 text-center text-neutralGray-400 text-sm font-medium">
                No pending cases in review queue.
              </div>
            ) : (
              cases.filter(c => c.status === 'pending').map(c => (
                <div 
                  key={c.id}
                  onClick={() => setSelectedCase(c)}
                  className={`border rounded-2xl p-4 cursor-pointer hover:shadow transition-all duration-150 ${selectedCase?.id === c.id ? 'bg-brand-100 bg-opacity-30 border-brand-500' : 'bg-white border-neutralGray-200'}`}
                >
                  <div className="flex justify-between items-start">
                    <span className="font-bold text-neutralGray-900 text-sm">{c.patientName}</span>
                    <span className={`text-[10px] uppercase font-bold tracking-wider px-2 py-0.5 rounded-full ${c.urgency === 'emergency' ? 'bg-red-100 text-danger' : c.urgency === 'urgent' ? 'bg-orange-100 text-warning-600' : 'bg-neutralGray-100 text-neutralGray-500'}`}>
                      {c.urgency}
                    </span>
                  </div>
                  <p className="text-xs text-neutralGray-500 mt-1 truncate">{c.complaint}</p>
                  <div className="flex items-center justify-between text-[10px] text-neutralGray-400 mt-3 pt-2 border-t border-neutralGray-100">
                    <span>Age: {c.age}</span>
                    <span>{c.date}</span>
                  </div>
                </div>
              ))
            )}
          </div>
        </div>

        {/* Right Side: Selected Case Details */}
        <div className="lg:col-span-2 space-y-6">
          {successMsg && (
            <div className="bg-green-50 border border-green-200 text-success-600 text-sm font-semibold px-4 py-3 rounded-2xl flex items-center space-x-2">
              <Check className="h-5 w-5" />
              <span>{successMsg}</span>
            </div>
          )}

          {selectedCase ? (
            <div className="bg-white border border-neutralGray-200 rounded-3xl p-8 shadow-sm space-y-6">
              {/* Triage Header */}
              <div className="flex justify-between items-start border-b border-neutralGray-100 pb-5">
                <div className="flex items-center space-x-3">
                  <div className="bg-neutralGray-100 p-3 rounded-2xl text-neutralGray-600">
                    <User className="h-6 w-6" />
                  </div>
                  <div>
                    <h3 className="text-xl font-bold text-neutralGray-900 tracking-tight">{selectedCase.patientName}</h3>
                    <p className="text-xs text-neutralGray-500">Age: {selectedCase.age} | Record Reference: #{selectedCase.id}</p>
                  </div>
                </div>
                <span className={`text-xs uppercase font-bold tracking-widest px-3.5 py-1.5 rounded-full ${selectedCase.urgency === 'emergency' ? 'bg-red-50 text-danger border border-red-200' : 'bg-neutralGray-50 border border-neutralGray-200 text-neutralGray-600'}`}>
                  {selectedCase.urgency} Triage
                </span>
              </div>

              {/* Urgency Red Flags block */}
              {selectedCase.urgency === 'emergency' && (
                <div className="bg-red-50 border border-red-200 text-danger-600 p-4 rounded-xl flex items-start space-x-2.5">
                  <AlertOctagon className="h-6 w-6 text-danger flex-shrink-0" />
                  <div>
                    <span className="font-bold text-red-950">Deterministic Emergency Red Flags Found</span>
                    <p className="text-xs text-red-800 mt-0.5">Symptom details triggered diagnostic constraints. Recommended movement and complementary remedies are blocked automatically by the system.</p>
                  </div>
                </div>
              )}

              {/* Symptom list */}
              <div className="space-y-3">
                <h4 className="text-sm font-bold text-neutralGray-500 uppercase tracking-wider">Patient Timeline & Symptoms</h4>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                  {selectedCase.symptoms.map((s, idx) => (
                    <div key={idx} className="bg-neutralGray-50 border border-neutralGray-200 p-3.5 rounded-xl text-xs font-semibold text-neutralGray-800 flex items-center space-x-2">
                      <FileText className="h-4.5 w-4.5 text-neutralGray-500" />
                      <span>{s}</span>
                    </div>
                  ))}
                </div>
              </div>

              {/* Draft Clinical Notes */}
              <div className="space-y-3">
                <h4 className="text-sm font-bold text-neutralGray-500 uppercase tracking-wider flex items-center space-x-1.5">
                  <MessageCircle className="h-4.5 w-4.5" />
                  <span>Clinical Assessment Notes</span>
                </h4>
                <textarea 
                  value={reviewNote}
                  onChange={e => setReviewNote(e.target.value)}
                  placeholder="Appended observations, medication dosage adjustments, or comments to share with the care team..."
                  className="w-full bg-white border border-neutralGray-200 rounded-2xl p-4 text-xs focus:outline-none focus:border-brand-500 min-h-24 transition-colors"
                />
              </div>

              {/* Decision Action Buttons */}
              <div className="pt-4 border-t border-neutralGray-100 flex flex-wrap gap-3 justify-end">
                <button 
                  onClick={() => handleRequestChanges(selectedCase.id)}
                  className="bg-white hover:bg-neutralGray-50 text-neutralGray-600 border border-neutralGray-200 font-semibold px-5 py-2.5 rounded-xl text-sm transition-colors duration-150"
                >
                  Request Changes
                </button>
                <button 
                  onClick={() => handleApprove(selectedCase.id)}
                  className="bg-brand-700 hover:bg-brand-500 text-white font-semibold px-5 py-2.5 rounded-xl text-sm transition-colors duration-150 flex items-center space-x-1.5 shadow"
                >
                  <Check className="h-4 w-4" />
                  <span>Approve & Release</span>
                </button>
              </div>
            </div>
          ) : (
            <div className="bg-white border border-neutralGray-200 rounded-3xl p-12 text-center text-neutralGray-400 text-sm font-semibold shadow-sm">
              Select a case from the queue to start clinical review.
            </div>
          )}
        </div>
      </div>
    </Layout>
  )
}

export default DoctorDashboard
