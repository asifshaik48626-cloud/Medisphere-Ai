import React, { useState } from 'react'
import Layout from '../components/Layout'
import { Shield, Users, Activity, FileText, CheckCircle, Database, Lock, AlertTriangle } from 'lucide-react'

interface AuditLog {
  id: string
  actor: string
  action: string
  target: string
  ip: string
  timestamp: string
}

const MOCK_AUDITS: AuditLog[] = [
  { id: '1', actor: 'doctor@medisphere.com', action: 'APPROVE_CARE_PLAN', target: 'CarePlan #4521', ip: '192.168.1.45', timestamp: '2026-07-26 00:45:10' },
  { id: '2', actor: 'patient@medisphere.com', action: 'READ_HEALTH_SUMMARY', target: 'PatientProfile #882', ip: '182.54.21.198', timestamp: '2026-07-26 00:40:22' },
  { id: '3', actor: 'system-scheduler', action: 'ROTATE_SECRET_KEY', target: 'SecurityManager', ip: '127.0.0.1', timestamp: '2026-07-26 00:00:00' },
  { id: '4', actor: 'doctor@medisphere.com', action: 'READ_CLINICAL_TIMELINE', target: 'PatientProfile #882', ip: '192.168.1.45', timestamp: '2026-07-25 23:58:12' }
]

const AdminDashboard: React.FC = () => {
  const [audits] = useState<AuditLog[]>(MOCK_AUDITS)
  const [safetyEngineVersion, setSafetyEngineVersion] = useState('v1.4.0 (Active)')

  return (
    <Layout>
      <div className="space-y-8">
        <div>
          <h2 className="text-3xl font-extrabold tracking-tight text-neutralGray-950 font-sans">Admin Control Panel</h2>
          <p className="text-sm text-neutralGray-500 mt-1">Monitor system performance, evaluate safety engines, and read audit compliance logs</p>
        </div>

        {/* Stats Grid */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
          <div className="bg-white border border-neutralGray-200 p-6 rounded-2xl shadow-sm flex items-center space-x-4">
            <div className="p-3 bg-brand-100 rounded-xl text-brand-700">
              <Users className="h-6 w-6" />
            </div>
            <div>
              <span className="text-xs text-neutralGray-400 font-bold uppercase tracking-wider">Total Patients</span>
              <p className="text-2xl font-bold text-neutralGray-900 mt-0.5">1,240</p>
            </div>
          </div>

          <div className="bg-white border border-neutralGray-200 p-6 rounded-2xl shadow-sm flex items-center space-x-4">
            <div className="p-3 bg-customBlue-100 rounded-xl text-customBlue-700">
              <Activity className="h-6 w-6" />
            </div>
            <div>
              <span className="text-xs text-neutralGray-400 font-bold uppercase tracking-wider">Clinicians</span>
              <p className="text-2xl font-bold text-neutralGray-900 mt-0.5">85</p>
            </div>
          </div>

          <div className="bg-white border border-neutralGray-200 p-6 rounded-2xl shadow-sm flex items-center space-x-4">
            <div className="p-3 bg-amber-100 rounded-xl text-warning-600">
              <FileText className="h-6 w-6" />
            </div>
            <div>
              <span className="text-xs text-neutralGray-400 font-bold uppercase tracking-wider">Active Intake Sessions</span>
              <p className="text-2xl font-bold text-neutralGray-900 mt-0.5">14</p>
            </div>
          </div>

          <div className="bg-white border border-neutralGray-200 p-6 rounded-2xl shadow-sm flex items-center space-x-4">
            <div className="p-3 bg-red-100 rounded-xl text-danger-600">
              <Shield className="h-6 w-6" />
            </div>
            <div>
              <span className="text-xs text-neutralGray-400 font-bold uppercase tracking-wider">Safety Overrides Run</span>
              <p className="text-2xl font-bold text-neutralGray-900 mt-0.5">4</p>
            </div>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Audit Logs Checklist Panel */}
          <div className="lg:col-span-2 bg-white border border-neutralGray-200 rounded-3xl p-8 shadow-sm space-y-6">
            <div className="flex items-center justify-between border-b border-neutralGray-100 pb-4">
              <div>
                <h3 className="text-lg font-bold text-neutralGray-900 flex items-center space-x-2">
                  <Database className="h-5 w-5 text-neutralGray-500" />
                  <span>HIPAA Compliance Audit Logs</span>
                </h3>
                <p className="text-xs text-neutralGray-400 mt-0.5">Append-only audit record tracking clinical read/write operations</p>
              </div>
              <span className="text-[10px] font-bold text-green-700 bg-green-100 px-3 py-1 rounded-full uppercase tracking-wider flex items-center space-x-1">
                <CheckCircle className="h-3.5 w-3.5" />
                <span>Secure</span>
              </span>
            </div>

            <div className="overflow-x-auto">
              <table className="w-full text-left border-collapse text-xs">
                <thead>
                  <tr className="border-b border-neutralGray-200 text-neutralGray-400 font-bold uppercase tracking-wider">
                    <th className="pb-3">Actor</th>
                    <th className="pb-3">Action</th>
                    <th className="pb-3">Target Entity</th>
                    <th className="pb-3">Client IP</th>
                    <th className="pb-3 text-right">Timestamp</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-neutralGray-100 font-semibold text-neutralGray-700">
                  {audits.map(log => (
                    <tr key={log.id} className="hover:bg-neutralGray-50 transition-colors">
                      <td className="py-3.5 text-neutralGray-900">{log.actor}</td>
                      <td className="py-3.5">
                        <span className={`px-2 py-0.5 rounded text-[10px] uppercase font-bold tracking-wider ${log.action.includes('APPROVE') ? 'bg-green-100 text-success-600' : log.action.includes('ROTATE') ? 'bg-blue-100 text-brand-700' : 'bg-neutralGray-100 text-neutralGray-500'}`}>
                          {log.action}
                        </span>
                      </td>
                      <td className="py-3.5 font-mono text-[10px]">{log.target}</td>
                      <td className="py-3.5 text-neutralGray-400">{log.ip}</td>
                      <td className="py-3.5 text-right text-neutralGray-500">{log.timestamp}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>

          {/* Right Column: Engine Rules Configuration */}
          <div className="lg:col-span-1 space-y-6">
            <div className="bg-white border border-neutralGray-200 rounded-3xl p-8 shadow-sm space-y-4">
              <h3 className="text-lg font-bold text-neutralGray-900 flex items-center space-x-2">
                <Lock className="h-5 w-5 text-danger" />
                <span>Deterministic Rules Engine</span>
              </h3>
              
              <div className="space-y-3">
                <div className="bg-neutralGray-50 border border-neutralGray-200 p-4 rounded-2xl space-y-1">
                  <span className="text-[10px] font-bold text-neutralGray-400 uppercase tracking-wider">Engine Version</span>
                  <p className="text-sm font-bold text-neutralGray-900">{safetyEngineVersion}</p>
                </div>
                
                <div className="bg-neutralGray-50 border border-neutralGray-200 p-4 rounded-2xl space-y-1">
                  <span className="text-[10px] font-bold text-neutralGray-400 uppercase tracking-wider">Trigger Rule Count</span>
                  <p className="text-sm font-bold text-neutralGray-900">18 Deterministic Gating Rules</p>
                </div>
              </div>

              <div className="pt-4 border-t border-neutralGray-100">
                <button 
                  onClick={() => alert("Safety Engine Rule Updates require multi-clinician verification signatures.")}
                  className="w-full bg-brand-700 hover:bg-brand-500 text-white font-semibold py-2.5 rounded-xl text-xs shadow transition-colors flex items-center justify-center space-x-1.5"
                >
                  <AlertTriangle className="h-4 w-4" />
                  <span>Update Safety Parameters</span>
                </button>
              </div>
            </div>
          </div>
        </div>

      </div>
    </Layout>
  )
}

export default AdminDashboard
