import cv2
from os.path import exists

from refObj import getReferenceObjectPoints as getRef
from measurer import measure


if __name__ == '__main__':
    # Set parameters
    IMAGE_PATH = r"./images/testing.jpeg"

    FIDUCIAL_SIZE = (7.5, 7.5) # In cm (w x h)
    MINAREA = 20
    THICKNESS = 5
    TEXT_SIZE = 10

    # Get sizes
    fidWidth, fidHeight = FIDUCIAL_SIZE

    # Get points of fiducial code
    reference = getRef(IMAGE_PATH)

    # Get final image
    finalSizeImg = measure(IMAGE_PATH, reference, fidWidth, fidHeight, MINAREA, THICKNESS, TEXT_SIZE)

    cv2.imwrite('./output/result.jpg', finalSizeImg)

    # Output/Window
    DOWNSIZE = 10
    finalSizeImg = cv2.resize(finalSizeImg, (finalSizeImg.shape[1]//DOWNSIZE, finalSizeImg.shape[0]//DOWNSIZE))

    cv2.namedWindow('final')
    cv2.imshow('final', finalSizeImg)
    cv2.moveWindow('final', 0, 200)

    cv2.waitKey(0)
    cv2.destroyAllWindows()
