import os
from PIL import Image

input_path = r"C:\Users\thall\Downloads\hero-bg.jpg.png"
output_path = r"c:\Users\thall\Desktop\landin\Projeto\hero-bg.jpg"

try:
    with Image.open(input_path) as img:
        # Convert to RGB (to avoid error when saving as JPEG if it has alpha channel)
        if img.mode in ('RGBA', 'P'):
            img = img.convert('RGB')
            
        # Get current size
        w, h = img.size
        print(f"Original size: {w}x{h}")
        
        # Resize if width is larger than 1920, maintaining aspect ratio
        target_width = 1920
        if w > target_width:
            target_height = int(target_width * h / w)
            img = img.resize((target_width, target_height), Image.Resampling.LANCZOS)
            print(f"Resized to: {target_width}x{target_height}")
            
        # Optimize and save
        img.save(output_path, 'JPEG', quality=85, optimize=True)
        print(f"Successfully saved to {output_path}")

except Exception as e:
    print(f"Error processing image: {e}")
