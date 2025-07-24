'use client';

import { useState } from 'react';
import { generateToken } from '@/app/actions';
import Room from '@/components/Room';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { useToast } from "@/hooks/use-toast";
import { Loader2 } from 'lucide-react';

export default function Home() {
  const [token, setToken] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const { toast } = useToast();

  const handleJoinRoom = async () => {
    setIsLoading(true);
    try {
      // Generate a random room name
      const roomName = `g-baymax-session-${Math.random().toString(36).substring(2, 9)}`;
      const result = await generateToken({ roomName });
      
      if (result.error) {
        toast({
          title: "Error joining room",
          description: typeof result.error === 'string' ? result.error : JSON.stringify(result.error),
          variant: "destructive",
        });
      } else if (result.token) {
        setToken(result.token);
      }
    } catch (error) {
       toast({
        title: "An unexpected error occurred",
        description: "Please check the server logs.",
        variant: "destructive",
      });
    } finally {
      setIsLoading(false);
    }
  };

  const serverUrl = process.env.NEXT_PUBLIC_LIVEKIT_URL;

  if (token) {
    if (!serverUrl) {
      return (
        <div className="flex h-screen items-center justify-center bg-destructive text-destructive-foreground p-4">
          LiveKit URL is not configured. Please set NEXT_PUBLIC_LIVEKIT_URL in your .env.local file.
        </div>
      );
    }
    return <Room token={token} serverUrl={serverUrl} />;
  }

  return (
      <main className="flex min-h-screen flex-col items-center justify-center p-4 bg-background">
        <Card className="w-full max-w-md shadow-lg border-2 border-primary/20">
          <CardHeader>
            <CardTitle className="text-3xl font-headline text-center text-primary-foreground bg-primary -mx-6 px-6 py-4 rounded-t-lg -mt-6">gBaymax</CardTitle>
            <CardDescription className="text-center pt-4">
              Start a session with your personal healthcare companion.
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="flex justify-center">
              <Button onClick={handleJoinRoom} className="w-full bg-accent hover:bg-accent/90 text-accent-foreground" disabled={isLoading}>
                {isLoading ? <Loader2 className="animate-spin" /> : "Start Session"}
              </Button>
            </div>
          </CardContent>
        </Card>
      </main>
  );
}
