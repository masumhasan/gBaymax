'use server';

import { AccessToken } from 'livekit-server-sdk';

export async function createLivekitToken(roomName: string, participantName: string) {
  const apiKey = process.env.LIVEKIT_API_KEY;
  const apiSecret = process.env.LIVEKIT_API_SECRET;

  if (!apiKey || !apiSecret) {
    console.error('LiveKit API Key or Secret not set.');
    throw new Error('Server configuration error: LiveKit credentials not set.');
  }

  const at = new AccessToken(apiKey, apiSecret, {
    identity: participantName,
    name: "User",
    ttl: '10m',
  });

  at.addGrant({
    room: roomName,
    roomJoin: true,
    canPublish: true,
    canSubscribe: true,
  });

  return at.toJwt();
}
