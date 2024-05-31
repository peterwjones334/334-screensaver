import cv2
import os

def extract_frames(video_path, output_folder):
    # Open the video file
    video_capture = cv2.VideoCapture(video_path)

    # Check if the video file opened successfully
    if not video_capture.isOpened():
        print(f"Error: Could not open video {video_path}")
        return

    # Create the output directory if it does not exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    frame_number = 0
    while True:
        # Read the next frame
        success, frame = video_capture.read()
        
        # If reading the frame was not successful, break the loop
        if not success:
            break
        
        # Save the frame as a PNG file
        frame_filename = os.path.join(output_folder, f"frame_{frame_number:04d}.png")
        cv2.imwrite(frame_filename, frame)
        
        frame_number += 1

    # Release the video capture object
    video_capture.release()
    print(f"Frames extracted and saved to {output_folder}")

# Example usage
video_path = 'test.mp4'
output_folder = '\\frames'
extract_frames(video_path, output_folder)
