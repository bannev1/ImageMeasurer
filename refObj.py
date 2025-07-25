import cv2
import numpy as np
import pupil_apriltags as tags


# Get reference
def getReferenceObjectPoints(imagePath: str) -> np.ndarray:
    """
    Gets the points (as a numpy array) in the shape (4,2) of the detected AprilTag. Note that if there are multiple tags detected, it will raise a RunTime error.
    """

    # Load image
    img = cv2.imread(imagePath)
    image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # Make greyscale

    # Detect fiducial marker (AprilTag based)
    detector = tags.Detector()

    detection = detector.detect(image)

    if len(detection) > 1:
        raise RuntimeError('More than one AprilTag detected')
    
    detection = detection[0]

    corners: np.ndarray = detection.corners # shape=(4, 2)

    return corners


