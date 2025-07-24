'use client';

import { useEffect, useState } from 'react';
import { useRoomContext } from '@livekit/components-react';

export default function VoiceVisualizer() {
    const room = useRoomContext();
    const [audioLevel, setAudioLevel] = useState(0);

    useEffect(() => {
        if (!room) {
            return;
        }

        const baymaxParticipant = Array.from(room.participants.values()).find(p => p.identity === 'Baymax');

        if (!baymaxParticipant) {
            setAudioLevel(0);
            return;
        }

        const onAudioLevelChanged = (level: number) => {
            setAudioLevel(level);
        };

        const onTrackSubscribed = (track: any) => {
            if (track.kind === 'audio') {
                track.on('audioLevelChanged', onAudioLevelChanged);
            }
        };

        baymaxParticipant.on('audioLevelChanged', onAudioLevelChanged);
        baymaxParticipant.on('trackSubscribed', onTrackSubscribed);

        return () => {
            baymaxParticipant.off('audioLevelChanged', onAudioLevelChanged);
            baymaxParticipant.off('trackSubscribed', onTrackSubscribed);
        };
    }, [room, room.participants]);

    const animationState = audioLevel > 0.05 ? 'speaking' : 'idle';

    return (
        <div className="relative flex h-[320px] w-[350px] items-center justify-center">
            <div
                id="container"
                className={`relative flex h-full w-full items-center justify-center`}
            >
                <span className={`blue absolute h-[50px] w-[50px] rounded-full bg-black/80 transition-all`} style={{ animation: animationState === 'speaking' ? 'sound-1 1.4s infinite' : 'updown 1.2s infinite ease-in-out alternate', left: 0 }}></span>
                <span className={`blue-2 absolute h-[50px] w-[50px] rounded-full bg-black/80 transition-all`} style={{ animation: animationState === 'speaking' ? 'sound-2 1.4s 0.25s infinite' : 'updown 1.2s 0.2s infinite ease-in-out alternate', left: '100px' }}></span>
                <span className={`blue-3 absolute h-[50px] w-[50px] rounded-full bg-black/80 transition-all`} style={{ animation: animationState === 'speaking' ? 'sound-1 1.4s 0.10s infinite' : 'updown 1.2s 0.4s infinite ease-in-out alternate', left: '200px' }}></span>
                <span className={`blue-4 absolute h-[50px] w-[50px] rounded-full bg-black/80 transition-all`} style={{ animation: animationState === 'speaking' ? 'sound-2 1.4s 0.15s infinite' : 'updown 1.2s 0.6s infinite ease-in-out alternate', left: '300px' }}></span>
            </div>
        </div>
    );
}
