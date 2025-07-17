"""
Text Chat Example for Baymax Agent

This example demonstrates how to send text messages to the Baymax agent
and receive responses using the LiveKit data channel.
"""

import asyncio
import logging
from livekit import Room, RoomOptions, DataPacket_Kind
from livekit.agents import JobContext

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TextChatClient:
    def __init__(self, server_url: str, token: str):
        self.server_url = server_url
        self.token = token
        self.room = None
        self.connected = False
        
    async def connect(self):
        """Connect to the LiveKit room"""
        try:
            self.room = Room()
            
            # Set up event handlers
            self.room.on("data_received", self.on_data_received)
            self.room.on("connected", self.on_connected)
            self.room.on("disconnected", self.on_disconnected)
            
            # Connect to the room
            await self.room.connect(self.server_url, self.token)
            
        except Exception as e:
            logger.error(f"Failed to connect: {e}")
            raise
    
    async def on_connected(self):
        """Handle connection event"""
        self.connected = True
        logger.info("Connected to room")
        print("✅ Connected to Baymax! You can now send messages.")
    
    async def on_disconnected(self):
        """Handle disconnection event"""
        self.connected = False
        logger.info("Disconnected from room")
        print("❌ Disconnected from Baymax")
    
    async def on_data_received(self, data, participant):
        """Handle incoming text messages from Baymax"""
        try:
            message = data.decode('utf-8')
            if message.startswith("Baymax:"):
                print(f"🤖 {message}")
            else:
                print(f"📨 {message}")
        except Exception as e:
            logger.error(f"Error processing received message: {e}")
    
    async def send_message(self, message: str):
        """Send a text message to Baymax"""
        if not self.connected or not self.room:
            print("❌ Not connected to room")
            return
        
        try:
            # Encode and send the message
            data = message.encode('utf-8')
            await self.room.local_participant.publish_data(
                data, 
                kind=DataPacket_Kind.RELIABLE
            )
            print(f"👤 You: {message}")
            
        except Exception as e:
            logger.error(f"Error sending message: {e}")
            print(f"❌ Failed to send message: {e}")
    
    async def disconnect(self):
        """Disconnect from the room"""
        if self.room:
            await self.room.disconnect()


async def main():
    """Main function to run the text chat client"""
    print("🏥 Baymax Text Chat Client")
    print("=" * 40)
    
    # You'll need to update these with your actual server URL and token
    server_url = "ws://localhost:7880"
    token = "your-token-here"  # Generate this from your LiveKit server
    
    print("⚠️  Note: Make sure to update the server_url and token in the code!")
    print("⚠️  Also ensure your Baymax agent is running before connecting.")
    
    client = TextChatClient(server_url, token)
    
    try:
        # Connect to the room
        await client.connect()
        
        # Interactive chat loop
        print("\n📝 Type your messages below (type 'quit' to exit):")
        print("💡 Try commands like:")
        print("   - 'What's the weather in New York?'")
        print("   - 'Search for Python programming tutorials'")
        print("   - 'Send an email to test@example.com'")
        print("   - 'How are you feeling today?'")
        print()
        
        while True:
            try:
                user_input = input("> ").strip()
                
                if user_input.lower() in ['quit', 'exit', 'q']:
                    print("👋 Goodbye!")
                    break
                
                if user_input:
                    await client.send_message(user_input)
                
                # Small delay to allow response processing
                await asyncio.sleep(0.1)
                
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
            except EOFError:
                print("\n👋 Goodbye!")
                break
    
    except Exception as e:
        logger.error(f"Error in main: {e}")
        print(f"❌ Error: {e}")
    
    finally:
        await client.disconnect()


if __name__ == "__main__":
    asyncio.run(main())
