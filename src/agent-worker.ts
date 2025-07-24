import {
  DataPacket_Kind,
  RemoteParticipant,
  RemoteTrackPublication,
  Room,
} from 'livekit-server-sdk';
import { RoomEvent, Track } from 'livekit-client';
import { createLivekitToken } from './app/actions';
import { summarizeConversation } from './ai/flows/summarize-conversation';
import { textToSpeech } from './ai/flows/text-to-speech';

const livekitUrl = process.env.LIVEKIT_URL!;

export async function runAgent(roomName: string) {
  const agentToken = await createLivekitToken(roomName, 'agent');
  const room = new Room();

  await room.connect(livekitUrl, agentToken);

  console.log('Agent connected to room', room.name);

  room.on(RoomEvent.TrackSubscribed, (track, publication, participant) => {
    if (track.source === Track.Source.Microphone) {
      // In a real app, you'd use a speech-to-text service here.
      // For this demo, we'll simulate a transcription.
      setTimeout(() => {
        handleTranscription('I am not feeling well.', participant, room);
      }, 2000);
    }
  });
}

async function handleTranscription(
  text: string,
  participant: RemoteParticipant,
  room: Room
) {
  if (!text.trim()) return;

  try {
    const { summary } = await summarizeConversation({ conversation: text });
    sendChunkedData(summary, room, 'baymax-chat');

    // const { audio } = await textToSpeech(summary);
    // if (audio) {
    //   sendChunkedData(audio, room, 'baymax-audio');
    // }
  } catch (error) {
    console.error('Agent processing error:', error);
  }
}

function sendChunkedData(data: string, room: Room, topic: string) {
  const CHUNK_SIZE = 60000;
  const encoder = new TextEncoder();
  for (let i = 0; i < data.length; i += CHUNK_SIZE) {
    const chunk = data.substring(i, i + CHUNK_SIZE);
    room.localParticipant.publishData(encoder.encode(chunk), DataPacket_Kind.RELIABLE, {
      topics: [topic],
    });
  }
  room.localParticipant.publishData(encoder.encode('EOM'), DataPacket_Kind.RELIABLE, {
    topics: [topic],
  });
}
