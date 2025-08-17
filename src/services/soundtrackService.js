// Soundtrack service for managing music data and playlist integration
class SoundtrackService {
  constructor() {
    this.soundtracks = []
    this.playlists = []
    this.loaded = false
  }

  // Load soundtrack data from CSV data
  async loadSoundtracks() {
    try {
      // Use the actual soundtrack data from the CSV
      const data = [
        {
          song_id: "STR_01",
          song_title: "Spark Still Rise (Male Rap)",
          mood_tag: "bitter, believing",
          playlist_tag: "Spiral, Believe, Lowkey",
          lyrics_snippet: "You ain't gotta fake the fire. Even sparks can light the sky.",
          featured: "TRUE",
          featured_order: 1,
          file_url: "https://myworld-soundtrack.s3.us-east-2.amazonaws.com/myworld_soundtrack/sparks-still-rise.mp3"
        },
        {
          song_id: "STR_02",
          song_title: "Spark Still Rise (Female Rap)",
          mood_tag: "bitter, believing",
          playlist_tag: "Spiral, Believe, Lowkey",
          lyrics_snippet: "You ain't gotta fake the fire. Even sparks can light the sky.",
          featured: "TRUE",
          featured_order: 2,
          file_url: "https://myworld-soundtrack.s3.us-east-2.amazonaws.com/myworld_soundtrack/sparks-still-rise+Girl.mp3"
        },
        {
          song_id: "DP_01",
          song_title: "Daring Path (Female V1)",
          mood_tag: "believing",
          playlist_tag: "Believe",
          lyrics_snippet: "I don't need small mirrors to shine. I don't need blind eyes to define.",
          featured: "TRUE",
          featured_order: 3,
          file_url: "https://myworld-soundtrack.s3.us-east-2.amazonaws.com/myworld_soundtrack/daring+path.mp3"
        },
        {
          song_id: "DP_02",
          song_title: "Daring Path (Female V2)",
          mood_tag: "believing",
          playlist_tag: "Believe",
          lyrics_snippet: "I don't need small mirrors to shine. I don't need blind eyes to define.",
          featured: "TRUE",
          featured_order: 4,
          file_url: "https://myworld-soundtrack.s3.us-east-2.amazonaws.com/myworld_soundtrack/daring+path+2.mp3"
        },
        {
          song_id: "DBNF_01",
          song_title: "Deleted But Not Forgotten (Female)",
          mood_tag: "bitter, believing",
          playlist_tag: "Hurt, Believe, Spiral",
          lyrics_snippet: "Delete the post, But Not Forgotten. I'm still here, still me, still real.",
          featured: "TRUE",
          featured_order: 5,
          file_url: "https://myworld-soundtrack.s3.us-east-2.amazonaws.com/myworld_soundtrack/deleted%2C-but-not-forgotten.mp3"
        },
        {
          song_id: "MVMW_01",
          song_title: "My Voice at My World My Say",
          mood_tag: "soft, believing",
          playlist_tag: "Spiral, Believe",
          lyrics_snippet: "Somewhere, someone's feeling just like this",
          featured: "TRUE",
          featured_order: 13,
          file_url: "https://myworld-soundtrack.s3.us-east-2.amazonaws.com/myworld_soundtrack/my-voice.mp3"
        }
      ]
      
      // Transform the data to match our component's format
      this.soundtracks = data.map(song => ({
        id: song.song_id,
        title: song.song_title,
        mood: song.mood_tag,
        playlist: song.playlist_tag,
        lyrics: song.lyrics_snippet,
        featured: song.featured === 'TRUE',
        featuredOrder: parseInt(song.featured_order),
        fileUrl: song.file_url
      }))

      // Extract unique playlists
      this.playlists = ['All Songs']
      this.soundtracks.forEach(song => {
        const songPlaylists = song.playlist.split(', ').map(p => p.trim())
        songPlaylists.forEach(playlist => {
          if (!this.playlists.includes(playlist)) {
            this.playlists.push(playlist)
          }
        })
      })

      this.loaded = true
      return this.soundtracks
    } catch (error) {
      console.error('Error loading soundtracks:', error)
      return []
    }
  }

  // Get all soundtracks
  getSoundtracks() {
    return this.soundtracks
  }

  // Get all playlists
  getPlaylists() {
    return this.playlists
  }

  // Get songs by playlist
  getSongsByPlaylist(playlist) {
    if (playlist === 'All Songs') {
      return this.soundtracks
    }
    return this.soundtracks.filter(song => 
      song.playlist.includes(playlist)
    )
  }

  // Get songs by mood
  getSongsByMood(mood) {
    return this.soundtracks.filter(song => 
      song.mood.toLowerCase().includes(mood.toLowerCase())
    )
  }

  // Get featured songs
  getFeaturedSongs() {
    return this.soundtracks
      .filter(song => song.featured)
      .sort((a, b) => a.featuredOrder - b.featuredOrder)
  }

  // Get songs by block/question context
  getSongsByContext(context) {
    // Map poll contexts to music moods/playlists
    const contextMappings = {
      'relationship': ['Love', 'Hurt', 'Believe'],
      'friendship': ['Love', 'Hurt', 'Believe'],
      'family': ['Family'],
      'school': ['Believe', 'Inspiring'],
      'emotions': ['Hurt', 'Believe', 'Spiral'],
      'identity': ['Believe', 'Inspiring'],
      'breakup': ['Breakup', 'Hurt', 'Believe'],
      'bullying': ['Hurt', 'Believe', 'Spiral'],
      'self-esteem': ['Believe', 'Inspiring'],
      'anxiety': ['Soft', 'Believing', 'Lowkey']
    }

    const relevantPlaylists = contextMappings[context] || ['Believe']
    const relevantSongs = []

    relevantPlaylists.forEach(playlist => {
      const songs = this.getSongsByPlaylist(playlist)
      relevantSongs.push(...songs)
    })

    // Remove duplicates and return unique songs
    return [...new Map(relevantSongs.map(song => [song.id, song])).values()]
  }

  // NEW: Smart song recommendation based on question content
  getSmartSongRecommendation(questionText, blockCode = '') {
    if (!questionText) return null
    
    const text = questionText.toLowerCase()
    
    // Define emotional and thematic keywords with their song matches
    const keywordMappings = {
      // Love & Relationships
      'love': { playlists: ['Love', 'Believe'], mood: 'soft, believing' },
      'relationship': { playlists: ['Love', 'Believe'], mood: 'soft, believing' },
      'crush': { playlists: ['Love', 'Believe'], mood: 'soft, believing' },
      'dating': { playlists: ['Love', 'Believe'], mood: 'soft, believing' },
      'romantic': { playlists: ['Love', 'Believe'], mood: 'soft, believing' },
      
      // Heartbreak & Hurt
      'heartbreak': { playlists: ['Hurt', 'Spiral'], mood: 'bitter, believing' },
      'breakup': { playlists: ['Hurt', 'Spiral'], mood: 'bitter, believing' },
      'hurt': { playlists: ['Hurt', 'Spiral'], mood: 'bitter, believing' },
      'pain': { playlists: ['Hurt', 'Spiral'], mood: 'bitter, believing' },
      'sad': { playlists: ['Hurt', 'Spiral'], mood: 'bitter, believing' },
      'lonely': { playlists: ['Hurt', 'Spiral'], mood: 'bitter, believing' },
      
      // Confidence & Empowerment
      'confidence': { playlists: ['Believe', 'Inspiring'], mood: 'believing' },
      'empower': { playlists: ['Believe', 'Inspiring'], mood: 'believing' },
      'strong': { playlists: ['Believe', 'Inspiring'], mood: 'believing' },
      'courage': { playlists: ['Believe', 'Inspiring'], mood: 'believing' },
      'brave': { playlists: ['Believe', 'Inspiring'], mood: 'believing' },
      
      // Anxiety & Stress
      'anxiety': { playlists: ['Soft', 'Lowkey'], mood: 'soft, believing' },
      'stress': { playlists: ['Soft', 'Lowkey'], mood: 'soft, believing' },
      'worried': { playlists: ['Soft', 'Lowkey'], mood: 'soft, believing' },
      'nervous': { playlists: ['Soft', 'Lowkey'], mood: 'soft, believing' },
      
      // Social & Friendship
      'friend': { playlists: ['Love', 'Believe'], mood: 'soft, believing' },
      'social': { playlists: ['Love', 'Believe'], mood: 'soft, believing' },
      'belong': { playlists: ['Love', 'Believe'], mood: 'soft, believing' },
      'included': { playlists: ['Love', 'Believe'], mood: 'soft, believing' },
      
      // Family & Home
      'family': { playlists: ['Family'], mood: 'soft, believing' },
      'home': { playlists: ['Family'], mood: 'soft, believing' },
      'parent': { playlists: ['Family'], mood: 'soft, believing' },
      
      // School & Learning
      'school': { playlists: ['Believe', 'Inspiring'], mood: 'believing' },
      'study': { playlists: ['Believe', 'Inspiring'], mood: 'believing' },
      'learn': { playlists: ['Believe', 'Inspiring'], mood: 'believing' },
      'future': { playlists: ['Believe', 'Inspiring'], mood: 'believing' },
      
      // Identity & Self-Discovery
      'identity': { playlists: ['Believe', 'Inspiring'], mood: 'believing' },
      'discover': { playlists: ['Believe', 'Inspiring'], mood: 'believing' },
      'myself': { playlists: ['Believe', 'Inspiring'], mood: 'believing' },
      'who i am': { playlists: ['Believe', 'Inspiring'], mood: 'believing' }
    }
    
    // Find matching keywords
    let bestMatch = null
    let highestScore = 0
    
    for (const [keyword, mapping] of Object.entries(keywordMappings)) {
      if (text.includes(keyword)) {
        // Score based on keyword length and position
        const score = keyword.length + (text.indexOf(keyword) < 20 ? 5 : 0)
        if (score > highestScore) {
          highestScore = score
          bestMatch = mapping
        }
      }
    }
    
    // If no keyword match, use block code context
    if (!bestMatch) {
      if (blockCode.includes('love') || blockCode.includes('relationship')) {
        bestMatch = { playlists: ['Love', 'Believe'], mood: 'soft, believing' }
      } else if (blockCode.includes('family')) {
        bestMatch = { playlists: ['Family'], mood: 'soft, believing' }
      } else if (blockCode.includes('school')) {
        bestMatch = { playlists: ['Believe', 'Inspiring'], mood: 'believing' }
      } else {
        bestMatch = { playlists: ['Believe'], mood: 'believing' }
      }
    }
    
    // Get songs that match the best match
    let relevantSongs = []
    bestMatch.playlists.forEach(playlist => {
      const songs = this.getSongsByPlaylist(playlist)
      relevantSongs.push(...songs)
    })
    
    // Filter by mood if possible
    if (bestMatch.mood) {
      relevantSongs = relevantSongs.filter(song => 
        song.mood.toLowerCase().includes(bestMatch.mood.split(',')[0].trim().toLowerCase())
      )
    }
    
    // Remove duplicates
    relevantSongs = [...new Map(relevantSongs.map(song => [song.id, song])).values()]
    
    // Return the best matching song (not random)
    if (relevantSongs.length > 0) {
      // Prioritize featured songs
      const featuredSongs = relevantSongs.filter(song => song.featured)
      if (featuredSongs.length > 0) {
        const song = featuredSongs[0]
        // Add question context for display
        song.questionContext = questionText.length > 60 ? questionText.substring(0, 60) + '...' : questionText
        return song
      }
      const song = relevantSongs[0]
      // Add question context for display
      song.questionContext = questionText.length > 60 ? questionText.substring(0, 60) + '...' : questionText
      return song
    }
    
    return null
  }

  // Check if data is loaded
  isLoaded() {
    return this.loaded
  }
}

// Create and export a singleton instance
const soundtrackService = new SoundtrackService()
export default soundtrackService
