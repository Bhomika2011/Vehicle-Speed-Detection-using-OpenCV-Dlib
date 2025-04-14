

# 🚗 Vehicle Speed Detection using OpenCV & Dlib

This project detects vehicles in a video and estimates their speed using computer vision techniques in Python. It uses Haar Cascade for vehicle detection and Dlib’s correlation trackers to track each car across frames. The speed is then estimated based on object movement and frame rate.

1. 📽️ Features

- Detects multiple vehicles in a video.
- Tracks each vehicle using Dlib correlation tracker.
- Calculates speed in km/h using distance covered between frames.
- Overlays speed of each vehicle on video output.
- Outputs a processed video with bounding boxes and speed display.
- Fully offline implementation using OpenCV and Dlib.

2. 📂 Files Included

- `speed_det.py`: Main script for vehicle speed detection.
- `vehicle_speed.py`: Alternate version with minor differences in color, detection XML, and annotations.
- `carsVid.mp4`: Input video file (**not included**, must be added).
- `vech.xml` or `Vehicle_cars.xml`: Haar Cascade classifier for detecting vehicles (**ensure the correct one is in the directory**).
- `out.mp4`: Output video generated with speed annotations.

3. 🛠️ Requirements

Make sure you have the following Python packages installed:

```bash: pip install opencv-python dlib

4.  Additional requirements:

   - A working webcam/video file (carsVid.mp4).

   - Haar Cascade XML file for vehicle detection (vech.xml or Vehicle_cars.xml).

5. 🧠 How Speed is Calculated

Speed is calculated using the distance moved by the vehicle between frames:

speed = (distance_in_pixels / pixels_per_meter) * fps * 3.6
Where:

    pixels_per_meter = 8.8

    fps = 18 (frames per second of the video)

6. 🚀 How to Run

    Place carsVid.mp4 and the corresponding Haar cascade XML in the same directory.

    Run either of the scripts:

      - python vehicle_speed.py

    A window will open showing detected vehicles and their estimated speeds.

    Press Esc to quit the video window.

7. 📌 Notes

    You may need to adjust pixels_per_meter and fps depending on the real-world calibration of your video footage.

    Ensure your OpenCV version supports cv2.VideoWriter_fourcc.

    The script supports speed estimation on the y-axis; performance might vary with camera angle.


