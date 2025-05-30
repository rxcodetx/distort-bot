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

    # Crear una copia para deformar
    distorted = image.copy()

    # Crear mapa de coordenadas de deformación
    map_y, map_x = np.indices((h, w), dtype=np.float32)
    radius = 100  # zona afectada
    strength = 0.5  # intensidad de la deformación

    for y in range(h):
        for x in range(w):
            dx = x - center[0]
            dy = y - center[1]
            distance = np.sqrt(dx*dx + dy*dy)

            if distance < radius:
                factor = 1 + strength * (1 - distance / radius)
                map_x[y, x] = center[0] + dx * factor
                map_y[y, x] = center[1] + dy * factor

    distorted = cv2.remap(image, map_x, map_y, interpolation=cv2.INTER_LINEAR)

    return distorted
