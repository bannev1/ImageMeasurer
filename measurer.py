import cv2
import numpy as np
import utils


def measure(imgPath: str, refObjPoints: np.ndarray, refWidth: int, refHeight: int, minArea: int, thickness: int = 1, textSize: int = 2, preprocessImg: bool = False) -> np.ndarray:
    """
    Adapted from https://github.com/alexyev/ObjectSizeEstimation/blob/master/ObjectMeasurement.py
    """
    img = cv2.imread(imgPath)

    if preprocessImg:
        img = utils.imagePreprocessing(img)
    
    # Warp image
    imgWarp, scaleFactor = utils.warpImage(
        img.copy(), refObjPoints, refWidth, refHeight)

    imgCont, conts2 = utils.getContours(
        imgWarp, minArea=minArea, filter=4, cThr=[50, 50], draw=False)

    if len(conts2) != 0:
        for obj in conts2:
            cv2.polylines(imgCont, [obj[2]], True, (0, 255, 0), thickness)
            nPoints = utils.reorder(obj[2])
            nW = round((utils.findDistance(
                nPoints[0][0]/scaleFactor, nPoints[1][0]/scaleFactor)), 2)
            nH = round((utils.findDistance(
                nPoints[0][0]/scaleFactor, nPoints[2][0]/scaleFactor)), 2)
            # display measurements on image
            cv2.arrowedLine(imgCont, (nPoints[0][0][0], nPoints[0][0][1]), (nPoints[1][0][0], nPoints[1][0][1]),
                            (255, 0, 255), thickness, 8, 0, 0.05)
            cv2.arrowedLine(imgCont, (nPoints[0][0][0], nPoints[0][0][1]), (nPoints[2][0][0], nPoints[2][0][1]),
                            (255, 0, 255), thickness, 8, 0, 0.05)
            x, y, w, h = obj[3]
            cv2.putText(imgCont, '{}cm'.format(nW), (x + 30, y - 10), cv2.FONT_HERSHEY_COMPLEX_SMALL, textSize,
                        (255, 0, 255), textSize)
            cv2.putText(imgCont, '{}cm'.format(nH), (x - 70, y + h // 2), cv2.FONT_HERSHEY_COMPLEX_SMALL, textSize,
                        (255, 0, 255), textSize)
    
    return imgCont
