'use client';

import { textToSpeech } from '@/ai/flows/text-to-speech';
import { useRoomContext, useDataChannel } from '@livekit/components-react';
import { useEffect, useState } from 'react';

const BAYMAX_CHAT_TOPIC = 'baymax-chat';
const BAYMAX_AUDIO_TOPIC = 'baymax-audio';

export default function BaymaxWelcome() {
  const room = useRoomContext();
  const { send: sendChat } = useDataChannel(BAYMAX_CHAT_TOPIC);
  const { send: sendAudio } = useDataChannel(BAYMAX_AUDIO_TOPIC);
  const [hasSentWelcome, setHasSentWelcome] = useState(false);

  useEffect(() => {
    if (room.state === 'connected' && !hasSentWelcome && sendChat && sendAudio) {
      const welcomeMessage = "Hello! I am Baymax, your personal healthcare companion. How can I help you today?";
      const encoder = new TextEncoder();
      
      // Send the text message
      sendChat(encoder.encode(welcomeMessage));
      
      // Generate and send the audio message
      textToSpeech(welcomeMessage).then(response => {
        if (response.audio) {
            sendAudio(encoder.encode(response.audio))
        }
      }).catch(e => console.error("TTS Error:", e));

      setHasSentWelcome(true);
    }
  }, [room.state, hasSentWelcome, sendChat, sendAudio]);

  return null;
}
