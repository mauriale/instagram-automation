#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Image Generator Module.
This module handles generating images using Hugging Face Diffusion models.
"""

import os
import logging
import requests
import uuid
from typing import Optional
from datetime import datetime

logger = logging.getLogger(__name__)

class ImageGenerator:
    """Class to handle image generation using Hugging Face models."""
    
    def __init__(self, model_name: str, hf_api_key: str, style: str = "digital art"):
        """
        Initialize the image generator.
        
        Args:
            model_name: The Hugging Face model name to use for image generation
            hf_api_key: Hugging Face API key for authentication
            style: The default style for image generation
        """
        self.model_name = model_name
        self.api_key = hf_api_key
        self.style = style
        self.api_url = f"https://api-inference.huggingface.co/models/{model_name}"
        self.headers = {"Authorization": f"Bearer {hf_api_key}"}
        
        logger.info(f"ImageGenerator initialized with model: {model_name}")
    
    def generate_image(self, prompt: str, output_dir: str, 
                       width: int = 1024, height: int = 1024) -> str:
        """
        Generate an image based on the provided prompt.
        
        Args:
            prompt: Text description to generate the image
            output_dir: Directory to save the generated image
            width: Image width in pixels
            height: Image height in pixels
            
        Returns:
            path: Path to the generated image file
        """
        # Enhance prompt with style if not already included
        if self.style.lower() not in prompt.lower():
            full_prompt = f"{prompt}, {self.style}"
        else:
            full_prompt = prompt
            
        logger.info(f"Generating image with prompt: {full_prompt}")
        
        try:
            # Prepare the payload for the API request
            payload = {
                "inputs": full_prompt,
                "parameters": {
                    "width": width,
                    "height": height,
                    "num_inference_steps": 50,
                    "guidance_scale": 7.5,
                    "negative_prompt": "low quality, blurry, distorted"
                }
            }
            
            # Make the API request
            response = requests.post(self.api_url, headers=self.headers, json=payload)
            response.raise_for_status()
            
            # Generate a unique filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            unique_id = str(uuid.uuid4())[:8]
            filename = f"generated_image_{timestamp}_{unique_id}.png"
            file_path = os.path.join(output_dir, filename)
            
            # Save the image
            with open(file_path, "wb") as f:
                f.write(response.content)
            
            logger.info(f"Image generated successfully: {file_path}")
            return file_path
        
        except requests.exceptions.RequestException as e:
            logger.error(f"API request failed: {e}")
            if hasattr(e, 'response') and e.response is not None:
                logger.error(f"Response status: {e.response.status_code}")
                logger.error(f"Response text: {e.response.text}")
            raise
        except Exception as e:
            logger.error(f"Failed to generate image: {e}")
            raise
    
    def change_model(self, new_model_name: str) -> None:
        """
        Change the model used for image generation.
        
        Args:
            new_model_name: The name of the new Hugging Face model
        """
        self.model_name = new_model_name
        self.api_url = f"https://api-inference.huggingface.co/models/{new_model_name}"
        logger.info(f"Model changed to: {new_model_name}")
    
    def change_style(self, new_style: str) -> None:
        """
        Change the default style for image generation.
        
        Args:
            new_style: The new style to use (e.g., "photorealistic", "anime")
        """
        self.style = new_style
        logger.info(f"Style changed to: {new_style}")