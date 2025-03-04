import os
from flask import Flask, render_template, request, redirect, url_for
import cloudinary
import cloudinary.uploader
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Cloudinary
cloudinary.config(
    cloud_name=os.getenv('CLOUDINARY_CLOUD_NAME'),
    api_key=os.getenv('CLOUDINARY_API_KEY'),
    api_secret=os.getenv('CLOUDINARY_API_SECRET')
)

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Check if a file was uploaded
        if 'image' not in request.files:
            return redirect(request.url)
            
        file = request.files['image']
        
        # If the user does not select a file, browser submits an empty file
        if file.filename == '':
            return redirect(request.url)
            
        if file:
            # Upload the image to Cloudinary
            upload_result = cloudinary.uploader.upload(file)
            
            # You can store additional metadata in a database if needed
            # For this simple app, we'll just redirect to the gallery
            return redirect(url_for('gallery'))
            
    return render_template('index.html')

@app.route('/gallery')
def gallery():
    # Get all images from Cloudinary with a specific tag or folder
    # For simplicity, we'll get the last 100 images
    result = cloudinary.api.resources(
        type="upload",
        max_results=100
    )
    
    images = result.get('resources', [])
    return render_template('gallery.html', images=images)

if __name__ == '__main__':
    app.run(debug=True)
