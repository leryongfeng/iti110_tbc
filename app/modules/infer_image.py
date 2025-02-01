from ultralytics import YOLO
from PIL import Image, ImageDraw, ImageFont
import os
from app.modules import config_parser

config_file="resource/app.conf"
details_dict, logger = config_parser.get_config(config_file)
model_path = details_dict['model_path']

# testing
#config_file = "../resource/app.conf"
#details_dict, logger = config_parser.get_config(config_file)
#model_path = '../resource/sword_n_bow_best.pt'

# YOLO image inference
def do_infer_image(pil_image):
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
    draw = ImageDraw.Draw(im_rgb)

    for i, r in enumerate(results):
        # Get the bounding boxes and labels from the results
        boxes = r.boxes  # This should be a list of detected boxes
        labels = r.names  # Labels (e.g., 'person', 'car')

        # Iterate over each detected object
        for box, label in zip(boxes, labels):
            # Extract the coordinates and confidence of the bounding box
            label_name = r.names[label]  # Get the string label from the index
            x_center, y_center, width, height = box.xywh[0]
            conf = box.conf

            # Convert center-width-height to top-left and bottom-right coordinates
            x1 = int(x_center - width / 2)
            y1 = int(y_center - height / 2)
            x2 = int(x_center + width / 2)
            y2 = int(y_center + height / 2)

            # Ensure coordinates are ordered correctly
            x1, x2 = min(x1, x2), max(x1, x2)
            y1, y2 = min(y1, y2), max(y1, y2)

            # Draw bounding box and label
            text = f"{label_name} {conf.item():.2f}"  # Convert Tensor to float before formatting
            font = ImageFont.load_default()
            draw.rectangle([x1, y1, x2, y2], outline="red", width=2)
            draw.text((x1, y1), text, fill="white", font=font)

            # Store bounding box details (x1, y1, x2, y2) and the label
            bounding_boxes.append({"bbox": (x1, y1, x2, y2), "label": label_name, "confidence": conf.item(), "size": (x2 - x1) * (y2 - y1)})

        # Plot results image (if you want to show it on screen)
        # r.show()

    # Save the annotated image to the results folder
    # annotated_image_path = os.path.join(result_path, "annotated_image.png")
    # im_rgb.save(annotated_image_path)

    logger.info(bounding_boxes)
    logger.info(im_rgb)

    return im_rgb, bounding_boxes

if __name__ == "__main__":
    pil_image = Image.open('../curl_tests/test.jpg')
    im_rgb, bounding_boxes = do_infer_image(pil_image)
