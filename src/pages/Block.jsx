import React, { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import axios from 'axios'
import Question from '../components/Question'
import HamburgerMenu from '../components/HamburgerMenu'
import Footer from '../components/Footer.jsx'
import soundtrackService from '../services/soundtrackService'
import API_BASE from '../config.js'

const Block = () => {
  const [questions, setQuestions] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  const [answeredQuestions, setAnsweredQuestions] = useState(0)
  const [showMusicSuggestion, setShowMusicSuggestion] = useState(false)
  const [musicSuggestion, setMusicSuggestion] = useState(null)
  const { blockCode } = useParams()
  const navigate = useNavigate()

  useEffect(() => {
    // Check if user has a valid UUID
    const userUuid = localStorage.getItem('user_uuid')
    if (!userUuid) {
      console.log('No user UUID found, redirecting to landing page')
      navigate('/')
      return
    }
    
    console.log('User UUID found:', userUuid)
    fetchQuestions()
    loadSoundtracks()
  }, [blockCode, navigate])

  const loadSoundtracks = async () => {
    await soundtrackService.loadSoundtracks()
  }

  const fetchQuestions = async () => {
    try {
      setLoading(true)
      const response = await axios.get(`${API_BASE}/api/blocks/${blockCode}/questions`)
      setQuestions(response.data)
    } catch (err) {
      setError('Failed to fetch questions')
      console.error('Error fetching questions:', err)
    } finally {
      setLoading(false)
    }
  }

  const handleQuestionAnswered = (questionData) => {
    const newCount = answeredQuestions + 1
    setAnsweredQuestions(newCount)
    
    // Show music suggestion after answering a few questions
    if (newCount >= Math.min(3, questions.length) && !showMusicSuggestion) {
      setShowMusicSuggestion(true)
      generateMusicSuggestion(questionData)
    }
  }

  const generateMusicSuggestion = (questionData) => {
    if (!questionData || !questionData.question_text) return
    
    // Use the new smart recommendation system with the specific answered question
    const smartSong = soundtrackService.getSmartSongRecommendation(questionData.question_text, blockCode)
    if (smartSong) {
      setMusicSuggestion(smartSong)
    }
  }

  const handleListenToPlaylist = () => {
    navigate('/soundtrack')
  }

  if (loading) {
    return (
      <div style={styles.loadingContainer}>
        <div style={styles.loadingText}>Loading questions...</div>
        <div style={styles.loadingSpinner}></div>
      </div>
    )
  }

  if (error) {
    return (
      <div style={styles.errorContainer}>
        <div style={styles.errorText}>Oops! {error}</div>
      </div>
    )
  }

  return (
    <div style={styles.container}>
      {/* Hamburger Menu */}
      <HamburgerMenu />
      


      {/* Questions Container */}
      <div style={styles.questionsContainer}>
        <div style={styles.questionsList}>
          {questions.map((question, index) => (
            <div
              key={question.question_code}
              style={{
                ...styles.questionCard,
                animationDelay: `${index * 0.1}s`
              }}
              className="question-card"
            >
              <Question question={question} onAnswered={handleQuestionAnswered} />
            </div>
          ))}
        </div>
      </div>

      {/* Music Suggestion Section */}
      {showMusicSuggestion && musicSuggestion && (
        <div style={styles.musicSuggestionContainer}>
          <div style={styles.musicSuggestionCard}>
            <div style={styles.musicIcon}>🎵</div>
            <h3 style={styles.musicSuggestionTitle}>Hey, listen to a song to expand your thoughts</h3>
            <div style={styles.songSuggestion}>
              <div style={styles.songTitle}>{musicSuggestion.title}</div>
              <div style={styles.songLyrics}>"{musicSuggestion.lyrics}"</div>
            </div>
            <div style={styles.musicButtons}>
              <button 
                style={styles.listenButton}
                onClick={handleListenToPlaylist}
              >
                Listen to Playlist
              </button>
              <button 
                style={styles.skipButton}
                onClick={() => setShowMusicSuggestion(false)}
              >
                Maybe Later
              </button>
            </div>
          </div>
        </div>
      )}
      
      {/* Footer */}
      <Footer />
    </div>
  )
}

// Premium styling
const styles = {
  container: {
    minHeight: '100vh',
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    background: 'linear-gradient(135deg, #0A0F2B 0%, #1A1F3B 50%, #2A2F4B 100%)',
    position: 'relative',
    overflowY: 'auto',
    padding: '20px'
  },
  
  loadingContainer: {
    minHeight: '100vh',
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    justifyContent: 'center',
    background: 'linear-gradient(135deg, #0A0F2B 0%, #1A1F3B 100%)',
    gap: '20px'
  },
  
  loadingText: {
    color: 'rgba(255, 255, 255, 0.8)',
    fontSize: '24px',
    fontWeight: '500'
  },
  
  loadingSpinner: {
    width: '40px',
    height: '40px',
    border: '4px solid rgba(255, 255, 255, 0.3)',
    borderTop: '4px solid #4ECDC4',
    borderRadius: '50%',
    animation: 'spin 1s linear infinite'
  },
  
  errorContainer: {
    minHeight: '100vh',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    background: 'linear-gradient(135deg, #0A0F2B 0%, #1A1F3B 100%)'
  },
  
  errorText: {
    color: '#FF7675',
    fontSize: '20px',
    textAlign: 'center'
  },
  

  
  questionsContainer: {
    width: '100%',
    flex: 1,
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    marginTop: '40px'
  },
  
  questionsList: {
    width: '100%',
    maxWidth: '800px',
    display: 'flex',
    flexDirection: 'column',
    gap: '30px'
  },
  
  questionCard: {
    background: 'transparent',
    borderRadius: '0',
    padding: '0',
    border: 'none',
    boxShadow: 'none',
    backdropFilter: 'none',
    transition: 'all 0.4s ease',
    animation: 'questionSlideIn 0.6s ease-out forwards',
    opacity: 0,
    transform: 'translateY(30px)',
    position: 'relative',
    overflow: 'visible'
  },

  musicSuggestionContainer: {
    width: '100%',
    maxWidth: '800px',
    marginTop: '40px',
    padding: '20px',
    background: 'linear-gradient(135deg, rgba(255, 255, 255, 0.05) 0%, rgba(255, 255, 255, 0.02) 100%)',
    borderRadius: '20px',
    border: '1px solid rgba(255, 255, 255, 0.1)',
    boxShadow: '0 10px 30px rgba(0, 0, 0, 0.2)',
    backdropFilter: 'blur(10px)',
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'center'
  },

  musicSuggestionCard: {
    background: 'linear-gradient(135deg, rgba(255, 255, 255, 0.1) 0%, rgba(255, 255, 255, 0.05) 100%)',
    borderRadius: '15px',
    padding: '25px',
    border: '1px solid rgba(255, 255, 255, 0.1)',
    boxShadow: '0 10px 20px rgba(0, 0, 0, 0.2)',
    backdropFilter: 'blur(10px)',
    textAlign: 'center',
    width: '100%',
    maxWidth: '600px'
  },

  musicIcon: {
    fontSize: '40px',
    marginBottom: '15px',
    color: '#4ECDC4'
  },

  musicSuggestionTitle: {
    fontSize: '22px',
    fontWeight: 'bold',
    color: 'white',
    marginBottom: '10px',
    textShadow: '0 0 15px rgba(255, 255, 255, 0.3)'
  },

  musicSuggestionText: {
    fontSize: '16px',
    color: 'rgba(255, 255, 255, 0.8)',
    marginBottom: '20px',
    lineHeight: '1.5'
  },

  songSuggestion: {
    background: 'rgba(255, 255, 255, 0.08)',
    borderRadius: '10px',
    padding: '15px',
    border: '1px solid rgba(255, 255, 255, 0.1)',
    marginBottom: '20px',
    textAlign: 'left'
  },

  songTitle: {
    fontSize: '20px',
    fontWeight: 'bold',
    color: 'white',
    marginBottom: '5px'
  },

  songLyrics: {
    fontSize: '14px',
    color: 'rgba(255, 255, 255, 0.7)',
    fontStyle: 'italic'
  },

  musicButtons: {
    display: 'flex',
    justifyContent: 'space-around',
    gap: '15px'
  },

  listenButton: {
    background: '#4ECDC4',
    color: 'white',
    padding: '12px 25px',
    borderRadius: '25px',
    border: 'none',
    cursor: 'pointer',
    fontSize: '16px',
    fontWeight: 'bold',
    transition: 'all 0.3s ease',
    boxShadow: '0 5px 15px rgba(78, 205, 196, 0.4)'
  },

  skipButton: {
    background: 'rgba(255, 255, 255, 0.1)',
    color: 'rgba(255, 255, 255, 0.7)',
    padding: '12px 25px',
    borderRadius: '25px',
    border: '1px solid rgba(255, 255, 255, 0.2)',
    cursor: 'pointer',
    fontSize: '16px',
    fontWeight: 'bold',
    transition: 'all 0.3s ease'
  }
}

export default Block
