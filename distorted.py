import cv2
import numpy as np
import mediapipe as mp

mp_face_mesh = mp.solutions.face_mesh

def distort_face(image_path):
    image = cv2.imread(image_path)
    if image is None:
        return None

    h, w, _ = image.shape
    face_mesh = mp_face_mesh.FaceMesh(static_image_mode=True, max_num_faces=1)

    results = face_mesh.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    if not results.multi_face_landmarks:
        return None

    landmarks = results.multi_face_landmarks[0].landmark
    center = np.mean([[int(p.x * w), int(p.y * h)] for p in landmarks], axis=0).astype(int)

    # Aumentar el tamaño de la cara
    mask = np.zeros_like(image)
    cv2.circle(mask, tuple(center), 120, (255, 255, 255), -1)
    dist_img = cv2.seamlessClone(image, image, mask, tuple(center), cv2.MIXED_CLONE)

    return dist_img
