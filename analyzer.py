import cv2
import numpy as np
from PIL import Image

def analyze_skin_image(image):
    img = np.array(image)
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

    # 1. symmetry score
    h, w = gray.shape
    left = gray[:, :w//2]
    right = cv2.flip(gray[:, w//2:], 1)
    diff = np.abs(left.astype(float) - right.astype(float))
    symmetry = 100 - (np.mean(diff) / 255 * 100)

    # 2. edge irregularity
    edges = cv2.Canny(gray, 50, 150)
    edge_density = np.sum(edges > 0) / (h * w) * 100

    # 3. color variation
    r, g, b = cv2.split(img)
    color_var = (np.std(r) + np.std(g) + np.std(b)) / 3

    # scoring
    warnings = []
    risk = 0

    if symmetry < 70: risk += 25; warnings.append("Asymmetrical, irregular shape detected")
    if edge_density > 12: risk += 25; warnings.append("Irregular borders, edges look uneven")
    if color_var > 55: risk += 25; warnings.append("High color variation, multiple tones present")

    if risk >= 50:
        verdict = "SEE A DOCTOR"
    elif risk >= 25:
        verdict = "MONITOR, recheck in 2 weeks"
    else:
        verdict = "LIKELY BENIGN"

    return verdict, risk, warnings, symmetry, edge_density, color_var
