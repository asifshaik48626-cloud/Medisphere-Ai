import React from 'react'
import { AlertOctagon, AlertTriangle, ShieldCheck, HelpCircle } from 'lucide-react'

interface UrgencyBadgeProps {
  level: string
}

export const UrgencyBadge: React.FC<UrgencyBadgeProps> = ({ level }) => {
  const normalizedLevel = level.toLowerCase()

  let styles = 'bg-neutralGray-200 text-neutralGray-700 border-neutralGray-300'
  let label = 'Unknown'
  let Icon = HelpCircle

  if (normalizedLevel === 'emergency') {
    styles = 'bg-red-50 text-danger border-red-200'
    label = 'Emergency Care Needed'
    Icon = AlertOctagon
  } else if (normalizedLevel === 'urgent') {
    styles = 'bg-orange-50 text-warning border-orange-200'
    label = 'Urgent Consultation Recommended'
    Icon = AlertTriangle
  } else if (normalizedLevel === 'same-day') {
    styles = 'bg-amber-50 text-amber-700 border-amber-200'
    label = 'Same-Day Clinical Review'
    Icon = AlertTriangle
  } else if (normalizedLevel === 'routine') {
    styles = 'bg-brand-100 text-brand-700 border-brand-500 border-opacity-30'
    label = 'Routine Consultation'
    Icon = ShieldCheck
  } else if (normalizedLevel === 'monitor') {
    styles = 'bg-green-50 text-success border-green-200'
    label = 'Self-Care & Monitoring'
    Icon = ShieldCheck
  }

  return (
    <div className={`flex items-center space-x-2 border px-3 py-1.5 rounded-full text-sm font-semibold inline-flex ${styles}`}>
      <Icon className="h-4.5 w-4.5" />
      <span>{label}</span>
    </div>
  )
}
