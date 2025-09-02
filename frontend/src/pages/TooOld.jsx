import React from 'react'
import Footer from '../components/Footer.jsx'

const TooOld = () => {
  return (
    <div style={styles.container}>
      <div style={styles.header}>
        <h1 style={styles.mainTitle}>
          Welcome, Grown-Ups 👋
        </h1>
        <p style={styles.tagline}>
          Your world, your say—too.
        </p>
      </div>

      <div style={styles.content}>
        {/* For Parents Section */}
        <div style={styles.section}>
          <h2 style={styles.sectionTitle}>For Parents</h2>
          <p style={styles.sectionText}>
            This isn't just about understanding your teen. It's about reconnecting with your own voice.
          </p>
          <div style={styles.questions}>
            <p style={styles.question}>What do you wish someone had told you?</p>
            <p style={styles.question}>What do you hope your child carries forward?</p>
          </div>
          <div style={styles.comingSoon}>
            <p style={styles.comingSoonTitle}>Coming soon:</p>
            <ul style={styles.featureList}>
              <li style={styles.featureListItem}>Reflection prompts</li>
              <li style={styles.featureListItem}>Your own private answers</li>
              <li style={styles.featureListItem}><em>Bar charts showing how other parents responded, too</em></li>
            </ul>
          </div>
        </div>

        {/* For Schools Section */}
        <div style={styles.section}>
          <h2 style={styles.sectionTitle}>For Schools</h2>
          <p style={styles.sectionText}>
            Teen mental health is increasingly visible, but support varies across school districts. A <a href="https://news.harvard.edu/gazette/story/2025/08/public-schools-a-weak-link-in-efforts-to-protect-teen-mental-health-study-suggests/" target="_blank" rel="noopener noreferrer" style={styles.link}>2025 Harvard Medical School study</a> indicates only 30% of U.S. public schools screen students for mental health issues, with even fewer offering in-school mental health care or telehealth.
          </p>
          <p style={styles.sectionText}>
            The need is critical: teens face stress, social media pressure, identity struggles, and often feel isolated. Surveys and screenings are important but can be expensive, limiting their frequency.
          </p>
          <p style={styles.sectionText}>
            This platform is a <strong>free emotional reflection tool</strong> that complements school efforts, providing a safe way for students to express their feelings, rather than replacing clinical care.
          </p>
          <div style={styles.comingSoon}>
            <p style={styles.comingSoonTitle}>Coming soon:</p>
            <ul style={styles.featureList}>
              <li style={styles.featureListItem}>Thoughtful input from real teens on wording, tone, and visuals</li>
              <li style={styles.featureListItem}>Anonymous format that allows students to open up and feel less alone</li>
              <li style={styles.featureListItem}>Support for schools adopting more consistent listening practices</li>
              <li style={styles.featureListItem}><em>schools.myworldmysay.com</em></li>
            </ul>
          </div>
        </div>

        {/* For Other Grown-Ups Section */}
        <div style={styles.section}>
          <h2 style={styles.sectionTitle}>For Other Grown-Ups</h2>
          <p style={styles.sectionText}>
            Whether you're a mentor, teacher, sibling, or just someone who's lived a little—you've got a story, a lens, a voice.
          </p>
          <p style={styles.sectionText}>
            We'll be asking real questions—about:
          </p>
          <div style={styles.topics}>
            <span style={styles.topic}>❤️ heartbreak</span>
            <span style={styles.topic}>👥 friendship</span>
            <span style={styles.topic}>💼 work</span>
            <span style={styles.topic}>🌱 healing</span>
            <span style={styles.topic}>🌀 choices you made (or didn't)</span>
          </div>
          <div style={styles.comingSoon}>
            <p style={styles.comingSoonTitle}>Coming soon:</p>
            <ul style={styles.featureList}>
              <li style={styles.featureListItem}>Thought-provoking polls</li>
              <li style={styles.featureListItem}>Insightful results</li>
              <li style={styles.featureListItem}>A space to reflect, laugh, regret, and grow</li>
              <li style={styles.featureListItem}>Sometimes, seeing the bar chart is all it takes to realize you're not the only one.</li>
            </ul>
          </div>
        </div>

        {/* Back Button */}
        <div style={styles.backButtonContainer}>
          <button 
            onClick={() => window.history.back()}
            style={styles.backButton}
          >
            ← Go Back
          </button>
        </div>
      </div>
      
      {/* Footer */}
      <Footer />
    </div>
  )
}

const styles = {
  container: {
    minHeight: '100vh',
    background: 'linear-gradient(135deg, #0A0F2B 0%, #1A1F3B 50%, #2A2F4B 100%)',
    padding: '40px 20px',
    color: 'white'
  },
  
  header: {
    textAlign: 'center',
    marginBottom: '50px'
  },
  
  mainTitle: {
    fontSize: '48px',
    fontWeight: 'bold',
    marginBottom: '20px',
    background: 'linear-gradient(135deg, #FFD93D 0%, #FFA500 100%)',
    WebkitBackgroundClip: 'text',
    WebkitTextFillColor: 'transparent',
    backgroundClip: 'text'
  },
  
  tagline: {
    fontSize: '24px',
    color: 'rgba(255, 255, 255, 0.9)',
    fontStyle: 'italic'
  },
  
  content: {
    maxWidth: '800px',
    margin: '0 auto'
  },
  
  section: {
    backgroundColor: 'rgba(255, 255, 255, 0.1)',
    borderRadius: '20px',
    padding: '30px',
    marginBottom: '30px',
    border: '1px solid rgba(255, 255, 255, 0.2)',
    backdropFilter: 'blur(10px)'
  },
  
  sectionTitle: {
    fontSize: '28px',
    fontWeight: 'bold',
    marginBottom: '20px',
    color: '#4ECDC4'
  },
  
  sectionText: {
    fontSize: '18px',
    lineHeight: '1.6',
    marginBottom: '20px',
    color: 'rgba(255, 255, 255, 0.9)'
  },
  
  questions: {
    marginBottom: '25px'
  },
  
  question: {
    fontSize: '20px',
    fontWeight: '600',
    color: '#FFD93D',
    marginBottom: '10px',
    fontStyle: 'italic'
  },
  
  topics: {
    display: 'flex',
    flexWrap: 'wrap',
    gap: '15px',
    marginBottom: '25px'
  },
  
  topic: {
    backgroundColor: 'rgba(78, 205, 196, 0.2)',
    padding: '8px 16px',
    borderRadius: '20px',
    fontSize: '16px',
    border: '1px solid rgba(78, 205, 196, 0.4)'
  },
  
  comingSoon: {
    backgroundColor: 'rgba(255, 217, 61, 0.1)',
    borderRadius: '15px',
    padding: '20px',
    border: '1px solid rgba(255, 217, 61, 0.3)'
  },
  
  comingSoonTitle: {
    fontSize: '18px',
    fontWeight: 'bold',
    color: '#FFD93D',
    marginBottom: '15px'
  },
  
  featureList: {
    listStyle: 'none',
    padding: 0,
    margin: 0
  },
  
  featureListItem: {
    fontSize: '16px',
    color: 'rgba(255, 255, 255, 0.8)',
    marginBottom: '8px',
    paddingLeft: '20px',
    position: 'relative'
  },
  
  backButtonContainer: {
    textAlign: 'center',
    marginTop: '40px'
  },
  
  backButton: {
    padding: '15px 30px',
    backgroundColor: 'rgba(255, 255, 255, 0.1)',
    color: 'white',
    border: '1px solid rgba(255, 255, 255, 0.3)',
    borderRadius: '25px',
    cursor: 'pointer',
    fontSize: '18px',
    fontWeight: '500',
    transition: 'all 0.3s ease',
    backdropFilter: 'blur(10px)'
  },
  
  link: {
    color: '#4ECDC4',
    textDecoration: 'underline',
    fontWeight: '500'
  }
}

export default TooOld
