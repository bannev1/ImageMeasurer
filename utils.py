import cv2
import numpy as np


def getContours(img, cThr=[100, 100], showCanny=False, minArea=1000, filter=0, draw=False):
    image = img.copy()
    imgGrey = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # convert into greyscale
    imgBlur = cv2.GaussianBlur(imgGrey, (5, 5), 1)
    imgCanny = cv2.Canny(imgBlur, cThr[0], cThr[1])
    kernel = np.ones((5, 5))
    imgDial = cv2.dilate(imgCanny, kernel, iterations=3)
    imgThreshold = cv2.erode(imgDial, kernel, iterations=2)
    if showCanny:
        resized = cv2.resize(imgThreshold, (0, 0), None, 0.15, 0.15)
        cv2.imshow('Canny', resized)

    contours, hierarchy = cv2.findContours(
        imgThreshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    finalContours = []

    for i in contours:
        area = cv2.contourArea(i)
        if area > minArea:
            perimeter = cv2.arcLength(i, True)
            approx = cv2.approxPolyDP(i, 0.02*perimeter, True)
            bbox = cv2.boundingRect(approx)
            if filter > 0:
                if len(approx) == filter:
                    finalContours.append([len(approx), area, approx, bbox, i])
            else:
                finalContours.append([len(approx), area, approx, bbox, i])

    # sort contour area from largest to smallest
    finalContours = sorted(finalContours, key=lambda x: x[1], reverse=True)

    if draw:
        for con in finalContours:
            cv2.drawContours(img, con[4], -1, (0, 0, 255), 3)

    return img, finalContours


def reorder(points):
    newPoints = np.zeros_like(points)
    points = points.reshape((4, 2))
    add = points.sum(1)
    newPoints[0] = points[np.argmin(add)]
    newPoints[3] = points[np.argmax(add)]
    diff = np.diff(points, axis=1)
    newPoints[1] = points[np.argmin(diff)]
    newPoints[2] = points[np.argmax(diff)]
    return newPoints


def img_warp(img, src, dst, inv=False, offset=False,offset_val=10):
    """
    Warps an image based on the input parameters

    From https://github.com/fvilmos/perspective_transform_tool/blob/main/utils/imagewarp.py

    Args:
        img ([type]): RGB / Gray image
        inv (bool, optional): invers transformation. Defaults to False.
        offset (bool, optional): use offset for warping the image. Defaults to False.

    Returns:
        [type]: warped image
    """

    img_h, img_w = img.shape[:2]
    
    wmat = cv2.getPerspectiveTransform(src, dst)
    wmat_inv = cv2.getPerspectiveTransform(dst,src)

    ret = []
    timg = None

    if offset == True:
        warp_offset = offset_val
    
    if offset == True:
        timg = img[warp_offset:warp_offset+img_h, 0: img_w]
    else:
        timg = img
    
    if inv == False:
        ret = cv2.warpPerspective(timg, wmat , ( img_w, img_h),flags=cv2.INTER_LANCZOS4)
    else:
        ret = cv2.warpPerspective(timg, wmat_inv , ( img_w, img_h), flags=cv2.INTER_LANCZOS4)
    return ret


def pts_unwarp(src, dst, pts):
    """
    Backprojects points from warped image to un-warped image

    Args:
        pts ([type]): points to backproject

    Returns:
        [type]: backprojected points
    """

    wmat_inv = cv2.getPerspectiveTransform(dst,src)

    if len(pts.flatten())>0:
        return cv2.perspectiveTransform (pts, wmat_inv)
    else:
        return []


# gets a bird's-eye perspective of the image and get scale difference
def warpImage(img, points, w, h):

    points = reorder(points)

    pts1 = np.float32(points)

    ogX, ogY = pts1[0]
    endX, endY = pts1[-1]

    # Calculate sizing/image-relative sizes
    ratio = w/h

    relWidth, relHeight = endX-ogX, endY-ogY
    relSize = (relWidth+relHeight)/2 # Avg
    relWidth, relHeight = int(relSize), int(relSize*ratio)

    pts2 = np.float32([[ogX, ogY], [ogX + relWidth, ogY], [ogX, ogY + relHeight], [ogX + relWidth, ogY + relHeight]])


    # img = cv2.circle(img, tuple(map(int, (ogX + relWidth//2, ogY + relHeight//2))), 100, (255, 255, 255), 5)
    # cv2.imwrite('./test.jpg', img)


    # matrix = cv2.getPerspectiveTransform(pts1, pts2)
    # imgWarp = cv2.warpPerspective(img, matrix, (w, h), cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=(0,0,0))

    imgWarp = img_warp(img.copy(), pts1, pts2, offset=True)

    scale = relWidth//w # Size difference

    return imgWarp, scale


def findDistance(pts1, pts2):
    return ((pts2[0] - pts1[0])**2 + (pts2[1] - pts1[1])**2)**0.5
