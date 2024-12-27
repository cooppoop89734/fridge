# Food Vision - Meal Suggestions

A web application that uses OpenAI's Vision API to analyze food ingredients and suggest meal ideas.

## Features

- Take pictures using your device's camera
- Upload existing food images
- Get AI-powered meal suggestions based on visible ingredients
- Modern, responsive UI

## Setup

1. Clone this repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file by copying `.env.example`:
   ```bash
   cp .env.example .env
   ```
4. Add your OpenAI API key to the `.env` file

## Running the Application

1. Start the Flask server:
   ```bash
   python app.py
   ```
2. Open your browser and navigate to `http://localhost:5000`

## Usage

1. Either take a picture using your device's camera or upload an existing image
2. Click "Get Meal Suggestions"
3. Wait for the AI to analyze the image and provide meal suggestions
4. Each suggestion will include a meal idea and basic cooking instructions

## Requirements

- Python 3.7+
- OpenAI API key
- Web camera (for taking pictures) or food images to upload 