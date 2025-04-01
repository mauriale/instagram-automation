#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Main module for Instagram Automation.
This script coordinates the process of generating images,
creating descriptions, and posting to Instagram.
"""

import os
import json
import time
import logging
import argparse
from datetime import datetime
from typing import Dict, Any
import sys
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.image_generator import ImageGenerator
from src.description_generator import DescriptionGenerator
from src.instagram_poster import InstagramPoster

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("instagram_automation.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def load_config(config_path: str = "config/config.json") -> Dict[str, Any]:
    """Load configuration from JSON file."""
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
        
        # Reemplazar valores con variables de entorno si están disponibles
        if os.getenv("HUGGINGFACE_API_KEY"):
            config["api_keys"]["huggingface"] = os.getenv("HUGGINGFACE_API_KEY")
        
        if os.getenv("ANTHROPIC_API_KEY"):
            config["api_keys"]["anthropic"] = os.getenv("ANTHROPIC_API_KEY")
            
        if os.getenv("INSTAGRAM_ACCESS_TOKEN"):
            config["api_keys"]["instagram"]["access_token"] = os.getenv("INSTAGRAM_ACCESS_TOKEN")
            
        if os.getenv("INSTAGRAM_USER_ID"):
            config["api_keys"]["instagram"]["user_id"] = os.getenv("INSTAGRAM_USER_ID")
            
        logger.info(f"Configuration loaded from {config_path}")
        return config
    except Exception as e:
        logger.error(f"Failed to load config: {e}")
        raise

def create_output_directory(directory: str = "output") -> str:
    """Create output directory if it doesn't exist."""
    if not os.path.exists(directory):
        os.makedirs(directory)
        logger.info(f"Created output directory: {directory}")
    return directory

def main():
    """Main function that orchestrates the Instagram automation process."""
    parser = argparse.ArgumentParser(description='Instagram Automation Tool')
    parser.add_argument('--config', default='config/config.json', help='Path to config file')
    parser.add_argument('--mode', choices=['single', 'scheduled'], default='single',
                        help='Run mode: single (one post) or scheduled (recurring posts)')
    args = parser.parse_args()
    
    try:
        # Load configuration
        config = load_config(args.config)
        output_dir = create_output_directory(config.get("output_directory", "output"))
        
        # Initialize components
        image_gen = ImageGenerator(
            model_name=config["image_generator"]["model_name"],
            hf_api_key=config["api_keys"]["huggingface"],
            style=config["image_generator"]["style"]
        )
        
        desc_gen = DescriptionGenerator(
            prompt_template=config["description_generator"]["prompt_template"],
            anthropic_api_key=config["api_keys"]["anthropic"],
            model=config["description_generator"]["model"]
        )
        
        insta_poster = InstagramPoster(
            access_token=config["api_keys"]["instagram"]["access_token"],
            user_id=config["api_keys"]["instagram"]["user_id"]
        )
        
        if args.mode == 'single':
            # Generate and post once
            single_post_workflow(image_gen, desc_gen, insta_poster, config, output_dir)
        else:
            # Schedule recurring posts
            scheduled_workflow(image_gen, desc_gen, insta_poster, config, output_dir)
            
    except Exception as e:
        logger.error(f"Error in main execution: {e}")
        raise

def single_post_workflow(image_gen, desc_gen, insta_poster, config, output_dir):
    """Execute a single post workflow."""
    try:
        # Generate image
        prompt = config["image_generator"]["default_prompt"]
        image_path = image_gen.generate_image(prompt, output_dir)
        logger.info(f"Image generated: {image_path}")
        
        # Generate description
        description = desc_gen.generate_description(prompt, image_path)
        logger.info(f"Description generated: {description[:50]}...")
        
        # Post to Instagram
        result = insta_poster.post(image_path, description, 
                                  hashtags=config["instagram_poster"]["default_hashtags"])
        
        logger.info(f"Posted to Instagram successfully: {result}")
        return result
    
    except Exception as e:
        logger.error(f"Error in single post workflow: {e}")
        raise

def scheduled_workflow(image_gen, desc_gen, insta_poster, config, output_dir):
    """Execute scheduled posting workflow."""
    post_frequency = config["instagram_poster"]["post_frequency_hours"]
    total_posts = config["instagram_poster"].get("scheduled_posts_count", 5)
    
    logger.info(f"Starting scheduled workflow. Posts: {total_posts}, Frequency: {post_frequency}h")
    
    for i in range(total_posts):
        try:
            logger.info(f"Executing scheduled post {i+1}/{total_posts}")
            
            # Execute single post workflow
            single_post_workflow(image_gen, desc_gen, insta_poster, config, output_dir)
            
            # Skip sleep after the last post
            if i < total_posts - 1:
                sleep_seconds = post_frequency * 3600
                next_post_time = datetime.now().timestamp() + sleep_seconds
                next_post_readable = datetime.fromtimestamp(next_post_time).strftime('%Y-%m-%d %H:%M:%S')
                
                logger.info(f"Next post scheduled at {next_post_readable}, sleeping for {post_frequency} hours")
                time.sleep(sleep_seconds)
        
        except Exception as e:
            logger.error(f"Error in post {i+1}: {e}")
            # Continue with next post even if current one fails
            continue

if __name__ == "__main__":
    main()