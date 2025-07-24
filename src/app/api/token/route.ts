import {NextResponse} from 'next/server';
import {createLivekitToken} from '@/app/actions';

export async function GET() {
  try {
    const roomName = `g-baymax-session-${Math.random().toString(36).substring(2, 9)}`;
    const participantName = `user-${Math.random().toString(36).substring(2, 9)}`;

    const token = await createLivekitToken(roomName, participantName);

    return NextResponse.json({token});
  } catch (error: any) {
    console.error('Error generating token:', error);
    return NextResponse.json(
      {error: error.message || 'Failed to generate token'},
      {status: 500}
    );
  }
}
