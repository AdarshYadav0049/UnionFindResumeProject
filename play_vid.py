import cv2


def play_video(file_path):
    # Open the video file
    cap = cv2.VideoCapture(file_path)

    while cap.isOpened():
        # Read a frame from the video
        ret, frame = cap.read()

        if ret:
            # Display the frame
            cv2.imshow('Video', frame)

            # Check for the 'q' key to exit the video playback
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            # If no frame is retrieved, exit the loop
            break

    # Release the video capture and close the window
    cap.release()
    cv2.destroyAllWindows()
