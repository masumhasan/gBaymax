'use client';

import { useDataChannel } from '@livekit/components-react';
import { useEffect, useMemo, useRef } from 'react';

const BAYMAX_AUDIO_TOPIC = 'baymax-audio';

export default function BaymaxAudio() {
  const audioRef = useRef<HTMLAudioElement>(null);
  const { publishedMessages } = useDataChannel(BAYMAX_AUDIO_TOPIC);
  const decoder = useMemo(() => new TextDecoder(), []);

  useEffect(() => {
    if (publishedMessages && publishedMessages.length > 0) {
      const lastMessage = publishedMessages[publishedMessages.length - 1];
      const audioData = decoder.decode(lastMessage.payload);
      if (audioRef.current) {
        audioRef.current.src = audioData;
        audioRef.current.play().catch((e) => console.error('Audio play failed:', e));
      }
    }
  }, [publishedMessages, decoder]);

  return <audio ref={audioRef} />;
}
