import cv2
import time
import multiprocessing

# Define the RTSP URLs and output file names for each camera
camera_info = [
    {'rtsp_url': 'rtsp://admin:Lset@123@136.232.197.6:2005','output_file': 'monkey10_2005.mp4'},
#     {'rtsp_url': 'rtsp://admin:Lset@123@136.232.197.6:3005','output_file': 'ip3005.mp4'},
    # {'rtsp_url': 'rtsp://admin:Lset@123@136.232.197.6:3009','output_file': 'ip3009.mp4'},
#     {'rtsp_url': 'rtsp://admin:Lset@123@136.232.197.6:3013','output_file': 'ip3013.mp4'},
#     {'rtsp_url': 'rtsp://admin:Lset@123@136.232.197.6:3017','output_file': 'ip3017.mp4'},
#     {'rtsp_url': 'rtsp://admin:Lset@123@136.232.197.6:3021','output_file': 'ip3021.mp4'},
#     {'rtsp_url': 'rtsp://admin:Lset@123@136.232.197.6:3025','output_file': 'ip3025.mp4'},
#     {'rtsp_url': 'rtsp://admin:Lset@123@136.232.197.6:3029','output_file': 'ip3029.mp4'},
#     {'rtsp_url': 'rtsp://admin:Lset@123@136.232.197.6:3033','output_file': 'ip3033.mp4'},
    # {'rtsp_url': 'rtsp://admin:Lset@123@136.232.197.6:3037','output_file': 'ip3037.mp4'},
#     {'rtsp_url': 'rtsp://admin:Lset@123@136.232.197.6:3041','output_file': 'ip3041.mp4'},
#     {'rtsp_url': 'rtsp://admin:Lset@123@136.232.197.6:3045','output_file': 'ip3045.mp4'},
#     {'rtsp_url': 'rtsp://admin:Lset@123@136.232.197.6:3049','output_file': 'ip3049.mp4'},
#     {'rtsp_url': 'rtsp://admin:Lset@123@136.232.197.6:3053','output_file': 'ip3053.mp4'},
#     {'rtsp_url': 'rtsp://admin:Lset@123@136.232.197.6:3057','output_file': 'ip3057.mp4'},
#     {'rtsp_url': 'rtsp://admin:Lset@123@136.232.197.6:3061','output_file': 'ip3061.mp4'},
#     {'rtsp_url': 'rtsp://admin:Lset@123@136.232.197.6:3065','output_file': 'ip3065.mp4'},
    # {'rtsp_url': 'rtsp://admin:Lset@123@136.232.197.6:2001','output_file': 'ip2001.mp4'},
#     {'rtsp_url': 'rtsp://admin:Lset@123@136.232.197.6:3073','output_file': 'ip3073.mp4'},
#     {'rtsp_url': 'rtsp://admin:Lset@123@136.232.197.6:3077','output_file': 'ip3077.mp4'},
#     {'rtsp_url': 'rtsp://admin:Lset@123@136.232.197.6:3081','output_file': 'ip3081.mp4'},
#     {'rtsp_url': 'rtsp://admin:Lset@123@136.232.197.6:3085','output_file': 'ip3085.mp4'},
#     {'rtsp_url': 'rtsp://admin:Lset@123@136.232.197.6:3089','output_file': 'ip3089.mp4'},
#     {'rtsp_url': 'rtsp://admin:Lset@123@136.232.197.6:3093','output_file': 'ip3093.mp4'},
#     {'rtsp_url': 'rtsp://admin:Lset@123@136.232.197.6:3097','output_file': 'ip3097.mp4'},
#     {'rtsp_url': 'rtsp://admin:Lset@123@136.232.197.6:3101','output_file': 'ip3101.mp4'},
    # {'rtsp_url': 'rtsp://admin:Lset@123@136.232.197.6:3105','output_file': 'ip3105.mp4'},
#     {'rtsp_url': 'rtsp://admin:Lset@123@136.232.197.6:3109','output_file': 'ip3109.mp4'},
    # {'rtsp_url': 'rtsp://admin:Lset@123@136.232.197.6:3113','output_file': 'ip3113.mp4'},
#     {'rtsp_url': 'rtsp://admin:Lset@123@136.232.197.6:3117','output_file': 'ip3117.mp4'},
]

# Duration to capture in seconds (1 minute = 60 seconds)
capture_duration = 30

desired_fps = 24

def capture_video(camera_info):
    rtsp_url = camera_info['rtsp_url']
    output_file = camera_info['output_file']
    
    # Initialize the RTSP stream
    cap = cv2.VideoCapture(rtsp_url)

    # Check if the stream is opened successfully
    if not cap.isOpened():
        print(f"Error: Could not open the RTSP stream for {output_file}")
        return

    # Get the video's frame width, height, and frames per second (fps)
    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))
    original_fps = int(cap.get(5))

    num_frames = int(capture_duration * desired_fps)

    # Define the codec and create a VideoWriter object to save the video
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # You can change this codec as needed
    out = cv2.VideoWriter(output_file, fourcc, desired_fps, (frame_width, frame_height))

    # Record the start time
    start_time = time.time()

    # Start capturing and writing frames to the output file for the specified duration
    while time.time() - start_time < capture_duration:
        ret, frame = cap.read()
        if not ret:
            break

        out.write(frame)

    # Release the video capture and writer objects
    cap.release()
    out.release()

    print(f"Video saved as {output_file} for {capture_duration} seconds")

if __name__ == "__main__":
    processes = []

    # Create separate processes for each camera
    for camera in camera_info:
        process = multiprocessing.Process(target=capture_video, args=(camera,))
        processes.append(process)
        process.start()

    # Wait for all processes to finish
    for process in processes:
        process.join()

    print("All camera recordings completed.")
