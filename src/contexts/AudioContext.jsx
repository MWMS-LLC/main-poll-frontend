import React, { createContext, useContext, useRef, useState, useEffect, useCallback } from 'react'

const AudioContext = createContext()

export const useAudio = () => {
  const context = useContext(AudioContext)
  if (!context) {
    throw new Error('useAudio must be used within an AudioProvider')
  }
  return context
}

export const AudioProvider = ({ children }) => {
  const audioRef = useRef(null)
  const [currentSong, setCurrentSong] = useState(null)
  const [isPlaying, setIsPlaying] = useState(false)
  const [currentTime, setCurrentTime] = useState(0)
  const [duration, setDuration] = useState(0)
  const [volume, setVolume] = useState(1)
  const [playlist, setPlaylist] = useState([])
  const [currentSongIndex, setCurrentSongIndex] = useState(0)

  // Define playlist functions first
  const setPlaylistSongs = (songs) => {
    setPlaylist(songs)
    setCurrentSongIndex(0)
  }



  const playNextSong = useCallback(() => {
    if (playlist.length === 0) {
      console.log('❌ No playlist available for auto-continue')
      return
    }
    
    console.log('🔄 Auto-continuing to next song...')
    console.log('Current index:', currentSongIndex, 'Playlist length:', playlist.length)
    
    const nextIndex = (currentSongIndex + 1) % playlist.length
    console.log('Next index:', nextIndex)
    
    setCurrentSongIndex(nextIndex)
    const nextSong = playlist[nextIndex]
    console.log('Next song:', nextSong.title)
    
    setCurrentSong(nextSong)
    
    // Play the next song
    if (audioRef.current) {
      audioRef.current.src = nextSong.fileUrl
      audioRef.current.load()
      audioRef.current.play().then(() => {
        console.log('✅ Next song started playing:', nextSong.title)
        setIsPlaying(true)
        setCurrentTime(0)
      }).catch(error => {
        console.error('❌ Error playing next song:', error)
        setIsPlaying(false)
      })
    }
  }, [playlist, currentSongIndex])

  const playPreviousSong = () => {
    if (playlist.length === 0) return
    
    const prevIndex = currentSongIndex === 0 ? playlist.length - 1 : currentSongIndex - 1
    setCurrentSongIndex(prevIndex)
    const prevSong = playlist[prevIndex]
    setCurrentSong(prevSong)
    
    // Play the previous song
    if (audioRef.current) {
      audioRef.current.src = prevSong.fileUrl
      audioRef.current.load()
      audioRef.current.play().then(() => {
        setIsPlaying(true)
        setCurrentTime(0)
      }).catch(error => {
        console.error('Error playing previous song:', error)
        setIsPlaying(false)
      })
    }
  }

  useEffect(() => {
    const audio = audioRef.current
    if (!audio) return

    const handleTimeUpdate = () => setCurrentTime(audio.currentTime)
    const handleLoadedMetadata = () => setDuration(audio.duration)
    const handleEnded = () => {
      console.log('🎵 Song ended, attempting to play next...')
      setIsPlaying(false)
      setCurrentTime(0)
      // Auto-play next song in playlist with a small delay to ensure state is updated
      setTimeout(() => {
        playNextSong()
      }, 100)
    }
    const handleCanPlay = () => {
      console.log('Audio can play now')
    }
    const handleError = (e) => {
      console.error('Audio error:', e)
      setIsPlaying(false)
    }

    audio.addEventListener('timeupdate', handleTimeUpdate)
    audio.addEventListener('loadedmetadata', handleLoadedMetadata)
    audio.addEventListener('ended', handleEnded)
    audio.addEventListener('canplay', handleCanPlay)
    audio.addEventListener('error', handleError)

    return () => {
      audio.removeEventListener('timeupdate', handleTimeUpdate)
      audio.removeEventListener('loadedmetadata', handleLoadedMetadata)
      audio.removeEventListener('ended', handleEnded)
      audio.removeEventListener('canplay', handleCanPlay)
      audio.removeEventListener('error', handleError)
    }
  }, [playNextSong])

  const playSong = (song, songList = []) => {
    if (!audioRef.current) return
    
    console.log('🎵 playSong called with:', song.title, 'Playlist length:', songList.length)
    
    // Stop any currently playing audio first
    audioRef.current.pause()
    audioRef.current.currentTime = 0
    audioRef.current.src = ''
    
    setCurrentSong(song)
    setIsPlaying(false)
    
    // Set playlist if provided
    if (songList.length > 0) {
      console.log('🎵 Setting up playlist with', songList.length, 'songs')
      console.log('Playlist songs:', songList.map(s => ({ id: s.id, title: s.title })))
      console.log('Current song:', { id: song.id, title: song.title })
      
      setPlaylist(songList)
      
      // Find the index of the current song in the playlist
      const songIndex = songList.findIndex(s => s.id === song.id)
      console.log('Current song ID:', song.id, 'Found at index:', songIndex)
      
      setCurrentSongIndex(songIndex >= 0 ? songIndex : 0)
      console.log('Set current song index to:', songIndex >= 0 ? songIndex : 0)
    } else {
      console.log('⚠️ No playlist provided, auto-continue disabled')
    }
    
    if (audioRef.current) {
      console.log('Setting audio src to:', song.fileUrl)
      audioRef.current.src = song.fileUrl
      audioRef.current.volume = volume
      audioRef.current.muted = false
      audioRef.current.load()
      
      // Try to play immediately
      if (audioRef.current && audioRef.current.src === song.fileUrl) {
        audioRef.current.play().then(() => {
          console.log('✅ Song started playing immediately!')
          setIsPlaying(true)
        }).catch(immediateError => {
          console.log('Immediate play failed, trying delayed play...', immediateError)
          
          // Try delayed play as fallback
          setTimeout(() => {
            if (audioRef.current && audioRef.current.src === song.fileUrl) {
              audioRef.current.play().then(() => {
                console.log('✅ Song started playing after delay!')
                setIsPlaying(true)
              }).catch(delayedError => {
                console.error('❌ Delayed play also failed:', delayedError)
                setIsPlaying(false)
              })
            }
          }, 200)
        })
      }
    }
  }

  const togglePlayPause = () => {
    if (!currentSong || !audioRef.current) return
    
    if (isPlaying) {
      audioRef.current.pause()
      setIsPlaying(false)
    } else {
      if (audioRef.current.readyState === 0) {
        audioRef.current.load()
      }
      
      audioRef.current.play().then(() => {
        setIsPlaying(true)
      }).catch(error => {
        console.error('Error playing audio:', error)
        setIsPlaying(false)
        // Try to reload and play again
        audioRef.current.load()
        audioRef.current.play().then(() => {
          setIsPlaying(true)
        }).catch(retryError => {
          console.error('Retry failed:', retryError)
        })
      })
    }
  }

  const setVolumeLevel = (newVolume) => {
    setVolume(newVolume)
    if (audioRef.current) {
      audioRef.current.volume = newVolume
    }
  }

  const seekTo = (time) => {
    if (audioRef.current && duration > 0) {
      audioRef.current.currentTime = time
      setCurrentTime(time)
    }
  }



  const value = {
    audioRef,
    currentSong,
    isPlaying,
    currentTime,
    duration,
    volume,
    playlist,
    currentSongIndex,
    playSong,
    togglePlayPause,
    setVolumeLevel,
    seekTo,
    setPlaylistSongs,
    playNextSong,
    playPreviousSong
  }

  return (
    <AudioContext.Provider value={value}>
      {/* Hidden audio element that persists across page navigation */}
      <audio 
        ref={audioRef} 
        preload="metadata" 
        style={{display: 'none'}}
        volume={volume}
        muted={false}
      />
      {children}
    </AudioContext.Provider>
  )
}
