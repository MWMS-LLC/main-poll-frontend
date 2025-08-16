import React from 'react'

const Footer = () => {
  return (
    <div style={styles.footer}>
      <div style={styles.footerContent}>
        <div style={styles.disclaimer}>
          This app is for reflection and educational purposes only. It is not a substitute for therapy, diagnosis, or professional mental health care.
        </div>
        
        <div style={styles.footerLinks}>
          <a href="/privacy" style={styles.footerLink}>Privacy Policy</a>
          <span style={styles.separator}>•</span>
          <a href="/contact" style={styles.footerLink}>Contact</a>
        </div>
        
        <div style={styles.socialIcons}>
          <a 
            href="https://www.instagram.com/myworldmysay" 
            target="_blank" 
            rel="noopener noreferrer"
            style={styles.socialIcon}
          >
            <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor">
              <path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zm0-2.163c-3.259 0-3.667.014-4.947.072-4.358.2-6.78 2.618-6.98 6.98-.059 1.281-.073 1.689-.073 4.948 0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98 1.281.058 1.689.072 4.948.072 3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98-1.281-.059-1.69-.073-4.949-.073zm0 5.838c-3.403 0-6.162 2.759-6.162 6.162s2.759 6.163 6.162 6.163 6.162-2.759 6.162-6.163c0-3.403-2.759-6.162-6.162-6.162zm0 10.162c-2.209 0-4-1.79-4-4 0-2.209 1.791-4 4-4s4 1.791 4 4c0 2.21-1.791 4-4 4zm6.406-11.845c-.796 0-1.441.645-1.441 1.44s.645 1.44 1.441 1.44c.795 0 1.439-.645 1.439-1.44s-.644-1.44-1.439-1.44z"/>
            </svg>
          </a>
          <a 
            href="https://www.tiktok.com/@myworldmysay" 
            target="_blank" 
            rel="noopener noreferrer"
            style={styles.socialIcon}
          >
            <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor">
              <path d="M19.59 6.69a4.83 4.83 0 0 1-3.77-4.25V2h-3.45v13.67a2.89 2.89 0 0 1-5.2 1.74 2.89 2.89 0 0 1 2.31-4.64 2.93 2.93 0 0 1 .88.13V9.4a6.84 6.84 0 0 0-.88-.05A6.33 6.33 0 0 0 4 15.38a6.33 6.33 0 0 0 10.86 4.43v-3.45a4.85 4.85 0 0 1-1.74.32 4.83 4.83 0 0 1-4.83-4.83 4.83 4.83 0 0 1 4.83-4.83z"/>
            </svg>
          </a>
        </div>
      </div>
    </div>
  )
}

const styles = {
  footer: {
    width: '100%',
    padding: '30px 20px',
    marginTop: 'auto',
    background: 'rgba(0, 0, 0, 0.2)',
    borderTop: '1px solid rgba(255, 255, 255, 0.1)'
  },
  
  footerContent: {
    maxWidth: '800px',
    margin: '0 auto',
    textAlign: 'center'
  },
  
  disclaimer: {
    color: 'rgba(255, 255, 255, 0.9)',
    fontSize: '14px',
    lineHeight: '1.5',
    marginBottom: '20px',
    fontStyle: 'italic'
  },
  
  footerLinks: {
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'center',
    gap: '15px',
    marginBottom: '20px'
  },
  
  footerLink: {
    color: 'white',
    textDecoration: 'none',
    fontSize: '14px',
    fontWeight: '500',
    transition: 'all 0.2s ease',
    ':hover': {
      color: '#4ECDC4',
      textDecoration: 'underline'
    }
  },
  
  separator: {
    color: 'rgba(255, 255, 255, 0.6)',
    fontSize: '14px'
  },
  
  socialIcons: {
    display: 'flex',
    justifyContent: 'center',
    gap: '20px'
  },
  
  socialIcon: {
    color: 'white',
    textDecoration: 'none',
    transition: 'all 0.2s ease',
    ':hover': {
      color: '#4ECDC4',
      transform: 'scale(1.1)'
    }
  }
}

export default Footer
