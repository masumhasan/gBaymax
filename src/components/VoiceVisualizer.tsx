'use client';

import { useEffect, useState } from 'react';
import { useRoomContext } from '@livekit/components-react';
import { RemoteParticipant } from 'livekit-client';

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

        baymaxParticipant.on('audioLevelChanged', onAudioLevelChanged);
        baymaxParticipant.on('trackSubscribed', (track) => {
            if (track.kind === 'audio') {
                track.on('audioLevelChanged', onAudioLevelChanged);
            }
        });

        return () => {
            baymaxParticipant.off('audioLevelChanged', onAudioLevelChanged);
        };
    }, [room, room.participants]);

    const animationState = audioLevel > 0.05 ? 'speaking' : 'idle';

    return (
        <div className="relative flex h-64 w-64 items-center justify-center rounded-full bg-primary/20">
            <div
                id="container"
                className={`relative flex h-full w-full items-center justify-center ${animationState}`}
            >
                <span className="blue absolute h-12 w-12 rounded-full bg-black/80 transition-all" style={{ left: 'calc(50% - 100px - 25px)' }}></span>
                <span className="blue-2 absolute h-12 w-12 rounded-full bg-black/80 transition-all" style={{ left: 'calc(50% - 50px - 25px)' }}></span>
                <span className="blue-3 absolute h-12 w-12 rounded-full bg-black/80 transition-all" style={{ left: 'calc(50% + 50px - 25px)' }}></span>
                <span className="blue-4 absolute h-12 w-12 rounded-full bg-black/80 transition-all" style={{ left: 'calc(50% + 100px - 25px)' }}></span>
            </div>
            <style jsx>{`
              .speaking .blue { animation: sound-1 1.4s infinite; }
              .speaking .blue-2 { animation: sound-2 1.4s 0.25s infinite; }
              .speaking .blue-3 { animation: sound-1 1.4s 0.10s infinite; }
              .speaking .blue-4 { animation: sound-2 1.4s 0.15s infinite; }
              
              .idle .blue { animation: updown 1.2s infinite ease-in-out alternate; }
              .idle .blue-2 { animation: updown 1.2s 0.2s infinite ease-in-out alternate; }
              .idle .blue-3 { animation: updown 1.2s 0.4s infinite ease-in-out alternate; }
              .idle .blue-4 { animation: updown 1.2s 0.6s infinite ease-in-out alternate; }
            `}</style>
        </div>
    );
}
