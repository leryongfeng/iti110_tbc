import time

from ultralytics import YOLO
from PIL import Image, ImageDraw, ImageFont
import os
from app.modules import config_parser
from app.modules import roboflow_infer_image
from app.modules import resnet_infer_image

config_file="resource/app.conf"
details_dict, logger = config_parser.get_config(config_file)
model_path = details_dict['model_path']

# testing
#config_file = "/Users/avada/Desktop/AI_Diploma/iti110/iti110_tbc/app/resource/app.conf"
#details_dict, logger = config_parser.get_config(config_file)
#model_path = '/Users/avada/Desktop/AI_Diploma/iti110/iti110_tbc/app/resource/fruit_detection.pt'

# YOLO image inference
def do_object_detection(pil_image, is_do_save_roi = False):
    global im_rgb

    # Set up result directory
    result_path = "../results"
    if not os.path.exists(result_path):
        os.makedirs(result_path)

    # Initialize YOLO model
    model = YOLO(model_path, task='detect')

    # Run inference
    results = model(pil_image, conf=0.5, iou=0.6)

    # Initialize a list to hold the bounding boxes and labels
    bounding_boxes = []

    # Convert PIL image to a format suitable for manipulation
    im_rgb = pil_image.copy()
    res_rgb = pil_image.copy()
    draw = ImageDraw.Draw(im_rgb)

    for r in results:
        boxes = r.boxes  # Detected bounding boxes
        class_names = r.names  # Class ID-to-label mapping

        # Iterate over each detected object
        for box in boxes:
            class_id = int(box.cls[0])  # Convert to integer class index
            label_name = class_names[class_id]  # Get the label name
            x_center, y_center, width, height = box.xywh[0]  # Bounding box
            conf = float(box.conf[0])  # Confidence score

            # Convert center-width-height to top-left and bottom-right coordinates
            x1 = int(x_center - width / 2)
            y1 = int(y_center - height / 2)
            x2 = int(x_center + width / 2)
            y2 = int(y_center + height / 2)

            # Ensure coordinates are ordered correctly
            x1, x2 = min(x1, x2), max(x1, x2)
            y1, y2 = min(y1, y2), max(y1, y2)

            # crop image for second inference
            roi = res_rgb.crop((x1, y1, x2, y2))

            if is_do_save_roi:
                time_val = f"{round(time.time() * 1000)}"
                roi.save(os.path.join(result_path, class_names[class_id]) +  f"_{time_val}.jpg")

            # classified_label = roboflow_infer_image.do_roboflow_classify_image(image = roi, class_str = label_name)
            # classified_label = resnet_infer_image.do_resnet_classify_image(image = roi, class_str = label_name)
            classified_label = "good"

            outline_color = "blue"
            if classified_label != "good":
               outline_color = "red"

            # Draw bounding box and label
            text = f"{label_name} {conf:.2f}"  # Convert Tensor to float before formatting
            font = ImageFont.load_default()
            draw.rectangle([x1, y1, x2, y2], outline=outline_color, width=2)
            draw.text((x1, y1), text, fill="white", font=font)

            # Store bounding box details (x1, y1, x2, y2) and the label
            bounding_boxes.append({"bbox": (x1, y1, x2, y2), "label": label_name, "classified_label": classified_label,
                                   "confidence": conf, "size": (x2 - x1) * (y2 - y1)})

    logger.info(bounding_boxes)
    logger.info(im_rgb)

    return im_rgb, bounding_boxes

if __name__ == "__main__":
    # pil_image = Image.open('../curl_tests/test.jpg')
    for root, dirs, files in os.walk(os.path.abspath("/Users/avada/Desktop/AI_Diploma/iti110/data_raw_good/starfruit")):
        for file in files:
            print(os.path.join(root, file))
            pil_image = Image.open(os.path.join(root, file))
            im_rgb, bounding_boxes = do_object_detection(pil_image, is_do_save_roi = True)

    # pil_image = Image.open('../../../data_raw_good/apple/WIN_20250202_15_46_56_Pro.jpg')
    # im_rgb, bounding_boxes = do_object_detection(pil_image)
