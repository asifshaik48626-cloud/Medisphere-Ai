import React, { useState } from 'react'
import Layout from '../components/Layout'
import ThreeColumnResults from '../components/ThreeColumnResults'
import { UrgencyBadge } from '../components/UrgencyBadge'
import { MessageSquare, Mic, AlertCircle, FilePlus, ChevronRight, Check } from 'lucide-react'

// Question lists
const FEVER_QUESTIONS = [
  { code: 'fever_temp', text: 'What is your current body temperature in degrees (F or C) if measured?' },
  { code: 'fever_red_flags', text: 'Do you have a stiff neck, severe headache, confusion, or difficulty breathing?' },
  { code: 'fever_duration', text: 'How many days has the fever lasted?' }
]

const HEADACHE_QUESTIONS = [
  { code: 'headache_thunderclap', text: 'Did this headache start suddenly and reach maximum severe intensity within one minute?' },
  { code: 'headache_red_flags', text: 'Do you have neck stiffness, fever, confusion, numbness, or slurred speech?' },
  { code: 'headache_location', text: 'Where is the pain located, and how would you describe it?' }
]

const PatientDashboard: React.FC = () => {
  const [inIntake, setInIntake] = useState(false)
  const [complaint, setComplaint] = useState('')
  const [inputMode, setInputMode] = useState<'text' | 'voice'>('text')
  
  // Intake state
  const [questions, setQuestions] = useState<any[]>([])
  const [currentQIndex, setCurrentQIndex] = useState(0)
  const [answers, setAnswers] = useState<Record<string, string>>({})
  const [currentAnswer, setCurrentAnswer] = useState('')
  
  // Results state
  const [showResults, setShowResults] = useState(false)
  const [urgencyLevel, setUrgencyLevel] = useState('monitor')
  const [blocked, setBlocked] = useState(false)
  const [escalationMsg, setEscalationMsg] = useState('')
  const [patientReport, setPatientReport] = useState<any>({
    exercises: [], remedies: [], medications: []
  })

  const startIntake = () => {
    if (!complaint.trim()) return
    
    setInIntake(true)
    setCurrentQIndex(0)
    setAnswers({})
    setCurrentAnswer('')
    
    // Choose questionnaire
    const compLower = complaint.toLowerCase()
    if (compLower.includes('fever')) {
      setQuestions(FEVER_QUESTIONS)
    } else if (compLower.includes('headache')) {
      setQuestions(HEADACHE_QUESTIONS)
    } else {
      setQuestions([
        { code: 'general_severity', text: 'How severe is the pain/discomfort on a scale of 1 to 10?' },
        { code: 'general_duration', text: 'How long have you been experiencing these symptoms?' }
      ])
    }
  }

  const handleNextQuestion = () => {
    const currentQ = questions[currentQIndex]
    const updatedAnswers = { ...answers, [currentQ.code]: currentAnswer }
    setAnswers(updatedAnswers)
    setCurrentAnswer('')

    if (currentQIndex < questions.length - 1) {
      setCurrentQIndex(currentQIndex + 1)
    } else {
      // Completed - evaluate safety
      evaluateSafety(updatedAnswers)
    }
  }

  const evaluateSafety = (allAnswers: Record<string, string>) => {
    setInIntake(false)
    setShowResults(true)
    
    const complaintLower = complaint.toLowerCase()
    
    // 1. Check Emergency Rules (Chest Pain, Thunderclap Headache, or Fever + Stiff neck)
    const feverStiffNeck = allAnswers['fever_red_flags']?.toLowerCase() || ''
    const thunderclap = allAnswers['headache_thunderclap']?.toLowerCase() || ''
    const headacheRedFlags = allAnswers['headache_red_flags']?.toLowerCase() || ''
    
    if (
      complaintLower.includes('chest pain') || 
      complaintLower.includes('breath') ||
      thunderclap.includes('yes') || 
      feverStiffNeck.includes('yes') || 
      feverStiffNeck.includes('neck') ||
      feverStiffNeck.includes('stiff') ||
      headacheRedFlags.includes('yes') ||
      headacheRedFlags.includes('neck') ||
      headacheRedFlags.includes('stiff')
    ) {
      setUrgencyLevel('emergency')
      setBlocked(True)
      setEscalationMsg("EMERGENCY WARNING: Critical symptoms found (potential cardiac, stroke, or severe systemic warnings). Please contact immediate emergency medical service.")
      return
    }

    // 2. Urgent Rules
    const tempAns = allAnswers['fever_temp'] || ''
    const daysAns = allAnswers['fever_duration'] || ''
    const isHighTemp = tempAns.includes('10') || tempAns.includes('39') || tempAns.includes('40')
    const isHighDays = daysAns.includes('5') || daysAns.includes('6') || daysAns.includes('7')
    
    if (isHighTemp || isHighDays || complaintLower.includes('severe')) {
      setUrgencyLevel('urgent')
      setBlocked(false)
      setEscalationMsg("URGENT WARNING: Moderate-to-high symptoms found. We recommend seeking clinical review today.")
      setPatientReport({
        exercises: [],
        remedies: [
          { id: '1', name: 'Herbal ginger tea infusion', traditional_use: 'Supports digestive and thermal comfort', evidence_level: 'Moderate' }
        ],
        medications: [
          { id: '1', generic_name: 'Paracetamol', medicine_class: 'Analgesics / Antipyretics', otc_or_prescription: 'otc', status: 'awaiting_pharmacist_review' }
        ]
      })
      return
    }

    // 3. Normal / Monitor
    setUrgencyLevel('monitor')
    setBlocked(false)
    setEscalationMsg("Recommendation: Continue monitoring symptoms and practice self-care.")
    setPatientReport({
      exercises: [
        { id: '1', name: 'Gentle neck stretches', description: 'Gently rotate neck clockwise and counter-clockwise.', difficulty: 'Beginner', repetitions: 5, reason: 'Relieve tension.' }
      ],
      remedies: [
        { id: '1', name: 'Herbal ginger tea infusion', traditional_use: 'Supports digestive and thermal comfort', evidence_level: 'Moderate' },
        { id: '2', name: 'Peppermint oil vapor', traditional_use: 'Supports cranial pressure relief', evidence_level: 'Moderate' }
      ],
      medications: [
        { id: '1', generic_name: 'Paracetamol', medicine_class: 'Analgesics / Antipyretics', otc_or_prescription: 'otc', status: 'approved' }
      ]
    })
  }

  return (
    <Layout>
      <div className="space-y-8">
        <div>
          <h2 className="text-3xl font-extrabold tracking-tight text-neutralGray-950 font-sans">Patient Portal</h2>
          <p className="text-sm text-neutralGray-500 mt-1">Submit assessments, upload medical sheets, and track care plans</p>
        </div>

        {/* 1. START NEW ASSESSMENT */}
        {!inIntake && !showResults && (
          <div className="bg-white border border-neutralGray-200 rounded-3xl p-8 shadow-sm max-w-3xl">
            <h3 className="text-xl font-bold text-neutralGray-900 tracking-tight flex items-center space-x-2">
              <FilePlus className="h-6 w-6 text-brand-500" />
              <span>Symptom Intake Assessment</span>
            </h3>
            
            <div className="mt-6 space-y-4">
              <div>
                <label className="block text-xs font-bold text-neutralGray-500 uppercase tracking-wider mb-2">Input Mode</label>
                <div className="flex space-x-2">
                  <button 
                    onClick={() => setInputMode('text')}
                    className={`flex items-center space-x-1.5 px-4 py-2 rounded-xl text-sm font-semibold border transition-all duration-150 ${inputMode === 'text' ? 'bg-brand-100 border-brand-500 text-brand-700' : 'bg-white border-neutralGray-200 text-neutralGray-500'}`}
                  >
                    <MessageSquare className="h-4 w-4" />
                    <span>Text Description</span>
                  </button>
                  <button 
                    onClick={() => setInputMode('voice')}
                    className={`flex items-center space-x-1.5 px-4 py-2 rounded-xl text-sm font-semibold border transition-all duration-150 ${inputMode === 'voice' ? 'bg-brand-100 border-brand-500 text-brand-700' : 'bg-white border-neutralGray-200 text-neutralGray-500'}`}
                  >
                    <Mic className="h-4 w-4" />
                    <span>Voice Input</span>
                  </button>
                </div>
              </div>

              <div>
                <label className="block text-xs font-bold text-neutralGray-500 uppercase tracking-wider mb-2">What symptoms are you experiencing?</label>
                {inputMode === 'text' ? (
                  <textarea 
                    value={complaint}
                    onChange={e => setComplaint(e.target.value)}
                    placeholder="Describe your symptoms in detail (e.g., I have had a high fever for three days, or I have chest tightness)..."
                    className="w-full bg-white border border-neutralGray-200 rounded-2xl p-4 text-sm focus:outline-none focus:border-brand-500 min-h-32 transition-all"
                  />
                ) : (
                  <div className="border-2 border-dashed border-neutralGray-200 rounded-2xl p-8 flex flex-col items-center justify-center text-center space-y-3 bg-neutralGray-50">
                    <button className="bg-brand-700 hover:bg-brand-500 text-white p-5 rounded-full shadow-lg transition-transform duration-150 hover:scale-105">
                      <Mic className="h-8 w-8" />
                    </button>
                    <span className="text-xs text-neutralGray-400 font-medium">Click to allow microphone permissions & speak</span>
                    <input 
                      type="text" 
                      value={complaint}
                      onChange={e => setComplaint(e.target.value)}
                      placeholder="Or type here to simulate spoken voice transcription..."
                      className="w-full bg-white border border-neutralGray-200 rounded-xl px-4 py-2 text-sm focus:outline-none focus:border-brand-500 text-center max-w-md"
                    />
                  </div>
                )}
              </div>

              <button 
                onClick={startIntake}
                className="bg-brand-700 hover:bg-brand-500 text-white font-semibold px-6 py-3 rounded-xl shadow-md transition-colors duration-150 flex items-center space-x-1"
              >
                <span>Start Assessment</span>
                <ChevronRight className="h-5 w-5" />
              </button>
            </div>
          </div>
        )}

        {/* 2. QUESTIONNAIRE SEQUENCE */}
        {inIntake && (
          <div className="bg-white border border-neutralGray-200 rounded-3xl p-8 shadow-sm max-w-2xl">
            <div className="flex items-center justify-between border-b border-neutralGray-100 pb-4 mb-6">
              <span className="text-xs font-bold text-brand-700 uppercase tracking-widest bg-brand-100 px-3 py-1 rounded-full">
                Question {currentQIndex + 1} of {questions.length}
              </span>
              <span className="text-xs text-neutralGray-400 font-medium">Symptom Intake Sequence</span>
            </div>

            <div className="space-y-6">
              <h4 className="text-lg sm:text-xl font-bold text-neutralGray-900 leading-tight">
                {questions[currentQIndex]?.text}
              </h4>

              <input 
                type="text"
                value={currentAnswer}
                onChange={e => setCurrentAnswer(e.target.value)}
                placeholder="Type your answer here..."
                className="w-full bg-white border border-neutralGray-200 rounded-xl px-4 py-3 text-sm focus:outline-none focus:border-brand-500"
                onKeyDown={e => { if (e.key === 'Enter') handleNextQuestion(); }}
                autoFocus
              />

              <div className="flex justify-between items-center pt-4">
                <button 
                  onClick={() => setInIntake(false)}
                  className="text-neutralGray-500 hover:underline text-sm font-semibold"
                >
                  Cancel Session
                </button>
                <button 
                  onClick={handleNextQuestion}
                  className="bg-brand-700 hover:bg-brand-500 text-white font-semibold px-5 py-2.5 rounded-xl shadow transition-colors duration-150"
                >
                  {currentQIndex === questions.length - 1 ? 'Complete Assessment' : 'Next Question'}
                </button>
              </div>
            </div>
          </div>
        )}

        {/* 3. ASSESSMENT TRIAGE RESULTS */}
        {showResults && (
          <div className="space-y-6">
            <div className="bg-white border border-neutralGray-200 rounded-3xl p-8 shadow-sm">
              <div className="flex flex-col sm:flex-row sm:items-center justify-between border-b border-neutralGray-100 pb-5 gap-4">
                <div>
                  <h3 className="text-xl font-bold text-neutralGray-900 tracking-tight">AI Understanding Triage</h3>
                  <p className="text-xs text-neutralGray-400 mt-0.5">Summary of Safety Engine evaluation results</p>
                </div>
                <UrgencyBadge level={urgencyLevel} />
              </div>

              <div className="mt-6 space-y-4">
                <div className="flex items-start space-x-2 text-sm text-neutralGray-600 bg-neutralGray-50 p-4 rounded-xl border border-neutralGray-200">
                  <AlertCircle className="h-5 w-5 text-neutralGray-500 flex-shrink-0 mt-0.5" />
                  <div>
                    <span className="font-bold text-neutralGray-900">Clinical Triage Assessment</span>
                    <p className="mt-1 leading-relaxed">{escalationMsg}</p>
                  </div>
                </div>

                <div className="grid grid-cols-2 gap-4 text-sm mt-4">
                  <div className="border border-neutralGray-200 p-4 rounded-2xl">
                    <span className="text-xs font-bold text-neutralGray-400 uppercase tracking-wide">Main Symptom</span>
                    <p className="font-semibold text-neutralGray-900 mt-1 capitalize">{complaint}</p>
                  </div>
                  <div className="border border-neutralGray-200 p-4 rounded-2xl">
                    <span className="text-xs font-bold text-neutralGray-400 uppercase tracking-wide">Triage Status</span>
                    <p className="font-semibold text-neutralGray-900 mt-1 capitalize">{urgencyLevel}</p>
                  </div>
                </div>
              </div>

              <div className="mt-8 flex space-x-3">
                <button 
                  onClick={() => setShowResults(false)}
                  className="bg-brand-700 hover:bg-brand-500 text-white font-semibold px-5 py-2.5 rounded-xl shadow transition-colors"
                >
                  New Assessment
                </button>
              </div>
            </div>

            {/* Three Column care recommendations */}
            <ThreeColumnResults 
              blocked={blocked}
              exercises={patientReport.exercises}
              remedies={patientReport.remedies}
              medications={patientReport.medications}
            />
          </div>
        )}
      </div>
    </Layout>
  )
}

export default PatientDashboard
