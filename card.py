# env name: card
import numpy as np
import cv2

# All the images paths
img_path = 'images/img.jpg'
mask_path = 'images/mask.jpg'
new_card_path = 'images/new_card.jpg'

# Read all the images
img = cv2.imread(img_path)
mask = cv2.imread(mask_path)
new_card = cv2.imread(new_card_path)

# Get the coordinates of mask
# convert mask from RGB to GREY
mask_grey = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)

# threshold
ret, thre = cv2.threshold(mask_grey, 127, 255, cv2.THRESH_BINARY)

# Contour maskCanny and draw it
maskContour = mask.copy()
contours, hierarchy = cv2.findContours(
    thre, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)


for i in range(len(contours)):
    # find the perimeter of the first closed contour
    perim = cv2.arcLength(contours[i], True)
    # setting the precision
    epsilon = 0.02*perim
    # approximating the contour with a polygon
    approxCorners = cv2.approxPolyDP(contours[i], epsilon, True)
    # check how many vertices has the approximate polygon
    approxCornersNumber = len(approxCorners)
    print("Number of approximated corners: ", approxCornersNumber)
    # printing the position of the calculated corners
    print("Coordinates of approximated corners:\n", approxCorners.shape)

#     box_x = np.zeros([4, 2], dtype=int)
#     box_y = np.zeros([4, 2], dtype=int)
#     for j in range(4):
#         box_x[j] = int(box[j, 0])  # box內數值的type是'numpy.float32'
#         box_y[j] = int(box[j, 1])
#         cv2.circle(maskContour, (box_x[j, 0],
#                    box_y[j, 1]), 10, (0, 0, 255), -1)

# cv2.drawContours(maskContour, contours, -1, (0, 0, 255), 4)

# dst = box
# print(dst)
# print(type(dst))

# # Get the coordinates of new_card
# print("new_card shape:" + str(new_card.shape))

# src = np.array([[0, 0], [new_card.shape[1] - 1, 0], [new_card.shape[1] - 1,
#                new_card.shape[0] - 1], [0, new_card.shape[0] - 1]]).astype(np.float32)
# print(src)
# print(type(src))

# # Perspective Transform
# warp_mat = cv2.getPerspectiveTransform(src, dst)
# warp_dst = cv2.warpPerspective(
#     new_card, warp_mat, (mask.shape[1], mask.shape[0]))

# # Use new_cardPerspective to paste to img

# # 白底黑物當遮罩
# mask_blackObj = 255 - mask

# # and疊加遮罩
# bg = cv2.bitwise_and(img, mask_blackObj)

# # Output：add合併被摳空的圖和歪的信用卡圖
# output = cv2.add(bg, warp_dst)

# Display the images
cv2.imshow('mask', mask)
cv2.imshow('maskContour', maskContour)
# cv2.imshow('new_cardPerspective', warp_dst)
# cv2.imshow('mask_blackObj', mask_blackObj)
# cv2.imshow('bg', bg)
# cv2.imshow('output', output)

# Close all the windows by ESC
esc = cv2.waitKey(0)
if esc == 27:
    cv2.destroyAllWindows()
