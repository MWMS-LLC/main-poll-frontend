import React from 'react'

const ValidationBox = ({ message, companionAdvice, showCompanion, onToggleCompanion }) => {
  if (!message) return null

  return (
    <div style={{
      marginTop: '20px',
      padding: '20px',
      backgroundColor: 'rgba(255, 255, 255, 0.05)',
      border: '1px solid rgba(45, 125, 122, 0.3)',
      borderRadius: '16px',
      borderLeft: '4px solid #2D7D7A',
      backdropFilter: 'blur(10px)',
      boxShadow: '0 8px 25px rgba(0, 0, 0, 0.2)'
    }}>
      <div style={{ 
        marginBottom: '15px',
        color: '#2D7D7A',
        fontWeight: '600',
        fontSize: '16px'
      }}>
        ✨ Your response has been recorded!
      </div>
      
      <div style={{ 
        whiteSpace: 'pre-line', 
        marginBottom: '20px',
        lineHeight: '1.6',
        color: 'rgba(255, 255, 255, 0.9)',
        fontSize: '15px'
      }}>
        {message}
      </div>

      {companionAdvice && (
        <div>
          <button
            onClick={onToggleCompanion}
            style={{
              padding: '10px 20px',
              backgroundColor: showCompanion ? '#4ECDC4' : 'rgba(45, 125, 122, 0.2)',
              color: 'white',
              border: '1px solid rgba(45, 125, 122, 0.4)',
              borderRadius: '25px',
              cursor: 'pointer',
              fontSize: '14px',
              fontWeight: '600',
              transition: 'all 0.3s ease',
              boxShadow: showCompanion ? '0 4px 15px rgba(78, 205, 196, 0.3)' : 'none'
            }}
          >
            {showCompanion ? 'Hide More' : 'More?'}
          </button>

          {showCompanion && (
            <div style={{
              marginTop: '20px',
              padding: '20px',
              backgroundColor: 'rgba(45, 125, 122, 0.1)',
              border: '1px solid rgba(45, 125, 122, 0.2)',
              borderRadius: '12px',
              backdropFilter: 'blur(10px)'
            }}>
              <div style={{ 
                marginBottom: '15px',
                color: '#4ECDC4',
                fontWeight: '600',
                fontSize: '16px'
              }}>
                💡 Companion Advice:
              </div>
              <div style={{ 
                whiteSpace: 'pre-line',
                lineHeight: '1.6',
                color: 'rgba(255, 255, 255, 0.9)',
                fontSize: '15px',
                marginBottom: '20px'
              }}>
                {companionAdvice}
              </div>
              
              {/* Disclaimer and Help Link */}
              <div style={{
                marginTop: '20px',
                padding: '15px',
                backgroundColor: 'rgba(255, 193, 7, 0.1)',
                border: '1px solid rgba(255, 193, 7, 0.3)',
                borderRadius: '8px',
                borderLeft: '3px solid #FFC107'
              }}>
                <div style={{
                  color: '#FFC107',
                  fontWeight: '600',
                  fontSize: '14px',
                  marginBottom: '8px'
                }}>
                  ⚠️ Important Note:
                </div>
                <div style={{
                  color: 'rgba(255, 255, 255, 0.8)',
                  fontSize: '13px',
                  lineHeight: '1.5',
                  marginBottom: '12px'
                }}>
                  This advice is for reflection and support—not a substitute for professional help. If you need someone to talk to, we have resources available.
                </div>
                <a 
                  href="/help" 
                  style={{
                    color: '#4ECDC4',
                    textDecoration: 'none',
                    fontSize: '13px',
                    fontWeight: '500',
                    display: 'inline-flex',
                    alignItems: 'center',
                    gap: '6px'
                  }}
                  onMouseEnter={(e) => e.target.style.textDecoration = 'underline'}
                  onMouseLeave={(e) => e.target.style.textDecoration = 'none'}
                >
                  📚 Get Help & Resources →
                </a>
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  )
}

export default ValidationBox
