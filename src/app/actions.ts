'use server';

import { AccessToken } from 'livekit-server-sdk';
import { z } from 'zod';

const joinRoomSchema = z.object({
  roomName: z.string().min(1, 'Room name is required'),
});

export async function generateToken(values: { roomName: string }) {
  const result = joinRoomSchema.safeParse(values);

  if (!result.success) {
    return { error: result.error.flatten().fieldErrors };
  }

  const apiKey = process.env.LIVEKIT_API_KEY;
  const apiSecret = process.env.LIVEKIT_API_SECRET;

  if (!apiKey || !apiSecret) {
    console.error('LiveKit API Key or Secret not set.');
    return { error: 'Server configuration error.' };
  }

  const { roomName } = result.data;
  const participantName = `user-${Math.random().toString(36).substring(2, 9)}`;

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

  return { token: at.toJwt() };
}
