import subprocess
from moviepy.editor import VideoFileClip
from moviepy.video.fx.all import mask_color
import os

def add_alpha_channel(input_video_path, output_video_path, color_to_make_transparent=(255, 255, 255)):
    # Load the video
    video = VideoFileClip(input_video_path)
    
    # Add alpha channel by making the specified color transparent
    video_with_alpha = mask_color(video, color=color_to_make_transparent)
    
    # Save the intermediate video to a temporary file
    temp_output_path = "temp_output.webm"
    video_with_alpha.write_videofile(temp_output_path, codec='libvpx-vp9', preset='medium', logger=None)
    
    # Use ffmpeg to add the alpha channel
    command = [
        'ffmpeg',
        '-i', temp_output_path,
        '-c:v', 'libvpx-vp9',
        '-pix_fmt', 'yuva420p',
        output_video_path
    ]
    
    subprocess.run(command)
    
    # Remove the temporary file
    os.remove(temp_output_path)
    print(f"Processed video saved to {output_video_path}")

# Example usage
input_video_path = 'input.mp4'
output_video_path = 'output.webm'
add_alpha_channel(input_video_path, output_video_path)
