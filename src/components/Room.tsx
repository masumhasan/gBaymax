'use client';

import {
  LiveKitRoom,
  VideoConference,
  useDataChannel,
} from '@livekit/components-react';
import '@livekit/components-styles';
import '@livekit/components-styles/prefabs/video-conference.css';
import BaymaxAudio from './BaymaxAudio';
import BaymaxDisplay from './BaymaxDisplay';
import BaymaxWelcome from './BaymaxWelcome';
import { useAgent } from '@/hooks/use-agent';

interface RoomProps {
  token: string;
  serverUrl: string;
}

const BAYMAX_CHAT_TOPIC = 'baymax-chat';
const BAYMAX_AUDIO_TOPIC = 'baymax-audio';

function RoomContent() {
  const { send: sendChat } = useDataChannel(BAYMAX_CHAT_TOPIC);
  const { send: sendAudio } = useDataChannel(BAYMAX_AUDIO_TOPIC);
  
  useAgent({
    sendAudio: sendAudio,
    sendChat: sendChat,
  });

  return (
    <>
      <VideoConference />
      <BaymaxDisplay />
      <BaymaxWelcome />
      <BaymaxAudio />
    </>
  );
}

export default function Room({ token, serverUrl }: RoomProps) {
  return (
    <LiveKitRoom
      token={token}
      serverUrl={serverUrl}
      connect={true}
      video={true}
      audio={true}
      data-lk-theme="default"
      style={{ height: '100dvh' }}
    >
      <RoomContent />
    </LiveKitRoom>
  );
}
