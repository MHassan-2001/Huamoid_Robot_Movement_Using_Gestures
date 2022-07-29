import time

import cv2
import mediapipe as mp
import numpy as np

from PoseName import PoseLandmark as PN
from Socket import InputFromUser, ConnectToEsp32

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

# Colors.
blue = (255, 127, 0)
red = (50, 50, 255)
green = (127, 255, 0)
dark_blue = (127, 20, 0)
light_green = (127, 233, 100)
yellow = (0, 255, 255)
pink = (255, 0, 255)


def calculate_angle(a, b, c):
    a = np.array(a)  # First
    b = np.array(b)  # Mid
    c = np.array(c)  # End

    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(radians * 180.0 / np.pi)

    if angle > 180.0:
        angle = 360 - angle

    return angle


def GetSpecificPose():
    # for lan in mp.solutions.pose.PoseLandmark:
    #     print(lan)
    cap = cv2.VideoCapture(0)
    # Setup mediapipe instance
    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        while cap.isOpened():
            ret, frame = cap.read()

            # Recolor image to RGB
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False

            # Make detection
            results = pose.process(image)

            # Recolor back to BGR
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            # Extract landmarks
            try:
                landmarks = results.pose_landmarks.landmark

                # Get coordinates
                # shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                #             landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                # elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,
                #          landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
                # wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,
                #          landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
                CalculateMultiplePoseAngle(image, landmarks, PN.LEFT_SHOULDER, PN.LEFT_ELBOW, PN.LEFT_WRIST)
                CalculateMultiplePoseAngle(image, landmarks, PN.LEFT_HIP, PN.LEFT_KNEE, PN.LEFT_ANKLE)
                CalculateMultiplePoseAngle(image, landmarks, PN.LEFT_HIP, PN.LEFT_KNEE, PN.LEFT_ANKLE)

                # start = [landmarks[start_pose].x,
                #          landmarks[start_pose].y]
                # mid = [landmarks[mid_pose].x,
                #        landmarks[mid_pose].y]
                # end = [landmarks[end_pose].x,
                #        landmarks[end_pose].y]
                #
                # # Calculate angle
                # angle = calculate_angle(start, mid, end)
                #
                # # Visualize angle
                # cv2.putText(image, str(int(angle)),
                #             tuple(np.multiply(mid, [640, 480]).astype(int)),
                #             cv2.FONT_HERSHEY_SIMPLEX, 0.5, blue, 2, cv2.LINE_AA
                #             )

            except:
                pass

            # Render detections
            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                      mp_drawing.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=2),
                                      mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=2)
                                      )

            cv2.imshow('Mediapipe Feed', image)

            if cv2.waitKey(10) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()


def CalculateMultiplePoseAngle(image, landmarks, start_pose, mid_pose, end_pose):
    start = [landmarks[start_pose].x,
             landmarks[start_pose].y]
    mid = [landmarks[mid_pose].x,
           landmarks[mid_pose].y]
    end = [landmarks[end_pose].x,
           landmarks[end_pose].y]

    # Calculate angle
    angle = calculate_angle(start, mid, end)

    # Visualize angle
    cv2.putText(image, str(int(angle)),
                tuple(np.multiply(mid, [640, 480]).astype(int)),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, blue, 2, cv2.LINE_AA
                )
    GetSpecificAngle(int(angle))


angleQueue = []


# checking that angle is change after specific interval of time
def GetSpecificAngle(angleToChange):
    # time.sleep(0.5)
    if len(angleQueue) > 0:
        if abs(angleQueue[-1] - angleToChange) > 10:
            # print(angleQueue[-1])
            angleQueue.append(angleToChange)
    else:
        angleQueue.append(angleToChange)


def SendingValueToMotor():
    while len(angleQueue) > 0:
        time.sleep(0.5)
        angle = angleQueue.pop()
        print(angle)


if __name__ == "__main__":
    # ConnectToEsp32()
    # InputFromUser()
    GetSpecificPose()
    # SendingValueToMotor()
