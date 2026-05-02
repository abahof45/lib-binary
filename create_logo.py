#!/usr/bin/env python3
"""
Create transparent logo for lib-binary .wd files
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_logo():
    """Create a transparent logo for .wd files"""
    
    # Create a new image with transparent background
    size = (256, 256)
    image = Image.new("RGBA", size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    
    # Try to use a nice font, fallback to default if not available
    try:
        font_large = ImageFont.truetype("arial.ttf", 120)
        font_small = ImageFont.truetype("arial.ttf", 40)
    except:
        font_large = ImageFont.load_default()
        font_small = ImageFont.load_default()
    
    # Create gradient background circle
    center_x, center_y = size[0] // 2, size[1] // 2
    radius = 100
    
    # Draw gradient circle (blue to purple)
    for i in range(radius, 0, -1):
        alpha = int(255 * (1 - i / radius))
        color = (
            int(100 + 155 * (i / radius)),  # Red
            int(50 + 100 * (i / radius)),   # Green  
            int(200 + 55 * (i / radius)),   # Blue
            alpha
        )
        draw.ellipse([center_x - i, center_y - i, center_x + i, center_y + i], fill=color)
    
    # Draw "LB" text for "lib-binary"
    text_color = (255, 255, 255, 255)  # White text
    text = "LB"
    
    # Get text bounding box
    bbox = draw.textbbox((0, 0), text, font=font_large)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    # Center the text
    text_x = center_x - text_width // 2
    text_y = center_y - text_height // 2 - 10
    
    # Draw text with shadow
    shadow_offset = 3
    draw.text((text_x + shadow_offset, text_y + shadow_offset), text, font=font_large, fill=(0, 0, 0, 180))
    draw.text((text_x, text_y), text, font=font_large, fill=text_color)
    
    # Draw ".wd" at the bottom
    wd_text = ".wd"
    wd_bbox = draw.textbbox((0, 0), wd_text, font=font_small)
    wd_width = wd_bbox[2] - wd_bbox[0]
    wd_x = center_x - wd_width // 2
    wd_y = center_y + 60
    
    draw.text((wd_x, wd_y), wd_text, font=font_small, fill=(255, 255, 255, 220))
    
    # Save as PNG with transparency
    image.save("lib-binary-logo.png", "PNG")
    print("✓ Logo saved as lib-binary-logo.png")
    
    # Create ICO version for Windows
    # Create multiple sizes for ICO
    sizes = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
    ico_images = []
    
    for size in sizes:
        # Resize image
        resized = image.resize(size, Image.Resampling.LANCZOS)
        ico_images.append(resized)
    
    # Save as ICO
    ico_images[0].save("lib-binary-logo.ico", format="ICO", sizes=[(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)])
    print("✓ ICO saved as lib-binary-logo.ico")
    
    return "lib-binary-logo.png", "lib-binary-logo.ico"

def create_simple_logo():
    """Create a simpler logo using basic shapes"""
    
    # Create a new image with transparent background
    size = (256, 256)
    image = Image.new("RGBA", size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    
    # Create a stylized "wd" logo
    center_x, center_y = size[0] // 2, size[1] // 2
    
    # Draw background shape - rounded rectangle with gradient
    rect_size = 180
    rect_x = center_x - rect_size // 2
    rect_y = center_y - rect_size // 2
    
    # Draw gradient background
    for i in range(rect_size // 2, 0, -1):
        alpha = int(200 * (1 - i / (rect_size // 2)))
        color = (
            int(50 + 100 * (i / (rect_size // 2))),  # Red
            int(100 + 50 * (i / (rect_size // 2))),  # Green
            int(200 + 55 * (i / (rect_size // 2))),  # Blue
            alpha
        )
        
        # Draw rounded rectangle
        corner_radius = i // 4
        draw.rounded_rectangle(
            [rect_x + (rect_size // 2 - i), rect_y + (rect_size // 2 - i), 
             rect_x + (rect_size // 2 + i), rect_y + (rect_size // 2 + i)],
            radius=corner_radius,
            fill=color
        )
    
    # Draw "wd" text
    try:
        font = ImageFont.truetype("arial.ttf", 100)
    except:
        font = ImageFont.load_default()
    
    text = "wd"
    text_color = (255, 255, 255, 255)
    
    # Get text bounding box
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    # Center the text
    text_x = center_x - text_width // 2
    text_y = center_y - text_height // 2
    
    # Draw text with shadow
    shadow_offset = 2
    draw.text((text_x + shadow_offset, text_y + shadow_offset), text, font=font, fill=(0, 0, 0, 180))
    draw.text((text_x, text_y), text, font=font, fill=text_color)
    
    # Draw small "lib-binary" text at bottom
    try:
        small_font = ImageFont.truetype("arial.ttf", 20)
    except:
        small_font = ImageFont.load_default()
    
    small_text = "lib-binary"
    small_bbox = draw.textbbox((0, 0), small_text, font=small_font)
    small_width = small_bbox[2] - small_bbox[0]
    small_x = center_x - small_width // 2
    small_y = center_y + 70
    
    draw.text((small_x, small_y), small_text, font=small_font, fill=(255, 255, 255, 200))
    
    # Save as PNG with transparency
    image.save("wd-logo.png", "PNG")
    print("✓ Simple logo saved as wd-logo.png")
    
    # Create ICO version
    sizes = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
    ico_images = []
    
    for size in sizes:
        resized = image.resize(size, Image.Resampling.LANCZOS)
        ico_images.append(resized)
    
    ico_images[0].save("wd-logo.ico", format="ICO", sizes=[(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)])
    print("✓ Simple ICO saved as wd-logo.ico")
    
    return "wd-logo.png", "wd-logo.ico"

if __name__ == "__main__":
    try:
        # Try to create the detailed logo first
        create_logo()
        print("✓ Detailed logo created successfully")
    except Exception as e:
        print(f"⚠ Detailed logo creation failed: {e}")
        print("Creating simple logo instead...")
        try:
            create_simple_logo()
            print("✓ Simple logo created successfully")
        except Exception as e2:
            print(f"⚠ Simple logo creation also failed: {e2}")
            print("Please install Pillow: pip install Pillow")
