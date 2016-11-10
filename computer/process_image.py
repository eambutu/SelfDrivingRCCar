import numpy as np
import cv2

if __name__ == '__main__':
    with open('./sample_input.txt', 'r') as fin:
        dim = fin.readline().split(" ")
        width = int(dim[0])
        height = int(dim[1])
        arr = np.zeros((height, width))

        for idx1 in range(0, height):
            inputs = fin.readline().split(" ")
            for idx2 in range(0, width):
                pixVal = (0xff & int(inputs[idx2]))
                pixVal = max(0, pixVal)
                pixVal = min(255, pixVal)
                print pixVal
                arr[idx1, idx2] = pixVal

        toshow = np.empty((height, width, 3))
        toshow[:,:,0] = arr
        toshow[:,:,1] = arr
        toshow[:,:,2] = arr

        cv2.imshow('sample image', toshow)
        cv2.imwrite('sample_image.png', toshow)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
