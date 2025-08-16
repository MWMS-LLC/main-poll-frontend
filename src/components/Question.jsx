import React, { useState, useEffect } from 'react'
import axios from 'axios'
import OptionsList from './OptionsList.jsx'
import ValidationBox from './ValidationBox.jsx'
import ResultsBarChart from './ResultsBarChart.jsx'
import API_BASE from '../config.js'

const Question = ({ question, onAnswered }) => {
  // Define styles at the top to avoid initialization errors
  const styles = {
    questionContainer: {
      border: '1px solid rgba(255, 255, 255, 0.15)',
      borderRadius: '24px',
      padding: '35px',
      backgroundColor: 'transparent',
      marginBottom: '30px',
      boxShadow: 'none',
      backdropFilter: 'none',
      transition: 'all 0.3s ease',
      position: 'relative',
      overflow: 'visible'
    },
    questionHeader: {
      padding: '15px 20px',
      borderRadius: '8px 8px 0 0',
      marginBottom: '20px',
      background: 'linear-gradient(135deg, #4A5568 0%, #2D3748 100%)',
      color: 'white',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'space-between',
      boxShadow: '0 4px 10px rgba(0, 0, 0, 0.1)'
    },
    questionTitle: {
      margin: 0,
      fontSize: '20px',
      fontWeight: 'normal',
      color: 'black',
      lineHeight: '1.6',
      whiteSpace: 'pre-wrap',
      wordWrap: 'break-word',
      fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", "Helvetica Neue", Helvetica, Arial, sans-serif'
    },
    optionsContainer: {
      marginBottom: '20px'
    },
    errorContainer: {
      padding: '20px',
      backgroundColor: 'rgba(255, 107, 107, 0.1)',
      border: '1px solid #ff6b6b',
      borderRadius: '8px',
      color: '#ff6b6b',
      textAlign: 'center'
    },
    submitButton: {
      padding: '12px 24px',
      background: '#4A5568',
      color: 'white',
      border: 'none',
      borderRadius: '4px',
      cursor: 'pointer',
      fontSize: '16px',
      marginTop: '15px',
      transition: 'background-color 0.3s ease'
    },
    resultsContainer: {
      marginTop: '20px'
    },
    loadingContainer: {
      padding: '20px',
      textAlign: 'center',
      color: 'rgba(255, 255, 255, 0.8)'
    }
  }

  const [options, setOptions] = useState([])
  const [loading, setLoading] = useState(true)
  const [selectedOptions, setSelectedOptions] = useState([])
  const [showResults, setShowResults] = useState(false)
  const [results, setResults] = useState(null)
  const [validationMessage, setValidationMessage] = useState('')
  const [companionAdvice, setCompanionAdvice] = useState('')
  const [showCompanion, setShowCompanion] = useState(false)
  const [otherText, setOtherText] = useState('')
  const [showOtherInput, setShowOtherInput] = useState(false)

  useEffect(() => {
    console.log('Question useEffect triggered for:', question.question_code)
    fetchOptions()
  }, [question.question_code])

  const fetchOptions = async () => {
    try {
      setLoading(true)
      const response = await axios.get(`${API_BASE}/api/questions/${question.question_code}/options`)
      setOptions(response.data)
    } catch (err) {
      console.error('Error fetching options:', err)
    } finally {
      setLoading(false)
    }
  }

  const handleSingleChoice = async (optionSelect) => {
    try {
      // Get user_uuid from localStorage
      const userUuid = localStorage.getItem('user_uuid')
      console.log('Attempting to submit vote with user_uuid:', userUuid)
      console.log('All localStorage items:', Object.keys(localStorage).map(key => ({ key, value: localStorage.getItem(key) })))
      
      if (!userUuid) {
        console.error('No user_uuid found')
        console.log('localStorage contents:', localStorage)
        return
      }

      const voteData = {
        question_code: question.question_code,
        option_select: optionSelect,
        user_uuid: userUuid
      }
      console.log('Submitting vote data:', voteData)

      // Submit vote
      await axios.post(`${API_BASE}/api/vote`, voteData)

      // Get results
      const resultsResponse = await axios.get(`${API_BASE}/api/results/${question.question_code}`)
      setResults(resultsResponse.data)
      setShowResults(true)

      // Set validation message
      const selectedOption = options.find(opt => opt.option_select === optionSelect)
      setValidationMessage(selectedOption.response_message)
      setCompanionAdvice(selectedOption.companion_advice)
      setShowCompanion(false)

      // Notify parent component that question was answered
      if (onAnswered) {
        onAnswered(question)
      }
    } catch (err) {
      console.error('Error submitting vote:', err)
    }
  }

  const handleCheckboxSubmit = async () => {
    if (selectedOptions.length === 0) return

    try {
      // Get user_uuid from localStorage
      const userUuid = localStorage.getItem('user_uuid')
      console.log('Checkbox vote - user_uuid:', userUuid)
      if (!userUuid) {
        console.error('No user_uuid found for checkbox vote')
        console.log('localStorage contents:', localStorage)
        return
      }

      // Filter out OTHER from checkbox vote since it's handled separately
      const checkboxOptions = selectedOptions.filter(opt => opt !== 'OTHER')
      
      // Submit checkbox vote (only if there are non-OTHER options)
      if (checkboxOptions.length > 0) {
        await axios.post(`${API_BASE}/api/checkbox_vote`, {
          question_code: question.question_code,
          option_selects: checkboxOptions,
          user_uuid: userUuid
        })
      }

      // If OTHER is selected, submit the text separately
      if (selectedOptions.includes('OTHER') && otherText.trim()) {
        await axios.post(`${API_BASE}/api/other`, {
          question_code: question.question_code,
          question_text: question.question_text,
          other_text: otherText,
          user_uuid: userUuid
        })
      }

      // Get results
      const resultsResponse = await axios.get(`${API_BASE}/api/results/${question.question_code}`)
      setResults(resultsResponse.data)
      setShowResults(true)

      // Set validation messages for all selected options
      const messages = selectedOptions.map(opt => {
        const option = options.find(o => o.option_select === opt)
        return option ? option.response_message : ''
      }).filter(msg => msg)
      
      setValidationMessage(messages.join('\n\n'))
      
      // Set companion advice for all selected options
      const advice = selectedOptions.map(opt => {
        const option = options.find(o => o.option_select === opt)
        return option ? option.companion_advice : ''
      }).filter(adv => adv)
      
      setCompanionAdvice(advice.join('\n\n'))
      setShowCompanion(false)
      
      // Clear the form
      setSelectedOptions([])
      setOtherText('')

      // Notify parent component that question was answered
      if (onAnswered) {
        onAnswered(question)
      }
    } catch (err) {
      console.error('Error submitting checkbox vote:', err)
    }
  }

  const handleOtherSubmit = async () => {
    if (!otherText.trim()) return

    try {
      // Get user_uuid from localStorage
      const userUuid = localStorage.getItem('user_uuid')
      if (!userUuid) {
        console.error('No user_uuid found')
        return
      }

      await axios.post(`${API_BASE}/api/other`, {
        question_code: question.question_code,
        question_text: question.question_text,
        other_text: otherText,
        user_uuid: userUuid
      })

      // Get results after submitting
      const resultsResponse = await axios.get(`${API_BASE}/api/results/${question.question_code}`)
      setResults(resultsResponse.data)
      setShowResults(true)

      // Set validation message for OTHER response
      setValidationMessage('Thank you for sharing your thoughts!')
      setCompanionAdvice('Your unique perspective adds valuable insight to this poll.')
      setShowCompanion(false)

      // Clear the form
      setOtherText('')
      setShowOtherInput(false)

      // Notify parent component that question was answered
      if (onAnswered) {
        onAnswered(question)
      }
    } catch (err) {
      console.error('Error submitting other response:', err)
    }
  }

  const handleOptionChange = (optionSelect, checked) => {
    console.log(`Option change: ${optionSelect}, checked: ${checked}`)
    if (checked) {
      setSelectedOptions(prev => {
        const newOptions = [...prev, optionSelect]
        console.log('New selected options:', newOptions)
        return newOptions
      })
    } else {
      setSelectedOptions(prev => {
        const newOptions = prev.filter(opt => opt !== optionSelect)
        console.log('New selected options:', newOptions)
        return newOptions
      })
    }
  }

  const handleOtherClick = () => {
    setShowOtherInput(true)
    setSelectedOptions([])
  }

  if (loading) return <div style={styles.loadingContainer}>Loading options...</div>
  
  // Safety check for question data
  if (!question || !question.question_text) {
    console.error('Invalid question data:', question)
    return (
      <div style={styles.errorContainer}>
        <h3>Error: Invalid question data</h3>
        <p>This question could not be loaded properly.</p>
        <pre>{JSON.stringify(question, null, 2)}</pre>
      </div>
    )
  }

  return (
    <div style={{
      ...styles.questionContainer,
      borderColor: question.color_code || '#4A5568',
      boxShadow: `0 8px 25px ${question.color_code ? `${question.color_code}20` : '#4A556820'}`
    }}>
      <div style={{
        ...styles.questionHeader,
        background: question.color_code ? `linear-gradient(135deg, ${question.color_code} 0%, ${question.color_code}CC 100%)` : 'linear-gradient(135deg, #4A5568 0%, #2D3748 100%)'
      }}>
        <h3 style={styles.questionTitle}>
          {question.question_text || 'Question loading...'}
        </h3>
      </div>

      {!showResults && (
        <div style={styles.optionsContainer}>
          {options && options.length > 0 ? (
            <OptionsList
              options={options}
              isCheckbox={question.check_box}
              selectedOptions={selectedOptions}
              onOptionChange={handleOptionChange}
              onSingleChoice={handleSingleChoice}
              onOtherClick={handleOtherClick}
              onOtherSubmit={handleOtherSubmit}
              otherText={otherText}
              setOtherText={setOtherText}
              showOtherInput={showOtherInput}
            />
          ) : (
            <div style={styles.errorContainer}>
              <strong>Error:</strong> No options available for this question.
              <br />
              <small>Question code: {question.question_code}</small>
            </div>
          )}
        </div>
      )}

      {question.check_box && !showResults && selectedOptions.length > 0 && (
        <button
          onClick={handleCheckboxSubmit}
          style={{
            ...styles.submitButton,
            background: question.color_code || '#4A5568'
          }}
        >
          Submit
        </button>
      )}

      {showResults && (
        <div style={styles.resultsContainer}>
          {results ? (
            <ResultsBarChart results={results} questionText={question.question_text} options={options} />
          ) : (
            <div style={styles.errorContainer}>
              <strong>Error:</strong> No results available to display.
            </div>
          )}
          
          <ValidationBox
            message={validationMessage}
            companionAdvice={companionAdvice}
            showCompanion={showCompanion}
            onToggleCompanion={() => setShowCompanion(!showCompanion)}
          />
        </div>
      )}
    </div>
  )
}

export default Question
