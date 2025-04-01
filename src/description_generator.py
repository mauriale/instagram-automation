#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Description Generator Module.
This module creates engaging Instagram descriptions using Anthropic's Claude.
"""

import os
import logging
import random
from typing import List, Optional
import base64
import requests
from anthropic import Anthropic

logger = logging.getLogger(__name__)

class DescriptionGenerator:
    """Class to generate Instagram descriptions using Claude."""
    
    def __init__(self, prompt_template: str, anthropic_api_key: str, 
                 model: str = "claude-3-opus-20240229"):
        """
        Initialize the description generator.
        
        Args:
            prompt_template: Template for prompting Claude
            anthropic_api_key: Anthropic API key for authentication
            model: The Claude model to use
        """
        self.prompt_template = prompt_template
        self.api_key = anthropic_api_key
        self.model = model
        self.client = Anthropic(api_key=anthropic_api_key)
        
        # Predefined variations for more engaging descriptions
        self.openers = [
            "✨ Check this out!",
            "🔥 Just created something amazing!",
            "💫 Excited to share this with you all!",
            "🌈 New day, new creation!",
            "🎨 Art in motion...",
            "👀 Take a look at my latest work!"
        ]
        
        self.closers = [
            "What do you think?",
            "Let me know your thoughts in the comments!",
            "Double tap if you love it!",
            "Share if this resonates with you!",
            "Tag someone who needs to see this!",
            "Save for inspiration later!"
        ]
        
        logger.info(f"DescriptionGenerator initialized with Claude model: {model}")
    
    def _get_image_description(self, image_path: str) -> str:
        """
        Use Claude to describe the image content.
        
        Args:
            image_path: Path to the image file
            
        Returns:
            description: Basic description of the image content
        """
        try:
            # Read the image file and encode it to base64
            with open(image_path, "rb") as img_file:
                image_data = base64.b64encode(img_file.read()).decode("utf-8")
            
            # Use Claude Vision to describe the image
            message = self.client.messages.create(
                model=self.model,
                max_tokens=300,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": "Describe this image in detail for use in an Instagram caption."
                            },
                            {
                                "type": "image",
                                "source": {
                                    "type": "base64",
                                    "media_type": "image/png",
                                    "data": image_data
                                }
                            }
                        ]
                    }
                ]
            )
            
            # Extract the description from Claude's response
            description = message.content[0].text
            return description
                
        except Exception as e:
            logger.warning(f"Failed to get image description from Claude: {e}")
            return "An amazing image"
    
    def generate_description(self, prompt: str, image_path: Optional[str] = None, 
                             max_length: int = 2000) -> str:
        """
        Generate an engaging Instagram description.
        
        Args:
            prompt: The prompt used to generate the image
            image_path: Path to the generated image
            max_length: Maximum length of the generated description
            
        Returns:
            description: Generated Instagram description
        """
        logger.info(f"Generating description for prompt: {prompt}")
        
        try:
            # Get image description if image path is provided
            image_desc = "an amazing image"
            if image_path and os.path.exists(image_path):
                image_desc = self._get_image_description(image_path)
                logger.info(f"Image description obtained from Claude")
            
            # Select random opener and closer for variety
            opener = random.choice(self.openers)
            closer = random.choice(self.closers)
            
            # Format the prompt for Claude
            formatted_prompt = self.prompt_template.format(
                image_prompt=prompt,
                image_description=image_desc,
                opener=opener,
                closer=closer
            )
            
            # Request description from Claude
            message = self.client.messages.create(
                model=self.model,
                max_tokens=max_length,
                temperature=0.8,
                messages=[
                    {
                        "role": "user",
                        "content": formatted_prompt
                    }
                ]
            )
            
            # Extract description from Claude's response
            description = message.content[0].text.strip()
            
            logger.info(f"Description generated successfully ({len(description)} chars)")
            return description
            
        except Exception as e:
            logger.error(f"Failed to generate description: {e}")
            # Return a fallback description
            return f"{random.choice(self.openers)} {prompt} {random.choice(self.closers)}"
    
    def add_hashtags(self, description: str, hashtags: List[str]) -> str:
        """
        Add hashtags to the description.
        
        Args:
            description: The original description
            hashtags: List of hashtags to add (without # symbol)
            
        Returns:
            updated_description: Description with hashtags
        """
        # Format hashtags with # symbol
        formatted_hashtags = [f"#{tag.strip('#')}" for tag in hashtags]
        hashtag_text = " ".join(formatted_hashtags)
        
        # Add hashtags to description
        updated_description = f"{description}\n\n{hashtag_text}"
        return updated_description
    
    def change_model(self, new_model: str) -> None:
        """
        Change the Claude model used.
        
        Args:
            new_model: The name of the new Claude model
        """
        self.model = new_model
        logger.info(f"Claude model changed to: {new_model}")