'use client';

import { useRoomContext, useDataChannel } from '@livekit/components-react';
import { useEffect, useState } from 'react';

const BAYMAX_CHAT_TOPIC = 'baymax-chat';

export default function BaymaxWelcome() {
  const room = useRoomContext();
  const { send } = useDataChannel(BAYMAX_CHAT_TOPIC);
  const [hasSentWelcome, setHasSentWelcome] = useState(false);

  useEffect(() => {
    if (room.state === 'connected' && !hasSentWelcome && send) {
      const welcomeMessage = "Hello! I am Baymax, your personal healthcare companion. How can I help you today?";
      const encoder = new TextEncoder();
      send(encoder.encode(welcomeMessage));
      setHasSentWelcome(true);
    }
  }, [room.state, hasSentWelcome, send]);

  return null;
}
