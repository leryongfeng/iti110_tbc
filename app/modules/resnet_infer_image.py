from PIL import Image
import os
from app.modules import config_parser
import torch
import torchvision.models as models
import torchvision.transforms as transforms

config_file="resource/app.conf"
# testing
#config_file = "../resource/app.conf"

details_dict, logger = config_parser.get_config(config_file)
device_val = details_dict['device_val']

def do_resnet_classify_image(image: Image.Image, class_str, model_path_prefix = ""):
    if class_str == "apple":
        model_path = model_path_prefix + details_dict['apple_model_path']
    elif class_str == "banana":
        model_path = model_path_prefix + details_dict['banana_model_path']
    elif class_str == "kiwi":
        model_path = model_path_prefix + details_dict['kiwi_model_path']
    elif class_str == "starfruit":
        model_path = model_path_prefix + details_dict['starfruit_model_path']
    elif class_str == "pear":
        model_path = model_path_prefix + details_dict['pear_model_path']
    else:
        model_path = model_path_prefix + details_dict['apple_model_path']

    num_classes = 2  # Update this to match your dataset
    model = models.resnet101(pretrained=False)  # Load model without pre-trained weights
    model.fc = torch.nn.Linear(model.fc.in_features, num_classes)

    model.load_state_dict(torch.load(model_path, map_location=torch.device(device_val)))
    model.eval()  # Set to evaluation mode

    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])
    image = transform(image)  # Apply transformations
    image = image.unsqueeze(0)  # Add batch dimension (1, 3, 224, 224)

    # Perform inference
    with torch.no_grad():
        output = model(image)
        predicted_class = torch.argmax(output, dim=1).item()

    # Get class labels (Update this based on your dataset)
    class_labels = ["good", "rotten"]  # Update with actual class names

    return class_labels[predicted_class]

if __name__ == "__main__":
    pil_image = Image.open('../../../data_raw_good/apple/WIN_20250202_15_46_56_Pro.jpg')
    label = do_resnet_classify_image(image=pil_image, class_str="apple", model_path_prefix="../")

    print(label)

    pil_image = Image.open('../../../data_raw_bad/kiwi/WIN_20250213_21_24_09_Pro.jpg')
    label = do_resnet_classify_image(image=pil_image, class_str="kiwi", model_path_prefix="../")

    print(label)
