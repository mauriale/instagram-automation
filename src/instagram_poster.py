#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Instagram Poster Module.
This module handles posting content to Instagram using its Graph API.
"""

import os
import logging
import requests
import time
from typing import Dict, List, Optional, Any, Union
import json

logger = logging.getLogger(__name__)

class InstagramPoster:
    """Class to handle posting to Instagram using the Graph API."""
    
    def __init__(self, access_token: str, user_id: str):
        """
        Initialize the Instagram poster.
        
        Args:
            access_token: Instagram Graph API access token
            user_id: Instagram Business Account ID
        """
        self.access_token = access_token
        self.user_id = user_id
        self.api_version = "v18.0"  # Instagram Graph API version
        self.base_url = f"https://graph.facebook.com/{self.api_version}"
        
        logger.info(f"InstagramPoster initialized for user ID: {user_id}")
    
    def post(self, image_path: str, caption: str, hashtags: List[str] = None) -> Dict[str, Any]:
        """
        Post an image to Instagram with caption.
        
        Args:
            image_path: Path to the image file
            caption: Caption for the post
            hashtags: List of hashtags to add to the caption
            
        Returns:
            response: API response data
        """
        if not os.path.exists(image_path):
            error_msg = f"Image file not found: {image_path}"
            logger.error(error_msg)
            raise FileNotFoundError(error_msg)
        
        # Add hashtags to caption if provided
        if hashtags:
            formatted_hashtags = " ".join([f"#{tag.strip('#')}" for tag in hashtags])
            full_caption = f"{caption}\n\n{formatted_hashtags}"
        else:
            full_caption = caption
        
        logger.info(f"Preparing to post image: {image_path}")
        logger.info(f"Caption length: {len(full_caption)} characters")
        
        try:
            # Step 1: Create a container for the media
            container_id = self._create_media_container(image_path, full_caption)
            
            # Step 2: Publish the container
            publish_response = self._publish_container(container_id)
            
            logger.info(f"Successfully posted to Instagram. Post ID: {publish_response.get('id', 'Unknown')}")
            return publish_response
            
        except Exception as e:
            logger.error(f"Failed to post to Instagram: {e}")
            raise
    
    def _create_media_container(self, image_path: str, caption: str) -> str:
        """
        Create a container for the media.
        
        Args:
            image_path: Path to the image file
            caption: Caption for the post
            
        Returns:
            container_id: ID of the created media container
        """
        url = f"{self.base_url}/{self.user_id}/media"
        
        # For Instagram, we need to provide a URL to the image
        # In a real implementation, this would require uploading the image to a public URL
        # For this example, we'll use a placeholder approach
        image_url = self._upload_image_to_temporary_storage(image_path)
        
        params = {
            "image_url": image_url,
            "caption": caption,
            "access_token": self.access_token
        }
        
        response = requests.post(url, data=params)
        
        if response.status_code != 200:
            error_msg = f"Failed to create media container: {response.text}"
            logger.error(error_msg)
            raise Exception(error_msg)
        
        result = response.json()
        container_id = result.get("id")
        
        if not container_id:
            error_msg = "Container ID not found in response"
            logger.error(error_msg)
            raise Exception(error_msg)
        
        logger.info(f"Media container created: {container_id}")
        return container_id
    
    def _publish_container(self, container_id: str) -> Dict[str, Any]:
        """
        Publish the media container.
        
        Args:
            container_id: ID of the media container
            
        Returns:
            response: API response data
        """
        url = f"{self.base_url}/{self.user_id}/media_publish"
        
        params = {
            "creation_id": container_id,
            "access_token": self.access_token
        }
        
        # Wait a moment for the container to be ready
        time.sleep(5)
        
        response = requests.post(url, data=params)
        
        if response.status_code != 200:
            error_msg = f"Failed to publish media: {response.text}"
            logger.error(error_msg)
            raise Exception(error_msg)
        
        result = response.json()
        logger.info(f"Media published successfully: {result}")
        return result
    
    def _upload_image_to_temporary_storage(self, image_path: str) -> str:
        """
        Upload image to temporary storage to get a public URL.
        
        In a real implementation, this would upload to a service like AWS S3.
        For this example code, it's a placeholder that would need to be implemented
        with a real file hosting service.
        
        Args:
            image_path: Path to the image file
            
        Returns:
            url: Public URL to the uploaded image
        """
        # This is a placeholder function
        # In a real implementation, you would upload the image to a hosting service
        # and return the public URL
        
        logger.info(f"In a real implementation, would upload {image_path} to obtain a public URL")
        
        # Placeholder return - in a real implementation, replace with actual upload code
        # Example services: AWS S3, Cloudinary, Imgur API, etc.
        return f"https://example.com/temp_images/{os.path.basename(image_path)}"
    
    def get_account_info(self) -> Dict[str, Any]:
        """
        Get information about the Instagram Business Account.
        
        Returns:
            account_info: Information about the account
        """
        url = f"{self.base_url}/{self.user_id}"
        
        params = {
            "fields": "username,name,profile_picture_url,media_count,followers_count,follows_count",
            "access_token": self.access_token
        }
        
        response = requests.get(url, params=params)
        
        if response.status_code != 200:
            error_msg = f"Failed to get account info: {response.text}"
            logger.error(error_msg)
            raise Exception(error_msg)
        
        result = response.json()
        logger.info(f"Retrieved account info for: {result.get('username', 'Unknown')}")
        return result