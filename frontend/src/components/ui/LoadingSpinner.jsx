import React from 'react'

export default function LoadingSpinner() {
  return (
    <div className="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50">
      <div className="bg-primary-card border border-primary-border/DEFAULT rounded-xl p-6 flex flex-col items-center space-y-4">
        <div className="w-12 h-12 border-4 border-accent border-t-transparent rounded-full animate-spin"></div>
        <p className="text-primary-text-primary font-medium">Chargement...</p>
      </div>
    </div>
  )
}
