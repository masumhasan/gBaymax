from dotenv import load_dotenv

from livekit import agents
from livekit.agents import AgentSession, Agent, RoomInputOptions
from livekit.plugins import (
    noise_cancellation,
)
from livekit.plugins import google
from prompts import AGENT_INSTRUCTION, SESSION_INSTRUCTION
from tools import get_weather, search_web, send_email
from text_chat_handler import TextChatHandler
import logging

load_dotenv()


class Assistant(Agent):
    def __init__(self) -> None:
        super().__init__(
            instructions=AGENT_INSTRUCTION,
            llm=google.beta.realtime.RealtimeModel(
                voice="Aoede",
                temperature=0.8,
            ),
            tools=[
                get_weather,
                search_web,
                send_email
            ],
        )


async def entrypoint(ctx: agents.JobContext):
    # Set up logging
    logging.basicConfig(level=logging.INFO)
    
    # Create session
    session = AgentSession()
    
    # Create assistant
    assistant = Assistant()
    
    # Start the session
    await session.start(
        room=ctx.room,
        agent=assistant,
        room_input_options=RoomInputOptions(
            video_enabled=True,
            noise_cancellation=noise_cancellation.BVC(),
        ),
    )

    await ctx.connect()

    # Create text chat handler
    text_handler = TextChatHandler(assistant, ctx)

    # Handle text messages via data channel
    @ctx.room.on("data_received")
    async def on_data_received(data_event):
        """Handle incoming text messages from data channel"""
        try:
            # Decode the incoming message
            message = data_event.data.decode('utf-8')
            logging.info(f"Received text message: {message}")
            
            # Skip if it's our own message
            if message.startswith("Baymax:"):
                return
            
            # Process the message using the text chat handler
            response = await text_handler.process_message(message)
            
            # Send response back
            await ctx.room.local_participant.publish_data(
                data=f"Baymax: {response}".encode('utf-8'),
                destination=agents.DataDestination.RELIABLE
            )
            
        except Exception as e:
            logging.error(f"Error handling text message: {e}")
            await ctx.room.local_participant.publish_data(
                data="Baymax: I apologize, but I encountered an error processing your message. Please try again.".encode('utf-8'),
                destination=agents.DataDestination.RELIABLE
            )

    # Send initial greeting via text
    await ctx.room.local_participant.publish_data(
        data="Baymax: Hello, I am Baymax, your personal healthcare companion. How can I assist you today?".encode('utf-8'),
        destination=agents.DataDestination.RELIABLE
    )

    # Generate initial voice reply
    await session.generate_reply(
        instructions=SESSION_INSTRUCTION,
    )


if __name__ == "__main__":
    agents.cli.run_app(agents.WorkerOptions(entrypoint_fnc=entrypoint))