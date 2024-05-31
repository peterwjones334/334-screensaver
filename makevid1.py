import cv2
import os

def images_to_video(input_dir, output_file, frame_rate):
    # Get all image files in the input directory
    image_files = [f for f in sorted(os.listdir(input_dir)) if f.endswith(('.png', '.jpg', '.jpeg', '.JPG'))]

    # Check if there are any images
    if not image_files:
        print("No images found in the directory.")
        return

    # Read the first image to get the dimensions
    first_image_path = os.path.join(input_dir, image_files[0])
    frame = cv2.imread(first_image_path)
    if frame is None:
        print("Failed to read the first image.")
        return

    height, width, layers = frame.shape
    size = (width, height)

    # Initialize the video writer
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Specify the codec
    video = cv2.VideoWriter(output_file, fourcc, frame_rate, size)

    # Iterate over each image file
    for image_file in image_files:
        image_path = os.path.join(input_dir, image_file)
        frame = cv2.imread(image_path)
        if frame is not None:
            video.write(frame)
        else:
            print(f"Failed to read image: {image_path}")

    # Release the video writer
    video.release()
    print(f"Video saved as {output_file}")

# Parameters
input_directory = 'D:\\Process\\Project52\\Code6\\video\\black\\rand'  # Directory containing the images
output_video_file = 'D:\\Process\\Project52\\Code6\\video\\black\screentest_rand_v1.8.mp4'  # Output video file path
frame_rate = 30  # Frames per second

# Create the video
images_to_video(input_directory, output_video_file, frame_rate)
