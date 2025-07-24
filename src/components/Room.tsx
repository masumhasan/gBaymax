'use client';

import { LiveKitRoom, VideoConference } from '@livekit/components-react';
import '@livekit/components-styles';
import '@livekit/components-styles/prefabs/video-conference.css';
import VoiceVisualizer from './VoiceVisualizer';

interface RoomProps {
  token: string;
  serverUrl: string;
}

export default function Room({ token, serverUrl }: RoomProps) {
  return (
    <main className="h-screen w-screen bg-background">
      <LiveKitRoom
        token={token}
        serverUrl={serverUrl}
        connect={true}
        video={true}
        audio={true}
        data-lk-theme="default"
      >
        <div className="flex h-full w-full justify-center items-center">
            <VoiceVisualizer />
        </div>
        <div className="absolute bottom-0 left-0 right-0">
            <VideoConference />
        </div>
      </LiveKitRoom>
    </main>
  );
}
