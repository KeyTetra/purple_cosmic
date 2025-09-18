import numpy as np
import cv2
from PIL import Image as pil_image
from outlines import outline, outline_feature, white_pixels_to_transparent
from pathlib import Path
import os


def grab(image_file, the_rect, feature=False):
    image = cv2.imread(image_file)
    mask = np.zeros(image.shape[:2], np.uint8)
    bgdModel = np.zeros((1, 65), np.float64)
    fgdModel = np.zeros((1, 65), np.float64)
    cv2.grabCut(image, mask, the_rect, bgdModel, fgdModel, 5, cv2.GC_INIT_WITH_RECT)
    #(the_mask, the_fg, the_bg) = cv2.grabCut(image, mask, the_rect, bgdModel, fgdModel, 5, cv2.GC_INIT_WITH_RECT)
    mask2 = np.where((mask == 0) | (mask == 2), 0, 1).astype("uint8")
    print("your mask:", mask2)
    img = image * mask2[:, :, np.newaxis]
    print("img:", img)


    path_object = Path(image_file)
    file_stem = path_object.stem
    stem, extension = os.path.splitext(image_file)
    out_pth = os.path.join("static/assets/mockups/cropped", file_stem + f"_cropped{extension}")
    print("out_path: ", out_pth)
    if feature:
        cv2.imwrite(out_pth, img)
        return out_pth
    else:
        yy = cv2.imwrite(out_pth, img)
        bnew_image = cv2.imread(out_pth)
        gray = cv2.cvtColor(bnew_image, cv2.COLOR_BGR2GRAY)
        _, mask2 = cv2.threshold(gray, 1, 255, cv2.THRESH_BINARY)
        b, g, r = cv2.split(image)

        # Merge with the new alpha channel (mask)
        transparent_image = cv2.merge((b, g, r, mask2))
        cv2.imwrite(out_pth, transparent_image)

        print("yy: ", yy)
        return {"og": image_file, "out": out_pth}
