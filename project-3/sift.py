import cv2

reference_images = []
for image_path in ["images/1.jpeg", "images/2.jpeg", "images/3.jpeg", "images/4.jpeg", "images/5.jpeg", "images/6.jpeg"]:
    reference_image = cv2.imread(image_path)
    gray_reference = cv2.cvtColor(reference_image, cv2.COLOR_BGR2GRAY)
    sift = cv2.SIFT_create()
    keypoints_reference, descriptors_reference = sift.detectAndCompute(gray_reference, None)
    reference_images.append((reference_image, keypoints_reference, descriptors_reference))

cap = cv2.VideoCapture("movie/movie.mp4")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    keypoints_frame, descriptors_frame = sift.detectAndCompute(gray_frame, None)

    best_match_count = 0
    best_matched_image = None
    best_matched_keypoints = None
    for reference_image, keypoints_reference, descriptors_reference in reference_images:
        bf = cv2.BFMatcher()
        matches = bf.knnMatch(descriptors_reference, descriptors_frame, k=2)

        good_matches = []
        for m, n in matches:
            if m.distance < 0.75 * n.distance:
                good_matches.append(m)

        if len(good_matches) > best_match_count:
            best_match_count = len(good_matches)
            best_matched_image = reference_image
            best_matched_keypoints = keypoints_reference


    if best_matched_image is not None and good_matches:
        img3 = cv2.drawMatches(best_matched_image, best_matched_keypoints, frame, keypoints_frame, good_matches, None,
                               flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
        cv2.imshow('Object Detection', img3)
    else:
        cv2.imshow('Object Detection', frame)

    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
