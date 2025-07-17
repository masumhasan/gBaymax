"""
Test script for Baymax text chat functionality

This script demonstrates how to test the text chat feature programmatically.
"""

import asyncio
import logging
from typing import Optional
from livekit import Room, RoomOptions, DataPacket_Kind

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BaymaxTextChatTester:
    def __init__(self, server_url: str, token: str):
        self.server_url = server_url
        self.token = token
        self.room: Optional[Room] = None
        self.connected = False
        self.responses = []
        
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
            
            # Wait for connection
            await asyncio.sleep(2)
            
        except Exception as e:
            logger.error(f"Failed to connect: {e}")
            raise
    
    async def on_connected(self):
        """Handle connection event"""
        self.connected = True
        logger.info("Connected to Baymax room for testing")
    
    async def on_disconnected(self):
        """Handle disconnection event"""
        self.connected = False
        logger.info("Disconnected from Baymax room")
    
    async def on_data_received(self, data, participant):
        """Handle incoming text messages from Baymax"""
        try:
            message = data.decode('utf-8')
            self.responses.append(message)
            logger.info(f"Received: {message}")
        except Exception as e:
            logger.error(f"Error processing received message: {e}")
    
    async def send_message(self, message: str) -> str:
        """Send a test message and wait for response"""
        if not self.connected or not self.room:
            raise Exception("Not connected to room")
        
        try:
            # Clear previous responses
            self.responses.clear()
            
            # Send the message
            data = message.encode('utf-8')
            await self.room.local_participant.publish_data(
                data, 
                kind=DataPacket_Kind.RELIABLE
            )
            logger.info(f"Sent: {message}")
            
            # Wait for response (with timeout)
            timeout = 30  # 30 seconds timeout
            elapsed = 0
            
            while elapsed < timeout:
                if self.responses:
                    return self.responses[-1]  # Return the latest response
                await asyncio.sleep(0.5)
                elapsed += 0.5
            
            raise TimeoutError("No response received within timeout")
            
        except Exception as e:
            logger.error(f"Error sending message: {e}")
            raise
    
    async def disconnect(self):
        """Disconnect from the room"""
        if self.room:
            await self.room.disconnect()
    
    async def run_tests(self):
        """Run a series of test messages"""
        test_cases = [
            {
                "message": "Hello Baymax!",
                "expected_keywords": ["hello", "baymax", "healthcare", "assist"],
                "description": "Basic greeting test"
            },
            {
                "message": "What's the weather like?",
                "expected_keywords": ["weather", "city", "location"],
                "description": "Weather tool test (should ask for location)"
            },
            {
                "message": "Search for Python tutorials",
                "expected_keywords": ["python", "tutorials", "search"],
                "description": "Web search tool test"
            },
            {
                "message": "How are you feeling?",
                "expected_keywords": ["feeling", "health", "scale"],
                "description": "Health-related conversation test"
            }
        ]
        
        results = []
        
        for i, test_case in enumerate(test_cases, 1):
            print(f"\n🧪 Test {i}: {test_case['description']}")
            print(f"📤 Sending: {test_case['message']}")
            
            try:
                response = await self.send_message(test_case['message'])
                print(f"📥 Response: {response}")
                
                # Check if response contains expected keywords
                response_lower = response.lower()
                keywords_found = [
                    keyword for keyword in test_case['expected_keywords']
                    if keyword in response_lower
                ]
                
                result = {
                    "test": test_case['description'],
                    "message": test_case['message'],
                    "response": response,
                    "keywords_found": keywords_found,
                    "passed": len(keywords_found) > 0,
                    "error": None
                }
                
                if result['passed']:
                    print(f"✅ Test passed (found keywords: {keywords_found})")
                else:
                    print(f"⚠️ Test warning (no expected keywords found)")
                
            except Exception as e:
                print(f"❌ Test failed: {e}")
                result = {
                    "test": test_case['description'],
                    "message": test_case['message'],
                    "response": None,
                    "keywords_found": [],
                    "passed": False,
                    "error": str(e)
                }
            
            results.append(result)
            
            # Wait between tests
            await asyncio.sleep(2)
        
        return results
    
    def print_summary(self, results):
        """Print test summary"""
        print("\n" + "="*50)
        print("📊 TEST SUMMARY")
        print("="*50)
        
        passed = sum(1 for r in results if r['passed'])
        total = len(results)
        
        print(f"✅ Passed: {passed}/{total}")
        print(f"❌ Failed: {total - passed}/{total}")
        
        print("\n📝 Detailed Results:")
        for i, result in enumerate(results, 1):
            status = "✅ PASS" if result['passed'] else "❌ FAIL"
            print(f"{i}. {result['test']}: {status}")
            if result['error']:
                print(f"   Error: {result['error']}")
            elif result['keywords_found']:
                print(f"   Keywords found: {result['keywords_found']}")


async def main():
    """Main function to run the text chat tests"""
    print("🧪 Baymax Text Chat Tester")
    print("=" * 40)
    
    # You'll need to update these with your actual server URL and token
    server_url = "ws://localhost:7880"
    token = "your-token-here"
    
    print("⚠️  Note: Make sure to update the server_url and token!")
    print("⚠️  Also ensure your Baymax agent is running before testing.")
    
    tester = BaymaxTextChatTester(server_url, token)
    
    try:
        print("\n🔗 Connecting to Baymax...")
        await tester.connect()
        
        if tester.connected:
            print("✅ Connected successfully!")
            
            print("\n🚀 Running tests...")
            results = await tester.run_tests()
            
            tester.print_summary(results)
        else:
            print("❌ Failed to connect to Baymax")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        
    finally:
        await tester.disconnect()


if __name__ == "__main__":
    print("Starting Baymax Text Chat Tests...")
    asyncio.run(main())
