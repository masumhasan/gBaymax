'use client';

import { useRoomContext, useDataChannel } from '@livekit/components-react';
import { useEffect, useState } from 'react';
import { RoomEvent } from 'livekit-client';

const BAYMAX_CHAT_TOPIC = 'baymax-chat';
const BAYMAX_TYPING_SPEED = 100; // ms per word

export default function BaymaxWelcome() {
  const room = useRoomContext();
  const { send } = useDataChannel(BAYMAX_CHAT_TOPIC);
  const [hasSentWelcome, setHasSentWelcome] = useState(false);
  const [isConnected, setIsConnected] = useState(false);

  useEffect(() => {
    const onConnected = () => setIsConnected(true);
    const onDisconnected = () => setIsConnected(false);

    room.on(RoomEvent.Connected, onConnected);
    room.on(RoomEvent.Disconnected, onDisconnected);
    
    // Set initial state
    if (room.state === 'connected') {
      setIsConnected(true);
    }

    return () => {
      room.off(RoomEvent.Connected, onConnected);
      room.off(RoomEvent.Disconnected, onDisconnected);
    };
  }, [room]);

  useEffect(() => {
    if (isConnected && !hasSentWelcome && send) {
      const welcomeMessage = "Hello! I am Baymax, your personal healthcare companion. How can I help you today?";
      const words = welcomeMessage.split(' ');
      const encoder = new TextEncoder();

      let wordIndex = 0;
      const typeWord = () => {
        if (wordIndex < words.length) {
          const word = words[wordIndex];
          // Add a space before the word, except for the first word.
          const messageToSend = wordIndex === 0 ? word : ` ${word}`;
          send(encoder.encode(messageToSend));
          wordIndex++;
          setTimeout(typeWord, BAYMAX_TYPING_SPEED);
        }
      };

      typeWord();
      setHasSentWelcome(true);
    }
  }, [isConnected, hasSentWelcome, send]);

  return null;
}
