'use client';

import { textToSpeech } from '@/ai/flows/text-to-speech';
import { useRoomContext, useDataChannel } from '@livekit/components-react';
import { useEffect, useState, useCallback } from 'react';

const BAYMAX_CHAT_TOPIC = 'baymax-chat';
const BAYMAX_AUDIO_TOPIC = 'baymax-audio';
const CHUNK_SIZE = 60000; // 60KB chunks

export default function BaymaxWelcome() {
  const room = useRoomContext();
  const { send: sendChat } = useDataChannel(BAYMAX_CHAT_TOPIC);
  const { send: sendAudio } = useDataChannel(BAYMAX_AUDIO_TOPIC);
  const [hasSentWelcome, setHasSentWelcome] = useState(false);

  const sendChunkedData = useCallback((data: string, sender: (payload: Uint8Array) => void) => {
    const encoder = new TextEncoder();
    for (let i = 0; i < data.length; i += CHUNK_SIZE) {
        const chunk = data.substring(i, i + CHUNK_SIZE);
        sender(encoder.encode(chunk));
    }
    sender(encoder.encode('EOM')); // End-of-message marker
  }, []);

  useEffect(() => {
    if (room.state === 'connected' && !hasSentWelcome && sendChat && sendAudio) {
      const welcomeMessage = "Hello! I am Baymax, your personal healthcare companion. How can I help you today?";
      
      // Send the text message
      sendChunkedData(welcomeMessage, sendChat);
      
      // Generate and send the audio message
      textToSpeech(welcomeMessage).then(response => {
        if (response.audio) {
            sendChunkedData(response.audio, sendAudio);
        }
      }).catch(e => console.error("TTS Error:", e));

      setHasSentWelcome(true);
    }
  }, [room.state, hasSentWelcome, sendChat, sendAudio, sendChunkedData]);

  return null;
}
