import cv2
import numpy as np


def process_image(image):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    lower_red = np.array([0, 100, 100])
    upper_red = np.array([10, 255, 255])
    mask1 = cv2.inRange(hsv, lower_red, upper_red)
    lower_red = np.array([170, 100, 100])
    upper_red = np.array([180, 255, 255])
    mask2 = cv2.inRange(hsv, lower_red, upper_red)
    mask = cv2.bitwise_or(mask1, mask2)

    kernel = np.ones((5, 5), np.uint8)
    opening = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel)

    M = cv2.moments(closing)
    cX = int(M["m10"] / M["m00"])
    cY = int(M["m01"] / M["m00"])

    cv2.circle(image, (cX, cY), 5, (0, 0, 0), -1)

    cv2.imshow('Image with Center Marked', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def process_movie(cap):
    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))
    fps = int(cap.get(cv2.CAP_PROP_FPS))

    out = cv2.VideoWriter('project-1/output.mp4', cv2.VideoWriter_fourcc(*'avc1'), fps, (frame_width, frame_height))

    kernel = np.ones((5, 5), np.uint8)

    while cap.isOpened():
        ret, frame = cap.read()

        if not ret:
            break

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Zadanie 2
        # lower_red = np.array([0, 100, 10])
        # upper_red = np.array([10, 255, 255])
        # mask1 = cv2.inRange(hsv, lower_red, upper_red)
        #
        # lower_red = np.array([160, 100, 20])
        # upper_red = np.array([179, 255, 255])
        # mask2 = cv2.inRange(hsv, lower_red, upper_red)
        #
        # mask = mask1 + mask2

        # Zadanie 3
        lower_blue = np.array([90, 50, 50])
        upper_blue = np.array([130, 255, 255])
        mask = cv2.inRange(hsv, lower_blue, upper_blue)

        opening = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel)

        edges = cv2.Canny(closing, 100, 200)

        edges = cv2.dilate(edges, kernel, iterations=1)

        edges = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)

        M = cv2.moments(edges)
        if M["m00"] != 0:
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])

            cv2.circle(frame, (cX, cY), 5, (0, 0, 0), -1)

        out.write(frame)

        cv2.imshow('Frame', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    out.release()
    cv2.destroyAllWindows()


def main():
    # Zadanie 1
    # image = cv2.imread('project-1/ball.png')
    # process_image(image)

    # Zadanie 2
    # cap = cv2.VideoCapture('project-1/movingball.mp4')
    # process_movie(cap)

    # Zadanie 3
    cap = cv2.VideoCapture('project-1/dogball.mp4')
    process_movie(cap)


if __name__ == "__main__":
    main()