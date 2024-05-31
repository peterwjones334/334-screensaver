import os
from rembg import remove
from PIL import Image

def remove_background_from_folder(input_folder, output_folder):
    # Create the output directory if it does not exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Iterate through all files in the input folder
    for filename in os.listdir(input_folder):
        input_image_path = os.path.join(input_folder, filename)

        # Ensure the file is an image
        if input_image_path.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
            try:
                # Load the image
                input_image = Image.open(input_image_path)
                
                # Remove the background
                output_image = remove(input_image)
                
                # Define the output image path
                output_image_path = os.path.join(output_folder, filename)
                
                # Save the output image
                output_image.save(output_image_path)
                
                print(f"Processed {filename}")
            except Exception as e:
                print(f"Failed to process {filename}: {e}")

# Example usage
input_folder = '\\in'
output_folder = '\\out'
remove_background_from_folder(input_folder, output_folder)
