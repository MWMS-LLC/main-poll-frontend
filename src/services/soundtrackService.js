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
          song_id: "LRDD_01",
          song_title: "Left on Read, Dragged in DMs (Female)",
          mood_tag: "bitter, believing",
          playlist_tag: "Hurt, Believe, Spiral",
          lyrics_snippet: "No reply, just side-eyes. But trust—I'm louder than your will.",
          featured: "TRUE",
          featured_order: 6,
          file_url: "https://myworld-soundtrack.s3.us-east-2.amazonaws.com/myworld_soundtrack/Left+on+Read%2C+Dragged+in+DMs.mp3"
        },
        {
          song_id: "PINI_01",
          song_title: "Photos I'm Not In (Male, Cinematic Rap)",
          mood_tag: "bitter, believing",
          playlist_tag: "Hurt, Believe, Spiral",
          lyrics_snippet: "Photos I'm not in, don't dim my light.",
          featured: "TRUE",
          featured_order: 7,
          file_url: "https://myworld-soundtrack.s3.us-east-2.amazonaws.com/myworld_soundtrack/Photos+I%E2%80%99m+Not+In.mp3"
        },
        {
          song_id: "ISWIA_01",
          song_title: "I Said What I Am (Female, Hip-Hop)",
          mood_tag: "bitter, believing",
          playlist_tag: "Hurt, Believe, Spiral",
          lyrics_snippet: "I know what I'm building. Even when they tear me down",
          featured: "TRUE",
          featured_order: 8,
          file_url: "https://myworld-soundtrack.s3.us-east-2.amazonaws.com/myworld_soundtrack/I+Said+What+I+Am+(Hip-Hop)+(Edit).mp3"
        },
        {
          song_id: "IWOTM_01",
          song_title: "I want one that's mine (Male)",
          mood_tag: "soft, believing",
          playlist_tag: "Spiral, Believe, Lowkey",
          lyrics_snippet: "Is it peace or just pretend? I'm tired of borrowing moods",
          featured: "TRUE",
          featured_order: 9,
          file_url: "https://myworld-soundtrack.s3.us-east-2.amazonaws.com/myworld_soundtrack/i-want-one-that%E2%80%99s-mine..mp3"
        },
        {
          song_id: "IWMG_01",
          song_title: "I wasn't mean to go (Female)",
          mood_tag: "soft, believing",
          playlist_tag: "Hurt, Spiral",
          lyrics_snippet: "I wasn't left out—I feel right. Not every room deserves my light",
          featured: "TRUE",
          featured_order: 10,
          file_url: "https://myworld-soundtrack.s3.us-east-2.amazonaws.com/myworld_soundtrack/I+Wasn%E2%80%99t+Meant+to+Go.mp3"
        },
        {
          song_id: "STS_M",
          song_title: "Sky That Stayed (Male)",
          mood_tag: "believing, inspiring",
          playlist_tag: "Hurt, Believe, Breakup",
          lyrics_snippet: "You were the storm that tore through fast. But I'm the sky that always lasts.",
          featured: "TRUE",
          featured_order: 11,
          file_url: "https://myworld-soundtrack.s3.us-east-2.amazonaws.com/myworld_soundtrack/Sky+That+Stayed+(Male).mp3"
        },
        {
          song_id: "STS_F",
          song_title: "Sky That Stayed (Female)",
          mood_tag: "believing, inspiring",
          playlist_tag: "Hurt, Believe, Breakup",
          lyrics_snippet: "You were the storm that tore through fast. But I'm the sky that always lasts.",
          featured: "TRUE",
          featured_order: 12,
          file_url: "https://myworld-soundtrack.s3.us-east-2.amazonaws.com/myworld_soundtrack/Sky+That+Stayed+(Female).mp3"
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
        },
        {
          song_id: "THM_1",
          song_title: "Theme Song (Male Inspiring Rap)",
          mood_tag: "inspiring",
          playlist_tag: "Theme Song",
          lyrics_snippet: "My World, My Say",
          featured: "TRUE",
          featured_order: 14,
          file_url: "https://myworld-soundtrack.s3.us-east-2.amazonaws.com/myworld_soundtrack/Theme+(Male+Inspiring+Rap).mp3"
        },
        {
          song_id: "THM_2",
          song_title: "Theme Song (Girl HipHop)",
          mood_tag: "spicy",
          playlist_tag: "Theme Song",
          lyrics_snippet: "My World, My Say",
          featured: "TRUE",
          featured_order: 15,
          file_url: "https://myworld-soundtrack.s3.us-east-2.amazonaws.com/myworld_soundtrack/Theme+(Girl%2C+HipHop).mp3"
        },
        {
          song_id: "TMTSA_M",
          song_title: "Tell Me That Story Again",
          mood_tag: "love, lowkey",
          playlist_tag: "Love, Lowkey",
          lyrics_snippet: "Just learning the map that leads to you. No need to impress, no need to bend.",
          featured: "TRUE",
          featured_order: 25,
          file_url: "https://myworld-soundtrack.s3.us-east-2.amazonaws.com/myworld_soundtrack/Tell+Me+That+Story+Again.mp3"
        },
        {
          song_id: "CIMH",
          song_title: "Cool in My Head",
          mood_tag: "Chaos, love",
          playlist_tag: "Love, Chaos",
          lyrics_snippet: "I planned the whole thing in my head. I'd say 'hey' real chill, then nod instead.",
          featured: "TRUE",
          featured_order: 26,
          file_url: "https://myworld-soundtrack.s3.us-east-2.amazonaws.com/myworld_soundtrack/Cool+in+My+Head.mp3"
        },
        {
          song_id: "LYAN",
          song_title: "Left You a Note (Male)",
          mood_tag: "love, lowkey",
          playlist_tag: "Love, Lowkey",
          lyrics_snippet: "I left you a note, didn't sign my name. But it's tucked in your book, like a gentle flame.",
          featured: "TRUE",
          featured_order: 27,
          file_url: "https://myworld-soundtrack.s3.us-east-2.amazonaws.com/myworld_soundtrack/Left+You+a+Note.mp3"
        },
        {
          song_id: "SYAS",
          song_title: "Save You a Seat",
          mood_tag: "Chaos, love",
          playlist_tag: "Love, Chaos",
          lyrics_snippet: "You dropped your pen, I gave it back. Said, 'No big deal,' then overreacted.",
          featured: "TRUE",
          featured_order: 28,
          file_url: "https://myworld-soundtrack.s3.us-east-2.amazonaws.com/myworld_soundtrack/Saved+You+a+Seat.mp3"
        },
        {
          song_id: "YAAW_M",
          song_title: "You're already whole",
          mood_tag: "love",
          playlist_tag: "Love",
          lyrics_snippet: "I don't need flowers or big displays. Just look at me that certain way.",
          featured: "TRUE",
          featured_order: 29,
          file_url: "https://myworld-soundtrack.s3.us-east-2.amazonaws.com/myworld_soundtrack/You%E2%80%99re+already+whole.mp3"
        },
        {
          song_id: "YEAH_F",
          song_title: "Yeah, I Noticed (POV: The girl who sees through the act)",
          mood_tag: "love",
          playlist_tag: "Love",
          lyrics_snippet: "You don't have to say you're brave. I already saw you try.",
          featured: "TRUE",
          featured_order: 30,
          file_url: "https://myworld-soundtrack.s3.us-east-2.amazonaws.com/myworld_soundtrack/Yeah%2C+I+Noticed+(POV_+The+girl+who+sees+through+the+act)+(1).mp3"
        },
        {
          song_id: "GG_1",
          song_title: "Glossed & Glowing",
          mood_tag: "pinky",
          playlist_tag: "Pinky",
          lyrics_snippet: "Glossed and glowing, heart still knowing: You don't need loud to be overflowing",
          featured: "TRUE",
          featured_order: 31,
          file_url: "https://myworld-soundtrack.s3.us-east-2.amazonaws.com/myworld_soundtrack/Glossed+%26+Glowing.mp3"
        },
        {
          song_id: "SSKY_TB",
          song_title: "Same Sky (Rap Teen Boy Side)",
          mood_tag: "family",
          playlist_tag: "Family",
          lyrics_snippet: "I don't need you to fix the rain. Just stay close when I'm hiding pain",
          featured: "TRUE",
          featured_order: 33,
          file_url: "https://myworld-soundtrack.s3.us-east-2.amazonaws.com/myworld_soundtrack/Same+Sky+(Rap+Teen+Side).mp3"
        },
        {
          song_id: "SSKY_TG",
          song_title: "Same Sky (Teen Girl Side)",
          mood_tag: "family",
          playlist_tag: "Family",
          lyrics_snippet: "I don't need you to fix the rain. Just stay close when I'm hiding pain",
          featured: "TRUE",
          featured_order: 34,
          file_url: "https://myworld-soundtrack.s3.us-east-2.amazonaws.com/myworld_soundtrack/Same+Sky+(Teen+Girl+Side).mp3"
        },
        {
          song_id: "SSKY_PRNT",
          song_title: "Same Sky (Parent Side)",
          mood_tag: "family",
          playlist_tag: "Family",
          lyrics_snippet: "If I listened with more grace, with less reply, Would your heart stay close instead of saying goodbye?",
          featured: "TRUE",
          featured_order: 35,
          file_url: "https://myworld-soundtrack.s3.us-east-2.amazonaws.com/myworld_soundtrack/Same+Sky+(Rap+Parent+Side).mp3"
        },
        {
          song_id: "SDSC",
          song_title: "Some Days Still Count",
          mood_tag: "lowkey",
          playlist_tag: "Lowkey, Believe",
          lyrics_snippet: "Some days don't shine. But I still keep time. I don't glow, I don't shout. But I still know what I'm about",
          featured: "TRUE",
          featured_order: 37,
          file_url: "https://myworld-soundtrack.s3.us-east-2.amazonaws.com/myworld_soundtrack/Some+Days+Still+Count+(emo).mp3"
        },
        {
          song_id: "AI_RAP_DUET",
          song_title: "We Name the Goal (Duet Rap)",
          mood_tag: "believing, inspiring",
          playlist_tag: "Theme Song, AI and My Future",
          lyrics_snippet: "We shape the world by what we say.",
          featured: "TRUE",
          featured_order: 19,
          file_url: "https://myworld-soundtrack.s3.us-east-2.amazonaws.com/myworld_soundtrack/We+Name+the+Goal+(Two+Voice).mp3"
        },
        {
          song_id: "AI_RAP",
          song_title: "We Name the Goal (Rap)",
          mood_tag: "believing, inspiring",
          playlist_tag: "Theme Song, AI and My Future",
          lyrics_snippet: "We shape the world by what we say.",
          featured: "TRUE",
          featured_order: 20,
          file_url: "https://myworld-soundtrack.s3.us-east-2.amazonaws.com/myworld_soundtrack/We+Name+the+Goal.mp3"
        },
        {
          song_id: "AI_RA_REG",
          song_title: "We Name the Goal (Reggaeton)",
          mood_tag: "believing, inspiring",
          playlist_tag: "Theme Song, AI and My Future",
          lyrics_snippet: "Mi voz, mi mundo, that's my role",
          featured: "TRUE",
          featured_order: 21,
          file_url: "https://myworld-soundtrack.s3.us-east-2.amazonaws.com/myworld_soundtrack/We+Name+the+Goal+(Female+Reggaeton).mp3"
        },
        {
          song_id: "THM_3",
          song_title: "Theme Song (Girl Rap)",
          mood_tag: "rap",
          playlist_tag: "Theme Song",
          lyrics_snippet: "My World, My Say",
          featured: "TRUE",
          featured_order: 16,
          file_url: "https://myworld-soundtrack.s3.us-east-2.amazonaws.com/myworld_soundtrack/Theme+(+Girl+Inspiring+Rap).mp3"
        },
        {
          song_id: "THM_4",
          song_title: "Theme Song (Children Choir)",
          mood_tag: "inspiring",
          playlist_tag: "Theme Song",
          lyrics_snippet: "My World, My Say",
          featured: "TRUE",
          featured_order: 17,
          file_url: "https://myworld-soundtrack.s3.us-east-2.amazonaws.com/myworld_soundtrack/Theme+(Children+Choir).mp3"
        },
        {
          song_id: "THM_5",
          song_title: "Theme Song (Girl HipHop 2)",
          mood_tag: "inspiring",
          playlist_tag: "Theme Song",
          lyrics_snippet: "My World, My Say",
          featured: "TRUE",
          featured_order: 18,
          file_url: "https://myworld-soundtrack.s3.us-east-2.amazonaws.com/myworld_soundtrack/Theme+(Girl+HipHop+2).mp3"
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
