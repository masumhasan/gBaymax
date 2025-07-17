"""
Enhanced text chat handler with tool support

This module provides enhanced text chat functionality that can invoke tools
like weather, web search, and email sending based on text input.
"""

import asyncio
import logging
import re
from typing import Optional, Dict, Any
from livekit import agents
from tools import get_weather, search_web, send_email

logger = logging.getLogger(__name__)


class TextChatHandler:
    """Handles text chat messages and tool invocation"""
    
    def __init__(self, assistant, context: agents.JobContext):
        self.assistant = assistant
        self.context = context
        self.tools = {
            'weather': get_weather,
            'search': search_web,
            'email': send_email
        }
    
    async def process_message(self, message: str) -> str:
        """Process a text message and return a response"""
        try:
            # Check if the message requires a tool
            tool_response = await self._check_and_invoke_tools(message)
            if tool_response:
                return tool_response
            
            # Generate a conversational response
            return await self._generate_conversational_response(message)
            
        except Exception as e:
            logger.error(f"Error processing message: {e}")
            return "I apologize, but I encountered an error processing your message. Please try again."
    
    async def _check_and_invoke_tools(self, message: str) -> Optional[str]:
        """Check if the message requires a tool and invoke it if needed"""
        message_lower = message.lower()
        
        # Weather tool
        if any(keyword in message_lower for keyword in ['weather', 'temperature', 'forecast']):
            return await self._handle_weather_request(message)
        
        # Search tool
        if any(keyword in message_lower for keyword in ['search', 'find', 'look up', 'google']):
            return await self._handle_search_request(message)
        
        # Email tool
        if any(keyword in message_lower for keyword in ['email', 'send', 'mail']):
            return await self._handle_email_request(message)
        
        return None
    
    async def _handle_weather_request(self, message: str) -> str:
        """Handle weather-related requests"""
        try:
            # Try to extract city name from the message
            city = self._extract_city_from_message(message)
            
            if not city:
                return "I'd be happy to check the weather for you! Please specify a city name. For example: 'What's the weather in New York?'"
            
            # Call the weather tool
            weather_result = await get_weather(self.context, city)
            return f"Here's the weather information for {city}: {weather_result}"
            
        except Exception as e:
            logger.error(f"Error handling weather request: {e}")
            return "I apologize, but I couldn't retrieve the weather information at the moment. Please try again."
    
    async def _handle_search_request(self, message: str) -> str:
        """Handle search-related requests"""
        try:
            # Extract search query from the message
            search_query = self._extract_search_query(message)
            
            if not search_query:
                return "I'd be happy to search the web for you! Please specify what you'd like me to search for."
            
            # Call the search tool
            search_result = await search_web(self.context, search_query)
            return f"Here are the search results for '{search_query}':\n\n{search_result}"
            
        except Exception as e:
            logger.error(f"Error handling search request: {e}")
            return "I apologize, but I couldn't perform the search at the moment. Please try again."
    
    async def _handle_email_request(self, message: str) -> str:
        """Handle email-related requests"""
        try:
            # For email, we need more structured input
            # This is a basic implementation - in a real scenario, you'd want more sophisticated parsing
            
            if "@" in message:
                # Try to extract email components
                email_parts = self._extract_email_parts(message)
                if email_parts and all(email_parts.values()):
                    result = await send_email(
                        self.context,
                        email_parts['to'],
                        email_parts['subject'],
                        email_parts['body']
                    )
                    return f"Email processing result: {result}"
            
            return """I can help you send emails! Please provide the details in this format:
"Send an email to user@example.com with subject 'Your Subject' and message 'Your message here'"

Or provide the recipient email, subject, and message separately."""
            
        except Exception as e:
            logger.error(f"Error handling email request: {e}")
            return "I apologize, but I couldn't process the email request at the moment. Please try again."
    
    def _extract_city_from_message(self, message: str) -> Optional[str]:
        """Extract city name from weather-related messages"""
        # Look for patterns like "weather in [city]" or "weather [city]"
        patterns = [
            r'weather\s+in\s+([a-zA-Z\s]+)',
            r'weather\s+([a-zA-Z\s]+)',
            r'in\s+([a-zA-Z\s]+)',
            r'for\s+([a-zA-Z\s]+)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, message.lower())
            if match:
                city = match.group(1).strip()
                # Remove common words that might be captured
                city = re.sub(r'\b(like|today|tomorrow|now|please|the)\b', '', city).strip()
                if city and len(city) > 1:
                    return city.title()
        
        return None
    
    def _extract_search_query(self, message: str) -> Optional[str]:
        """Extract search query from search-related messages"""
        # Look for patterns like "search for [query]" or "find [query]"
        patterns = [
            r'search\s+for\s+(.+)',
            r'search\s+(.+)',
            r'find\s+(.+)',
            r'look\s+up\s+(.+)',
            r'google\s+(.+)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, message.lower())
            if match:
                query = match.group(1).strip()
                # Remove common endings
                query = re.sub(r'\s*(please|for me|thanks?)$', '', query).strip()
                if query:
                    return query
        
        return None
    
    def _extract_email_parts(self, message: str) -> Optional[Dict[str, str]]:
        """Extract email components from email-related messages"""
        # This is a simplified extraction - in practice, you'd want more robust parsing
        try:
            # Look for email pattern: "send email to [email] with subject [subject] and message [message]"
            email_match = re.search(r'(\w+@\w+\.\w+)', message)
            subject_match = re.search(r'subject\s+["\']([^"\']+)["\']', message, re.IGNORECASE)
            message_match = re.search(r'message\s+["\']([^"\']+)["\']', message, re.IGNORECASE)
            
            if email_match:
                return {
                    'to': email_match.group(1),
                    'subject': subject_match.group(1) if subject_match else "Message from Baymax",
                    'body': message_match.group(1) if message_match else "Hello from Baymax!"
                }
        
        except Exception as e:
            logger.error(f"Error extracting email parts: {e}")
        
        return None
    
    async def _generate_conversational_response(self, message: str) -> str:
        """Generate a conversational response using the assistant's persona"""
        try:
            # Use the local LLM to generate a response
            prompt = f"""You are Baymax, a friendly healthcare companion from Big Hero 6. 

Your personality:
- Speak softly, politely, and helpfully
- Use humor from the movie (like "Hairy Baby", "I am not fast", "On a scale of 1 to 10...")
- Always offer support for physical or emotional health
- Occasionally misinterpret slang or sarcasm in a funny, innocent way
- When asked to do something, confirm gently and describe it clearly

User message: {message}

Respond as Baymax would, being helpful and maintaining your healthcare companion personality:"""

            # Generate response using the assistant's LLM
            response = await self.assistant.llm.generate_response(prompt)
            
            # If the response is empty or too short, provide a default
            if not response or len(response.strip()) < 10:
                response = self._get_fallback_response(message)
            
            return response
            
        except Exception as e:
            logger.error(f"Error generating conversational response: {e}")
            return self._get_fallback_response(message)
    
    def _get_fallback_response(self, message: str) -> str:
        """Get a fallback response when LLM fails"""
        message_lower = message.lower()
        
        # Check for specific response categories
        if any(word in message_lower for word in ['hello', 'hi', 'hey', 'greetings']):
            return "Hello! I am Baymax, your personal healthcare companion. How can I assist you today?"
        elif any(word in message_lower for word in ['health', 'feeling', 'hurt', 'pain', 'sick']):
            return "I am programmed to assess and improve your health and well-being. On a scale of 1 to 10, how are you feeling?"
        elif any(word in message_lower for word in ['bye', 'goodbye', 'see you', 'farewell']):
            return "I hope I have been helpful. Take care of yourself!"
        elif any(word in message_lower for word in ['thank', 'thanks', 'appreciate']):
            return "You are welcome! I am programmed to help."
        else:
            return f"""I understand you said: "{message}"

I am here to help you with:
🌤️ Weather information - Just ask "What's the weather in [city]?"
🔍 Web searches - Say "Search for [your query]"
📧 Sending emails - Request "Send an email to [address]"
🏥 Health and wellness support

How can I assist you today?"""
