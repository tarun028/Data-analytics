import mediapipe as mp
import cv2
import numpy as np

# Initialize MediaPipe Hands module
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)

# Use OpenCV's VideoCapture to start capturing from the webcam.
cap = cv2.VideoCapture(0)  # 0 represents the default camera; you can change it if you have multiple cameras.

# Create an empty list to store history coordinates
history = []
drawing_started = False  # Flag to check if drawing has started
draw_complete = False
count = 0
while cap.isOpened():
    # Create a loop to read the latest frame from the camera using VideoCapture.read()
    ret, frame = cap.read()

    if not ret:
        continue
    frame = cv2.flip(frame, 1)  # Mirror display

    # Convert the frame received from OpenCV to a MediaPipe's Image object.
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)

    # Process the frame using the MediaPipe Hands module
    results = hands.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))  # Convert frame to RGB before processing

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Get the landmarks for the thumb (landmark[4]) and forefinger (landmark[8])
            thumb_tip = hand_landmarks.landmark[4]
            forefinger_tip = hand_landmarks.landmark[8]

            # Extract x, y, and z coordinates of the landmarks
            thumb_x, thumb_y, thumb_z = int(thumb_tip.x * frame.shape[1]), int(thumb_tip.y * frame.shape[0]), thumb_tip.z
            forefinger_x, forefinger_y, forefinger_z = int(forefinger_tip.x * frame.shape[1]), int(forefinger_tip.y * frame.shape[0]), forefinger_tip.z

            # Calculate the Euclidean distance
            euclidean_distance = np.sqrt((thumb_x - forefinger_x)**2 + (thumb_y - forefinger_y)**2 + (thumb_z - forefinger_z)**2)

            # Draw landmarks on the frame
            cv2.circle(frame, (thumb_x, thumb_y), 5, (0, 0, 255), -1)  # Red circle for thumb
            cv2.circle(frame, (forefinger_x, forefinger_y), 5, (0, 255, 0), -1)  # Green circle for forefinger

            # Print the Euclidean distance
            print(f"Euclidean Distance between Thumb and Forefinger: {euclidean_distance}")

            if euclidean_distance <= 30:
                if not drawing_started:
                    # Start a new drawing
                    drawing_started = True
                    history.append([])


                # Append coordinates to the current drawing
                history[-1].append((int((thumb_x + forefinger_x) / 2), int((thumb_y + forefinger_y) / 2)))

            elif(euclidean_distance >=45):
                if drawing_started:
                    # Complete the drawing by joining the first and last coordinates
                    if len(history[-1]) > 1:
                        history[-1].append(history[-1][0])
                    # drwa_complete = True

                    # Flag to indicate drawing is completed
                    drawing_started = False

    # Draw lines for continuous drawing
     # Display only the current drawing in progress
# Display only the current drawing in progress
    if drawing_started:
        drawing = history[-1]
        if len(drawing) > 1:
            for i in range(1, len(drawing)):
                cv2.line(frame, drawing[i - 1], drawing[i], (255, 0, 0), 2)



    # if(draw_complete):
    #     history.clear()
    # Display the frame with landmarks
    cv2.imshow('Hand Landmarks', frame)

    # Break the loop and release the camera when the 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


# Release the VideoCapture and close any OpenCV windows
cap.release()
cv2.destroyAllWindows()
