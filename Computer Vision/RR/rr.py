import os
import numpy as np
from PIL import Image
import cv2
import imutils
from imutils import contours
import torch
from torchvision import transforms as T


parseq = torch.hub.load('baudm/parseq', 'parseq_tiny', pretrained=True).eval()
img_transform = T.Compose([
                    T.Resize((32, 128), T.InterpolationMode.BICUBIC),
                    T.ToTensor(),
                    T.Normalize(0.5, 0.5)
                ])


folder = "imgs/"
for im_name in os.listdir(folder):
    im_path = os.path.join(folder, im_name)
    image = cv2.imread(im_path)

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)
    edged = cv2.Canny(gray, 50, 100, 3)

    cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:5]
    for (i, c) in enumerate(cnts):
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)
        if len(approx) == 4:
            screenCnt = approx
            break

    rect = np.array([list(p[0]) for p in screenCnt])
    top_left, bottom_left = sorted(sorted(rect, key=lambda x: x[0])[:2], key=lambda x: x[1])
    top_right, bottom_right = sorted(sorted(rect, key=lambda x: -x[0])[:2], key=lambda x: x[1])
    pts1 = np.float32([top_left, top_right, bottom_right, bottom_left])
    pts2 = np.float32([[0, 0], [485, 0], [485, 305], [0, 305]])
    M = cv2.getPerspectiveTransform(pts1, pts2)
    warped = cv2.warpPerspective(image, M, (485, 305))
    gray = cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY)

    rectKernel = cv2.getStructuringElement(cv2.MORPH_RECT, (18, 6))
    tophat = cv2.morphologyEx(gray, cv2.MORPH_TOPHAT, rectKernel)

    gradX = cv2.Sobel(tophat, ddepth=cv2.CV_32F, dx=1, dy=0, ksize=-1)
    gradX = np.absolute(gradX)
    (minVal, maxVal) = (np.min(gradX), np.max(gradX))
    gradX = (255 * ((gradX - minVal) / (maxVal - minVal)))
    gradient = gradX.astype("uint8")

    closed = cv2.morphologyEx(gradient, cv2.MORPH_CLOSE, rectKernel)
    thresh = cv2.threshold(closed, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    sqKernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, sqKernel)

    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    cnts = contours.sort_contours(cnts, method="top-to-bottom")[0]
    locs = []
    for (i, c) in enumerate(cnts):
        (x, y, w, h) = cv2.boundingRect(c)
        ar = w / float(h)
        if ar > 2.5 and ar < 4.0:
            if (w > 78 and w < 95) and (h > 20 and h < 34):
                locs.append((x, y, w, h))
                if len(locs) == 4:
                    break
    locs = sorted(locs, key=lambda x:x[0])
    output = []
     
    for (i, (gX, gY, gW, gH)) in enumerate(locs):
        group = tophat[gY - 5:gY + gH + 5, gX - 5:gX + gW + 5]
        group = Image.fromarray(cv2.cvtColor(group, cv2.COLOR_GRAY2RGB))
        group = img_transform(group).unsqueeze(0)
        logits = parseq(group)
        pred = logits.softmax(-1)
        label, confidence = parseq.tokenizer.decode(pred)
        groupOutput = label[0][:4]
        cv2.rectangle(warped, (gX - 5, gY - 5),
            (gX + gW + 5, gY + gH + 5), (0, 255, 0), 2)
        cv2.putText(warped, "".join(groupOutput), (gX, gY - 15),
            cv2.FONT_HERSHEY_SIMPLEX, 0.65, (0, 255, 0), 2)
        output.extend(groupOutput)
         
    print("Credit Card #: {}".format("".join(output)))
    cv2.imshow("Image", warped)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
