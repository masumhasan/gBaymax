'use client';

import { useRoomContext, useDataChannel } from '@livekit/components-react';
import { useEffect, useState } from 'react';
import { RoomEvent } from 'livekit-client';

const BAYMAX_CHAT_TOPIC = 'baymax-chat';

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
      const encoder = new TextEncoder();
      send(encoder.encode(welcomeMessage));
      setHasSentWelcome(true);
    }
  }, [isConnected, hasSentWelcome, send]);

  return null;
}
