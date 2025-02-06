from ultralytics import YOLO
from PIL import Image, ImageDraw, ImageFont
import torchvision.transforms as transforms
import os
from app.modules import config_parser

config_file="resource/app.conf"
details_dict, logger = config_parser.get_config(config_file)
model_path = details_dict['model_path']
classification_model_path = details_dict['classification_model_path']

# testing
#config_file = "../resource/app.conf"
#details_dict, logger = config_parser.get_config(config_file)
#model_path = '../resource/fruit_detection.pt'

# YOLO image inference
def do_object_detection(pil_image):
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
            roi = im_rgb.crop((x1, y1, x2, y2))
            # cropped_results = do_classify_image(classification_model_path, roi)
            class_name = "test"
            # class_name = cropped_results.names[cropped_results.probs.top1]
            outline_color = "blue"
            # if class_name == "damaged":
            #    outline_color = "red"

            # Draw bounding box and label
            text = f"{label_name} {conf:.2f}"  # Convert Tensor to float before formatting
            font = ImageFont.load_default()
            draw.rectangle([x1, y1, x2, y2], outline=outline_color, width=2)
            draw.text((x1, y1), text, fill="white", font=font)

            # Store bounding box details (x1, y1, x2, y2) and the label
            bounding_boxes.append({"bbox": (x1, y1, x2, y2), "label": label_name, "classified_label": class_name,
                                   "confidence": conf, "size": (x2 - x1) * (y2 - y1)})


    # for i, r in enumerate(results):
    #     # Get the bounding boxes and labels from the results
    #     boxes = r.boxes  # This should be a list of detected boxes
    #     labels = r.names  # Labels (e.g., 'person', 'car')
    #
    #     # Iterate over each detected object
    #     for box, label in zip(boxes, labels):
    #         # Extract the coordinates and confidence of the bounding box
    #         label_name = r.names[label]  # Get the string label from the index
    #         x_center, y_center, width, height = box.xywh[0]
    #         conf = box.conf
    #
    #         # Convert center-width-height to top-left and bottom-right coordinates
    #         x1 = int(x_center - width / 2)
    #         y1 = int(y_center - height / 2)
    #         x2 = int(x_center + width / 2)
    #         y2 = int(y_center + height / 2)
    #
    #         # Ensure coordinates are ordered correctly
    #         x1, x2 = min(x1, x2), max(x1, x2)
    #         y1, y2 = min(y1, y2), max(y1, y2)
    #
    #         # crop image for second inference
    #         roi = im_rgb.crop((x1, y1, x2, y2))
    #         #cropped_results = do_classify_image(classification_model_path, roi)
    #         class_name = "test"
    #         #class_name = cropped_results.names[cropped_results.probs.top1]
    #         outline_color = "blue"
    #         #if class_name == "damaged":
    #         #    outline_color = "red"
    #
    #         # Draw bounding box and label
    #         text = f"{label_name} {conf.item():.2f}"  # Convert Tensor to float before formatting
    #         font = ImageFont.load_default()
    #         draw.rectangle([x1, y1, x2, y2], outline=outline_color, width=2)
    #         draw.text((x1, y1), text, fill="white", font=font)
    #
    #         # Store bounding box details (x1, y1, x2, y2) and the label
    #         bounding_boxes.append({"bbox": (x1, y1, x2, y2), "label": label_name, "classified_label": class_name, "confidence": conf.item(), "size": (x2 - x1) * (y2 - y1)})

        # Plot results image (if you want to show it on screen)
        # r.show()

    # Save the annotated image to the results folder
    # annotated_image_path = os.path.join(result_path, "annotated_image.png")
    # im_rgb.save(annotated_image_path)

    logger.info(bounding_boxes)
    logger.info(im_rgb)

    return im_rgb, bounding_boxes


def do_classify_image(model_path: str, image: Image.Image):
    model = YOLO(model_path, task='classify')
    transform = transforms.Compose([
        transforms.Resize((640, 640)),
        transforms.ToTensor()
    ])
    image_tensor = transform(image).unsqueeze(0)

    result = model.predict(image_tensor)

    return result

if __name__ == "__main__":
    # pil_image = Image.open('../curl_tests/test.jpg')
    pil_image = Image.open('../../../data_raw_good/apple/WIN_20250202_15_46_56_Pro.jpg')
    im_rgb, bounding_boxes = do_object_detection(pil_image)
