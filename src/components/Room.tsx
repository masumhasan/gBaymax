'use client';

import { LiveKitRoom, VideoConference } from '@livekit/components-react';
import '@livekit/components-styles';
import '@livekit/components-styles/prefabs/video-conference.css';
import BaymaxAudio from './BaymaxAudio';
import BaymaxDisplay from './BaymaxDisplay';
import BaymaxWelcome from './BaymaxWelcome';

interface RoomProps {
  token: string;
  serverUrl: string;
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
      <VideoConference />
      <BaymaxDisplay />
      <BaymaxWelcome />
      <BaymaxAudio />
    </LiveKitRoom>
  );
}
