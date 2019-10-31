from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
import sys

def main():
    # image
    filename = sys.argv[1]
    im_matrix = np.array(Image.open(filename).convert('L'))
    # create a histogram of the image
    hist = np.zeros(256)
    count = 0
    for row in im_matrix:
        for gray_data in row:
            hist[gray_data] += 1
            count += 1
    hist = hist / count
    # create the plot
    plt.title("Histogram")
    plt.plot(hist)
    plt.axis([0, 255, 0, np.max(hist) * 1.05])
    plt.xlabel("Gray Level")
    plt.ylabel("Frequence")
    plt.show()

if __name__ == "__main__":
    main()