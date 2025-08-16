import React from 'react'

const ValidationBox = ({ message, companionAdvice, showCompanion, onToggleCompanion }) => {
  if (!message) return null

  return (
    <div style={{
      marginTop: '20px',
      padding: '15px',
      backgroundColor: '#f8f9fa',
      border: '1px solid #dee2e6',
      borderRadius: '6px',
      borderLeft: '4px solid #007bff'
    }}>
      <div style={{ marginBottom: '10px' }}>
        <strong>Validation Message:</strong>
      </div>
      
      <div style={{ 
        whiteSpace: 'pre-line', 
        marginBottom: '15px',
        lineHeight: '1.5'
      }}>
        {message}
      </div>

      {companionAdvice && (
        <div>
          <button
            onClick={onToggleCompanion}
            style={{
              padding: '8px 16px',
              backgroundColor: '#6c757d',
              color: 'white',
              border: 'none',
              borderRadius: '4px',
              cursor: 'pointer',
              fontSize: '14px'
            }}
          >
            {showCompanion ? 'Hide More' : 'More?'}
          </button>

          {showCompanion && (
            <div style={{
              marginTop: '15px',
              padding: '15px',
              backgroundColor: '#fff',
              border: '1px solid #ced4da',
              borderRadius: '4px'
            }}>
              <div style={{ marginBottom: '10px' }}>
                <strong>Companion Advice:</strong>
              </div>
              <div style={{ 
                whiteSpace: 'pre-line',
                lineHeight: '1.5'
              }}>
                {companionAdvice}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  )
}

export default ValidationBox
