from scipy.misc import imread, imsave, imresize

# Read an JPEG image into a numpy array
img = imread('input.jpg')
height, width, dim = img.shape  # Prints "uint8 (400, 248, 3)"

# We can tint the image by scaling each of the color channels
# by a different scalar constant. The image has shape (400, 248, 3);
# we multiply it by the array [1, 0.95, 0.9] of shape (3,);
# numpy broadcasting means that this leaves the red channel unchanged,
# and multiplies the green and blue channels by 0.95 and 0.9
# respectively.
# Resize the tinted image to be width 300 pixels
img_tinted = imresize(img, (int(height * 300 / width), 300))

# Write the tinted image back to disk
imsave('input.jpg', img_tinted)
