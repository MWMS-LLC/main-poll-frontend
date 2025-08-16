// API Configuration
// Change this based on your environment

// For production deployment (update with your actual backend URL)
const PRODUCTION_API = 'https://teen-poll-backend.onrender.com'

// For local development
const LOCAL_API = 'http://localhost:8000'

// For phone access on local network
const NETWORK_API = 'http://192.168.87.244:8000'

// Automatically detect environment
const isProduction = window.location.hostname !== 'localhost' && !window.location.hostname.includes('192.168')
const isLocalNetwork = window.location.hostname.includes('192.168')

let API_BASE
if (isProduction) {
  API_BASE = PRODUCTION_API
} else if (isLocalNetwork) {
  API_BASE = NETWORK_API
} else {
  API_BASE = LOCAL_API
}

export default API_BASE
