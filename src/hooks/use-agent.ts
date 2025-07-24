'use client';

import { summarizeConversation } from '@/ai/flows/summarize-conversation';
import { textToSpeech } from '@/ai/flows/text-to-speech';
import { useTracks } from '@livekit/components-react';
import { DataPacket_Kind, LocalParticipant, Track } from 'livekit-client';
import { useCallback, useEffect, useRef, useState } from 'react';

const AGENT_RESPONSE_TOPIC = 'agent-response';
const CHUNK_SIZE = 60000; // 60KB chunks

interface UseAgentOptions {
    sendChat?: (payload: Uint8Array, kind?: DataPacket_Kind) => void;
    sendAudio?: (payload: Uint8Array, kind?: DataPacket_Kind) => void;
}

export function useAgent({ sendChat, sendAudio }: UseAgentOptions) {
    const [isProcessing, setIsProcessing] = useState(false);
    const tracks = useTracks(
        [
            { source: Track.Source.Microphone, withPlaceholder: false },
        ],
        { onlySubscribed: false },
    );

    const localParticipant = tracks.find((track) => track.participant instanceof LocalParticipant)?.participant as LocalParticipant;

    const sendChunkedData = useCallback((data: string, sender: (payload: Uint8Array) => void) => {
        const encoder = new TextEncoder();
        const dataStr = data;
        for (let i = 0; i < dataStr.length; i += CHUNK_SIZE) {
            const chunk = dataStr.substring(i, i + CHUNK_SIZE);
            sender(encoder.encode(chunk));
        }
        // Send an end-of-message marker
        sender(encoder.encode('EOM'));
    }, []);

    const handleTranscription = useCallback(async (text: string) => {
        if (!text.trim() || !sendChat || !sendAudio) return;

        setIsProcessing(true);
        try {
            // 1. Get AI summary
            const { summary } = await summarizeConversation({ conversation: text });
            sendChunkedData(summary, sendChat);

            // 2. Get TTS audio for the summary
            const { audio } = await textToSpeech(summary);
            if (audio) {
                sendChunkedData(audio, sendAudio);
            }
        } catch (error) {
            console.error('Agent processing error:', error);
        } finally {
            setIsProcessing(false);
        }
    }, [sendChat, sendAudio, sendChunkedData]);


    useEffect(() => {
        if (!localParticipant) return;

        // Example of how to simulate user speaking.
        // In a real app this would be driven by a speech-to-text service.
        const simulateUserInput = () => {
             if (localParticipant) {
                // This is a placeholder for a real transcription service.
                // We send a hardcoded message to trigger the agent's response flow.
                const sampleText = "I am not feeling well.";
                handleTranscription(sampleText);
             }
        };
        // After 5 seconds of connecting, simulate the user speaking.
        const timeoutId = setTimeout(simulateUserInput, 7000);


        return () => {
             clearTimeout(timeoutId);
        };

    }, [localParticipant, handleTranscription]);


    return { isProcessing };
}
