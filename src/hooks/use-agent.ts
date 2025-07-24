
'use client';

import { summarizeConversation } from '@/ai/flows/summarize-conversation';
import { textToSpeech } from '@/ai/flows/text-to-speech';
import { useTracks } from '@livekit/components-react';
import { DataPacket_Kind, LocalParticipant, Track } from 'livekit-client';
import { useCallback, useEffect, useRef, useState } from 'react';

const AGENT_RESPONSE_TOPIC = 'agent-response';

interface UseAgentOptions {
    sendChat?: (payload: Uint8Array, kind?: DataPacket_Kind) => void;
    sendAudio?: (payload: Uint8Array, kind?: DataPacket_Kind) => void;
}

export function useAgent({ sendChat, sendAudio }: UseAgentOptions) {
    const [isProcessing, setIsProcessing] = useState(false);
    const audioRef = useRef<HTMLAudioElement>(null);
    const tracks = useTracks(
        [
            { source: Track.Source.Microphone, withPlaceholder: false },
        ],
        { onlySubscribed: false },
    );

    const localParticipant = tracks.find((track) => track.participant instanceof LocalParticipant)?.participant as LocalParticipant;

    const handleTranscription = useCallback(async (text: string) => {
        if (!text.trim() || !sendChat || !sendAudio) return;

        setIsProcessing(true);
        try {
            const encoder = new TextEncoder();
            
            // 1. Get AI summary
            const { summary } = await summarizeConversation({ conversation: text });
            sendChat(encoder.encode(summary));

            // 2. Get TTS audio for the summary
            const { audio } = await textToSpeech(summary);
            if (audio && audioRef.current) {
                sendAudio(encoder.encode(audio));
            }
        } catch (error) {
            console.error('Agent processing error:', error);
        } finally {
            setIsProcessing(false);
        }
    }, [sendChat, sendAudio]);


    useEffect(() => {
        if (!localParticipant) return;

        const handleData = (payload: Uint8Array) => {
            const text = new TextDecoder().decode(payload);
            handleTranscription(text);
        };

        localParticipant.on('trackSubscribed', (track) => {
            if (track.source === Track.Source.Microphone) {
                 // This is where real-time transcription would happen.
                 // For this example, we'll simulate it with a simple data channel message.
                 // In a real app, you would use a speech-to-text service.
            }
        });
        
        // Example of how to simulate user speaking.
        // In a real app this would be driven by a speech-to-text service.
        const simulateUserInput = () => {
             if (localParticipant) {
                // This is a placeholder for a real transcription service.
                // We send a hardcoded message to trigger the agent's response flow.
                const sampleText = "I have a headache and a fever.";
                handleTranscription(sampleText);
             }
        };
        // After 5 seconds of connecting, simulate the user speaking.
        const timeoutId = setTimeout(simulateUserInput, 7000);


        return () => {
             clearTimeout(timeoutId);
        };

    }, [localParticipant, handleTranscription]);


    return { isProcessing, audioRef };
}
