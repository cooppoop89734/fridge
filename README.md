# Food Vision - Meal Suggestions

An AI-powered web application that analyzes food ingredients from images and suggests creative meal ideas.

## Features

- Take pictures using your device's camera
- Upload existing food images
- AI-powered ingredient detection
- Editable ingredient list
- Smart meal suggestions with descriptions and cooking instructions
- Modern, responsive UI built with TailwindCSS

## Quick Start

1. Clone this repository:
   ```bash
   git clone https://github.com/cooppoop89734/fridge.git
   cd fridge
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   ```bash
   cp .env.example .env
   ```
   Edit `.env` and add your:
   - OpenAI API key
   - Preferred model (defaults to gpt-4-vision-preview if not specified)

4. Run the application:
   ```bash
   python app.py
   ```

5. Open your browser and navigate to `http://localhost:5000`

## How to Use

1. **Capture or Upload Image**
   - Use your device's camera to take a picture of ingredients
   - Or upload an existing image of ingredients

2. **Review Ingredients**
   - The AI will analyze the image and list detected ingredients
   - You can edit the ingredient list if needed
   - Add missing ingredients or remove incorrect ones

3. **Get Meal Suggestions**
   - Click "Get Meal Suggestions" to receive three creative meal ideas
   - Each suggestion includes:
     - Dish name
     - Brief description
     - Basic cooking instructions

## Requirements

- Python 3.7+
- OpenAI API key
- Web camera (for taking pictures) or food images to upload
- Modern web browser

## Technical Stack

- Backend: Flask (Python)
- Frontend: HTML, JavaScript, TailwindCSS
- AI: OpenAI GPT-4 Vision API
- Image Processing: Pillow (Python Imaging Library)

## Contributing

Feel free to open issues or submit pull requests with improvements.

## License

MIT License - feel free to use this project for your own purposes. 