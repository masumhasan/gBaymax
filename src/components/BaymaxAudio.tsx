'use client';

import { useDataChannel } from '@livekit/components-react';
import { useEffect, useMemo, useRef, useState } from 'react';

const BAYMAX_AUDIO_TOPIC = 'baymax-audio';

export default function BaymaxAudio() {
  const audioRef = useRef<HTMLAudioElement>(null);
  const [audioData, setAudioData] = useState('');
  const [isReceiving, setIsReceiving] = useState(false);
  
  const { publishedMessages } = useDataChannel(BAYMAX_AUDIO_TOPIC);
  const decoder = useMemo(() => new TextDecoder(), []);

  useEffect(() => {
    if (!publishedMessages || publishedMessages.length === 0) return;

    const lastMessage = publishedMessages[publishedMessages.length - 1];
    const decodedMessage = decoder.decode(lastMessage.payload);

    if (decodedMessage === 'EOM') {
      setIsReceiving(false);
    } else {
        if (!isReceiving) {
            // Start of a new message
            setAudioData(decodedMessage);
        } else {
            // Appending chunks
            setAudioData(prev => prev + decodedMessage);
        }
        setIsReceiving(true);
    }
  }, [publishedMessages, decoder, isReceiving]);

  useEffect(() => {
    if (!isReceiving && audioData && audioRef.current) {
      audioRef.current.src = audioData;
      audioRef.current.play().catch((e) => console.error('Audio play failed:', e));
      // Clear data after playing
      setAudioData('');
    }
  }, [isReceiving, audioData]);

  return <audio ref={audioRef} />;
}
