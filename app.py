"""
Food Vision - A Flask application that uses AI to analyze food images and suggest meals.
This module handles the web server and AI integration components.
"""

import os
import base64
import logging
from io import BytesIO
from typing import Dict, Union, Any

from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
from PIL import Image
import openai

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Initialize OpenAI client
openai.api_key = os.getenv('OPENAI_API_KEY')
if not openai.api_key:
    raise ValueError("No OpenAI API key found. Please add it to your .env file.")

# Get model from environment variable
model = os.getenv('OPENAI_MODEL', 'gpt-4-vision-preview')

def process_image(image_data: str) -> Image.Image:
    """
    Process and validate the incoming image data.
    
    Args:
        image_data: Base64 encoded image data
        
    Returns:
        PIL Image object
        
    Raises:
        ValueError: If image processing fails
    """
    try:
        # Decode base64 image
        image_bytes = base64.b64decode(image_data.split(',')[1])
        image = Image.open(BytesIO(image_bytes))
        
        # Convert RGBA to RGB if necessary
        if image.mode in ('RGBA', 'LA') or (image.mode == 'P' and 'transparency' in image.info):
            background = Image.new('RGB', image.size, (255, 255, 255))
            if image.mode == 'P':
                image = image.convert('RGBA')
            background.paste(image, mask=image.split()[-1])
            image = background
            
        return image
    except Exception as e:
        logger.error(f"Image processing failed: {str(e)}")
        raise ValueError(f"Invalid image format: {str(e)}")

@app.route('/')
def home() -> str:
    """Render the home page with the image upload interface."""
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze_image() -> Union[Dict[str, Any], tuple[Dict[str, str], int]]:
    """
    Analyze an uploaded image to identify food ingredients.
    
    Returns:
        JSON response containing the list of identified ingredients or error message.
    """
    try:
        if not request.json or 'image' not in request.json:
            return jsonify({'error': 'No image data provided'}), 400
            
        # Process the image
        image = process_image(request.json['image'])
        
        # Prepare image for API
        buffered = BytesIO()
        image.save(buffered, format="JPEG", quality=95)
        
        # Create OpenAI vision request
        logger.info("Sending image to OpenAI for analysis")
        response = openai.ChatCompletion.create(
            model=model,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "List all the food ingredients you can see in this image. "
                                   "Format the response as a simple bullet point list."
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64.b64encode(buffered.getvalue()).decode()}"
                            }
                        }
                    ]
                }
            ],
            max_tokens=300
        )
        
        return jsonify({'ingredients': response['choices'][0]['message']['content']})
    
    except ValueError as ve:
        logger.error(f"Validation error: {str(ve)}")
        return jsonify({'error': str(ve)}), 400
    except Exception as e:
        logger.error(f"Unexpected error in analyze_image: {str(e)}")
        return jsonify({'error': 'An unexpected error occurred'}), 500

@app.route('/suggest', methods=['POST'])
def suggest_meals() -> Union[Dict[str, Any], tuple[Dict[str, str], int]]:
    """
    Generate meal suggestions based on the provided ingredients.
    
    Returns:
        JSON response containing meal suggestions or error message.
    """
    try:
        if not request.json or 'ingredients' not in request.json:
            return jsonify({'error': 'No ingredients provided'}), 400
            
        ingredients = request.json['ingredients']
        
        # Get meal suggestions based on confirmed ingredients
        logger.info("Requesting meal suggestions from OpenAI")
        response = openai.ChatCompletion.create(
            model=model,
            messages=[
                {
                    "role": "user",
                    "content": (
                        f"Based on these ingredients:\n{ingredients}\n\n"
                        "Suggest 3 possible meal ideas. For each meal, provide:\n"
                        "1. Name of the dish\n"
                        "2. Brief description\n"
                        "3. Basic cooking instructions"
                    )
                }
            ],
            max_tokens=500
        )
        
        return jsonify({'suggestions': response['choices'][0]['message']['content']})
    
    except Exception as e:
        logger.error(f"Error in suggest_meals: {str(e)}")
        return jsonify({'error': 'An unexpected error occurred'}), 500

if __name__ == '__main__':
    app.run(debug=True) 