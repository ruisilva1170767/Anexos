app = cv2.cvtColor(app, cv2.COLOR_BGR2HSV)
img3 = cv2.cvtColor(img3, cv2.COLOR_BGR2HSV)

hist1_h = cv2.calcHist([app], [0], None, [256], [0, 256])
hist1_s = cv2.calcHist([app], [1], None, [256], [0, 256])
hist1_v = cv2.calcHist([app], [2], None, [256], [0, 256])

hist2_h = cv2.calcHist([img3], [0], None, [256], [0, 256])
hist2_s = cv2.calcHist([img3], [1], None, [256], [0, 256])
hist2_v = cv2.calcHist([img3], [2], None, [256], [0, 256])

hist1_h = cv2.normalize(hist1_h, hist1_h).flatten()
hist1_s = cv2.normalize(hist1_s, hist1_s).flatten()
hist1_v = cv2.normalize(hist1_v, hist1_v).flatten()

hist2_h = cv2.normalize(hist2_h, hist2_h).flatten()
hist2_s = cv2.normalize(hist2_s, hist2_s).flatten()
hist2_v = cv2.normalize(hist2_v, hist2_v).flatten()

MSE_error[i] = cv2.compareHist(hist1_h, hist2_h, cv2.HISTCMP_BHATTACHARYYA) + cv2.compareHist(hist1_s, hist2_v, cv2.HISTCMP_BHATTACHARYYA) + cv2.compareHist(hist1_v, hist2_v, cv2.HISTCMP_BHATTACHARYYA)