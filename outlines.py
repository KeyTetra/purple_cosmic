import cv2
from PIL import Image

def outline(image):
    src_image = image
    b_grey = cv2.cvtColor(src_image, cv2.COLOR_BGR2GRAY)
    cv2.imwrite("quick_examples/output/output-b_grey.png", b_grey)
    inverted = cv2.bitwise_not(b_grey)
    cv2.imwrite("quick_examples/output/output-inverted.png", inverted)
    blurred = cv2.GaussianBlur(inverted, (15, 15), 0)
    d_blur = cv2.bilateralFilter(blurred, 11, 17, 17)
    inverted_blur = cv2.bitwise_not(d_blur)
    cv2.imwrite("quick_examples/output/output_ib.png", inverted_blur)
    sketch = cv2.divide(b_grey, inverted_blur, scale=1024)
    ib_sketch = cv2.divide(blurred, sketch, scale=256)
    cv2.imwrite("quick_examples/output/output_ib_sketch_ref.png", ib_sketch)
    inverted_ib_sketch = cv2.adaptiveThreshold(cv2.bitwise_not(ib_sketch),255, adaptiveMethod=cv2.ADAPTIVE_THRESH_GAUSSIAN_C, thresholdType=cv2.THRESH_BINARY, blockSize=9, C=2)
    cv2.imwrite("quick_examples/output/output_inib_sketch_ref.png", inverted_ib_sketch)

    grand_div = cv2.divide(ib_sketch, inverted_ib_sketch, scale=256)
    inverted_grand_div = cv2.bitwise_not(grand_div)
    cv2.imwrite("quick_examples/output/output_grand.png", inverted_grand_div)

    th3 = cv2.adaptiveThreshold(sketch, 255, adaptiveMethod=cv2.ADAPTIVE_THRESH_GAUSSIAN_C, thresholdType=cv2.THRESH_BINARY, blockSize=9, C=2)
    cv2.imwrite("quick_examples/output/output_sketch.png", th3)
    return th3


def outline_feature(image):
    src_image = image
    b_grey = cv2.cvtColor(src_image, cv2.COLOR_BGR2GRAY)
    cv2.imwrite("quick_examples/output/output-b_grey.png", b_grey)

    inverted = cv2.bitwise_not(b_grey)
    cv2.imwrite("quick_examples/output/foutput-inverted.png", inverted)
    blurred = cv2.GaussianBlur(inverted, (15, 15), 0)
    d_blur = cv2.bilateralFilter(blurred, 11, 17, 17)
    inverted_blur = cv2.bitwise_not(d_blur)
    cv2.imwrite("quick_examples/output/foutput_ib.png", inverted_blur)
    sketch = cv2.divide(b_grey, inverted_blur, scale=1024)
    ib_sketch = cv2.divide(blurred, sketch, scale=256)
    cv2.imwrite("quick_examples/output/foutput_ib_sketch_ref.png", ib_sketch)
    inverted_ib_sketch = cv2.adaptiveThreshold(cv2.bitwise_not(ib_sketch),255, adaptiveMethod=cv2.ADAPTIVE_THRESH_GAUSSIAN_C, thresholdType=cv2.THRESH_BINARY, blockSize=9, C=2)
    cv2.imwrite("quick_examples/output/foutput_inib_sketch_ref.png", inverted_ib_sketch)

    grand_div = cv2.divide(ib_sketch, inverted_ib_sketch, scale=256)
    inverted_grand_div = cv2.bitwise_not(grand_div)
    cv2.imwrite("quick_examples/output/foutput_grand.png", inverted_grand_div)

    th3 = cv2.adaptiveThreshold(sketch, 255, adaptiveMethod=cv2.ADAPTIVE_THRESH_GAUSSIAN_C, thresholdType=cv2.THRESH_BINARY, blockSize=9, C=2)
    cv2.imwrite("quick_examples/output/foutput_sketch.png", th3)
    return th3

#def final_slap(image1, image2):


#make sure it doesnt look for black in the parts you dont want to make transparent
def white_pixels_to_transparent(image_dest, output_dest):
    img = Image.open(image_dest)
    img = img.convert("RGBA")
    datas = img.getdata()

    newData = []
    for item in datas:
        if item[0] == 255 and item[1] == 255 and item[2] == 255:

            newData.append((255, 255, 255, 0))
        else:
            newData.append(item)

    img.putdata(newData)
    img.save(output_dest, "PNG")