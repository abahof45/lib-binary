#!/usr/bin/env python3
"""
Create transparent logo for lib-binary .wd files (simple version)
"""

try:
    from PIL import Image, ImageDraw, ImageFont
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False
    print("PIL not available, creating ASCII logo instead")

def create_ascii_logo():
    """Create ASCII art logo for .wd files"""
    logo = """
    ╔══════════════════════╗
    ║   LIB-BINARY         ║
    ║   .wd File Type       ║
    ║                      ║
    ║   ┌─────┐ ┌─────┐   ║
    ║   │ W   │ │ D   │   ║
    ║   └─────┘ └─────┘   ║
    ╚══════════════════════╝
    """
    
    with open("wd-logo.txt", "w") as f:
        f.write(logo)
    print("ASCII logo saved as wd-logo.txt")

def create_simple_image_logo():
    """Create simple image logo"""
    if not PIL_AVAILABLE:
        create_ascii_logo()
        return None, None
    
    # Create a new image with transparent background
    size = (256, 256)
    image = Image.new("RGBA", size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    
    # Draw a simple rounded rectangle background
    rect_size = 200
    rect_x = (size[0] - rect_size) // 2
    rect_y = (size[1] - rect_size) // 2
    
    # Gradient background
    for i in range(rect_size // 2, 0, -1):
        alpha = int(200 * (1 - i / (rect_size // 2)))
        color = (
            int(50 + 100 * (i / (rect_size // 2))),  # Red
            int(100 + 50 * (i / (rect_size // 2))),  # Green  
            int(200 + 55 * (i / (rect_size // 2))),  # Blue
            alpha
        )
        draw.ellipse([
            rect_x + (rect_size // 2 - i), 
            rect_y + (rect_size // 2 - i), 
            rect_x + (rect_size // 2 + i), 
            rect_y + (rect_size // 2 + i)
        ], fill=color)
    
    # Draw "WD" text
    try:
        font = ImageFont.truetype("arial.ttf", 80)
    except:
        try:
            font = ImageFont.truetype("arialbd.ttf", 80)  # Bold Arial
        except:
            font = ImageFont.load_default()
    
    text = "WD"
    text_color = (255, 255, 255, 255)
    
    # Get text bounding box
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    # Center the text
    text_x = (size[0] - text_width) // 2
    text_y = (size[1] - text_height) // 2
    
    # Draw text with shadow
    shadow_offset = 2
    draw.text((text_x + shadow_offset, text_y + shadow_offset), text, font=font, fill=(0, 0, 0, 180))
    draw.text((text_x, text_y), text, font=font, fill=text_color)
    
    # Save as PNG
    image.save("wd-logo.png", "PNG")
    print("Logo saved as wd-logo.png")
    
    # Create ICO version for Windows
    try:
        # Create multiple sizes for ICO
        sizes = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
        ico_images = []
        
        for size_tuple in sizes:
            resized = image.resize(size_tuple, Image.Resampling.LANCZOS)
            ico_images.append(resized)
        
        # Save as ICO
        ico_images[0].save("wd-logo.ico", format="ICO", sizes=sizes)
        print("ICO saved as wd-logo.ico")
        return "wd-logo.png", "wd-logo.ico"
    except Exception as e:
        print(f"ICO creation failed: {e}")
        return "wd-logo.png", None

if __name__ == "__main__":
    if PIL_AVAILABLE:
        png_file, ico_file = create_simple_image_logo()
        if png_file:
            print(f"Logo files created: {png_file}, {ico_file}")
    else:
        create_ascii_logo()
