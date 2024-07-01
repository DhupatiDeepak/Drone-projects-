

import cv2
import numpy as np
img = cv2.imread('shapes2.png')
resizeImg = cv2.resize(img,(1080,720))

grayImg = cv2.cvtColor(resizeImg,cv2.COLOR_BGR2GRAY)


_, thresh = cv2.threshold(grayImg,150,255,cv2.THRESH_BINARY)

contours, _ = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)

for contour in  contours:
    approx = cv2.approxPolyDP(contour,0.01* cv2.arcLength(contour,True), True)
    cv2.drawContours(resizeImg,[approx],0,(199,89,200),3)

    x = approx.ravel()[0]
    y = approx.ravel()[1] - 10
    if len(approx) == 3:
     cv2.putText(resizeImg,"Triangle",(x,y),cv2.FONT_HERSHEY_COMPLEX,0.6,(0,200,0))

    if len(approx) == 5:
     cv2.putText(resizeImg,"Pentagan",(x,y),cv2.FONT_HERSHEY_COMPLEX,0.6,(0,200,0))

    if len(approx) == 4:
     x1,y1,w,h = cv2.boundingRect(approx)
     measureValue = float(w)/ h

     if 0.95 <= measureValue<=1.05:
         cv2.putText(resizeImg, "Square", (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.6, (0, 200, 0))
     else:
        cv2.putText(resizeImg, "Rectangle", (x, y), cv2.FONT_HERSHEY_COMPLEX,0.6,(0,200,0))
    if len(approx) == 8:
     cv2.putText(resizeImg,"Octogon",(x,y),cv2.FONT_HERSHEY_COMPLEX,0.6,(0,200,0))
    if len(approx) > 8:
     cv2.putText(resizeImg,"Circle",(x,y),cv2.FONT_HERSHEY_COMPLEX,0.6,(0,200,0))


cv2.imshow("SystemImage", resizeImg)
cv2.imshow("Processed Img", thresh)
cv2.waitKey(0)
cv2.destroyAllWindows()
