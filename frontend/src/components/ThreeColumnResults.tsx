import React from 'react'
import { Dumbbell, Leaf, Pill, AlertOctagon, ExternalLink, HelpCircle } from 'lucide-react'

interface Exercise {
  id: string
  name: str
  description: string
  difficulty?: string
  duration_seconds?: number
  repetitions?: number
  reason?: string
}

interface Complementary {
  id: string
  name: string
  traditional_use?: string
  evidence_level?: string
  reason?: string
}

interface Medication {
  id: string
  generic_name: string
  medicine_class?: string
  otc_or_prescription: string
  purpose?: string
  status: string
}

interface ThreeColumnResultsProps {
  blocked: boolean
  exercises: Exercise[]
  remedies: Complementary[]
  medications: Medication[]
}

const ThreeColumnResults: React.FC<ThreeColumnResultsProps> = ({ blocked, exercises, remedies, medications }) => {
  if (blocked) {
    return (
      <div className="bg-red-50 border border-red-200 text-danger-600 p-6 rounded-2xl flex flex-col items-center text-center space-y-4 max-w-2xl mx-auto my-8 shadow-sm">
        <AlertOctagon className="h-16 w-16 text-danger" />
        <h3 className="text-2xl font-bold tracking-tight text-red-950">Self-Care Recommendations Blocked</h3>
        <p className="text-red-800 leading-relaxed">
          Due to triggered emergency warning flags, standard exercise, complementary remedies, and medication suggestions have been blocked for your safety. Please consult immediate emergency services.
        </p>
      </div>
    )
  }

  return (
    <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 my-8">
      {/* Column 1: Exercise and Movement */}
      <div className="bg-white border border-neutralGray-200 rounded-2xl shadow-sm hover:shadow-md transition-all duration-200 overflow-hidden flex flex-col">
        <div className="bg-brand-700 text-white p-4 flex items-center space-x-2">
          <Dumbbell className="h-6 w-6" />
          <h4 className="font-bold text-lg tracking-tight">Movement & Supportive Care</h4>
        </div>
        <div className="p-6 flex-1 flex flex-col justify-between">
          <div className="space-y-6">
            <p className="text-xs text-neutralGray-500 italic bg-neutralGray-50 p-2.5 rounded-lg border border-neutralGray-200">
              Note: Supportive movements and light exercises to improve circulation and posture under review.
            </p>
            {exercises.length === 0 ? (
              <p className="text-neutralGray-500 text-sm">No exercises currently recommended for this profile.</p>
            ) : (
              exercises.map(ex => (
                <div key={ex.id} className="border-b border-neutralGray-100 pb-4 last:border-b-0 last:pb-0">
                  <h5 className="font-bold text-neutralGray-900 text-base">{ex.name}</h5>
                  <p className="text-sm text-neutralGray-600 mt-1">{ex.description}</p>
                  {ex.reason && (
                    <div className="mt-2 text-xs text-brand-700 bg-brand-100 bg-opacity-30 px-2 py-1 rounded">
                      <strong>Reason:</strong> {ex.reason}
                    </div>
                  )}
                  <div className="mt-3 flex items-center space-x-3 text-xs text-neutralGray-500">
                    {ex.difficulty && <span className="bg-neutralGray-100 px-2 py-0.5 rounded">Diff: {ex.difficulty}</span>}
                    {ex.repetitions && <span className="bg-neutralGray-100 px-2 py-0.5 rounded">Reps: {ex.repetitions}</span>}
                  </div>
                </div>
              ))
            )}
          </div>
          <div className="mt-6 pt-4 border-t border-neutralGray-100 flex items-center justify-between text-xs text-neutralGray-500">
            <span>Reviewed by: Physiotherapist</span>
            <button className="text-brand-500 font-semibold hover:underline flex items-center space-x-1">
              <span>Save to plan</span>
            </button>
          </div>
        </div>
      </div>

      {/* Column 2: Complementary Wellness */}
      <div className="bg-white border border-neutralGray-200 rounded-2xl shadow-sm hover:shadow-md transition-all duration-200 overflow-hidden flex flex-col">
        <div className="bg-green-700 text-white p-4 flex items-center space-x-2">
          <Leaf className="h-6 w-6" />
          <h4 className="font-bold text-lg tracking-tight">Complementary Wellness</h4>
        </div>
        <div className="p-6 flex-1 flex flex-col justify-between">
          <div className="space-y-6">
            <p className="text-xs text-neutralGray-500 italic bg-neutralGray-50 p-2.5 rounded-lg border border-neutralGray-200">
              Heading: Complementary Wellness Options. Reminders: Non-guaranteed supportive botanical summaries.
            </p>
            {remedies.length === 0 ? (
              <p className="text-neutralGray-500 text-sm">No complementary remedies are recommended for this profile.</p>
            ) : (
              remedies.map(rem => (
                <div key={rem.id} className="border-b border-neutralGray-100 pb-4 last:border-b-0 last:pb-0">
                  <h5 className="font-bold text-neutralGray-900 text-base">{rem.name}</h5>
                  {rem.traditional_use && <p className="text-sm text-neutralGray-600 mt-1">{rem.traditional_use}</p>}
                  {rem.evidence_level && (
                    <span className="mt-2 inline-block text-xs bg-green-50 text-success border border-green-200 px-2.5 py-0.5 rounded-full font-medium">
                      Evidence: {rem.evidence_level}
                    </span>
                  )}
                </div>
              ))
            )}
          </div>
          <div className="mt-6 pt-4 border-t border-neutralGray-100 flex items-center justify-between text-xs text-neutralGray-500">
            <span>Reviewed by: Practitioner</span>
            <button className="text-brand-500 font-semibold hover:underline flex items-center space-x-1">
              <span>Save for discussion</span>
            </button>
          </div>
        </div>
      </div>

      {/* Column 3: Medication Information */}
      <div className="bg-white border border-neutralGray-200 rounded-2xl shadow-sm hover:shadow-md transition-all duration-200 overflow-hidden flex flex-col">
        <div className="bg-customBlue-600 text-white p-4 flex items-center space-x-2">
          <Pill className="h-6 w-6" />
          <h4 className="font-bold text-lg tracking-tight">Medication Information</h4>
        </div>
        <div className="p-6 flex-1 flex flex-col justify-between">
          <div className="space-y-6">
            <p className="text-xs text-neutralGray-500 italic bg-neutralGray-50 p-2.5 rounded-lg border border-neutralGray-200">
              Disclaimer: This is general informational data, NOT an automated prescription. Verify with a pharmacist.
            </p>
            {medications.length === 0 ? (
              <p className="text-neutralGray-500 text-sm">No generic medication profiles loaded for this symptom.</p>
            ) : (
              medications.map(med => (
                <div key={med.id} className="border-b border-neutralGray-100 pb-4 last:border-b-0 last:pb-0">
                  <h5 className="font-bold text-neutralGray-900 text-base">{med.generic_name}</h5>
                  {med.medicine_class && <p className="text-sm text-neutralGray-600 mt-1">Class: {med.medicine_class}</p>}
                  <div className="mt-2 flex items-center space-x-2 text-xs">
                    <span className={`px-2 py-0.5 rounded font-medium ${med.otc_or_prescription === 'otc' ? 'bg-green-100 text-green-800' : 'bg-blue-100 text-blue-800'}`}>
                      {med.otc_or_prescription.toUpperCase()}
                    </span>
                    <span className={`px-2 py-0.5 rounded font-medium ${med.status === 'approved' ? 'bg-brand-100 text-brand-700' : 'bg-amber-100 text-amber-800'}`}>
                      {med.status.replace('_', ' ')}
                    </span>
                  </div>
                </div>
              ))
            )}
          </div>
          <div className="mt-6 pt-4 border-t border-neutralGray-100 flex items-center justify-between text-xs text-neutralGray-500">
            <span>Reviewed by: Pharmacist</span>
            <button className="text-brand-500 font-semibold hover:underline flex items-center space-x-1">
              <span>Ask Doctor</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}

export default ThreeColumnResults
