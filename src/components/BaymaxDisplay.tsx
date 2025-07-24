'use client';

import { useDataChannel } from '@livekit/components-react';
import { useMemo } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Bot } from 'lucide-react';
import { ScrollArea } from './ui/scroll-area';

const BAYMAX_CHAT_TOPIC = 'baymax-chat';

export default function BaymaxDisplay() {
  const { publishedMessages } = useDataChannel(BAYMAX_CHAT_TOPIC);
  const decoder = useMemo(() => new TextDecoder(), []);

  const fullText = useMemo(() => {
    return (publishedMessages || []).map((msg) => decoder.decode(msg.payload)).join('');
  }, [publishedMessages, decoder]);

  if (!fullText) {
    return (
      <div className="fixed bottom-4 left-4 right-4 md:left-auto md:max-w-md z-50 pointer-events-none">
        <Card className="bg-background/80 backdrop-blur-sm shadow-2xl pointer-events-auto">
          <CardHeader className="flex flex-row items-center space-x-3 pb-2">
            <div className="p-2 bg-primary rounded-full">
              <Bot className="h-6 w-6 text-primary-foreground" />
            </div>
            <CardTitle className="font-headline text-primary">Baymax</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-foreground whitespace-pre-wrap">...</p>
          </CardContent>
        </Card>
      </div>
    );
  }

  return (
    <div className="fixed bottom-4 left-4 right-4 md:left-auto md:max-w-md z-50 pointer-events-none">
      <Card className="bg-background/80 backdrop-blur-sm shadow-2xl pointer-events-auto">
        <CardHeader className="flex flex-row items-center space-x-3 pb-2">
          <div className="p-2 bg-primary rounded-full">
            <Bot className="h-6 w-6 text-primary-foreground" />
          </div>
          <CardTitle className="font-headline text-primary">Baymax</CardTitle>
        </CardHeader>
        <CardContent>
          <ScrollArea className="h-full max-h-48 pr-4">
            <p className="text-foreground whitespace-pre-wrap">{fullText}</p>
          </ScrollArea>
        </CardContent>
      </Card>
    </div>
  );
}
