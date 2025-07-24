# **App Name**: gBaymax

## Core Features:

- Join Room Input: Simple text input to specify the room name to join.
- Join Button: Button to submit the form and join the specified room, triggering connection to LiveKit.
- LiveKit Connection: Connect to the LiveKit room with the user-provided room name and credentials (LIVEKIT_URL, LIVEKIT_API_KEY, LIVEKIT_API_SECRET) from .env.local.
- Audio/Video Activation: Enable microphone and video upon joining the room to initiate real-time voice chat.
- Baymax Response UI: Display a floating UI to present Baymax's responses, received from LiveKit Agent.
- AI-Powered Chat: The AI tool responds in the form of streaming agent output.

## Style Guidelines:

- Primary color: Gentle blue (#64B5F6), reminiscent of Baymax's caring and supportive nature.
- Background color: Very light blue (#E3F2FD), for a calming and friendly interface.
- Accent color: Soft green (#81C784), suggesting health and assistance, to highlight interactive elements.
- Font: 'PT Sans', sans-serif, for clear and accessible UI elements and readability.
- Simple, clean layout with input fields at the top and floating output display from Livekit Agent at the bottom.