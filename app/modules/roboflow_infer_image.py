from PIL import Image
from inference_sdk import InferenceHTTPClient

# initialize the client
CLIENT = InferenceHTTPClient(
    api_url="https://detect.roboflow.com",
    api_key="w5cGsb8hG3hp5ontKZCV"
)

def do_roboflow_classify_image(image: Image.Image, class_str):
    if class_str == "apple":
        model_id = "pdc-assignment/7"
    else:
        model_id = "pdc-assignment/7"

    result = CLIENT.infer(image, model_id=model_id)

    print(result)

    label = result["top"]

    return label.split("_")[0]

if __name__ == "__main__":
    # pil_image = Image.open('../curl_tests/test.jpg')
    pil_image = Image.open('../../../data_raw_good/apple/WIN_20250202_15_46_56_Pro.jpg')
    label = do_roboflow_classify_image(pil_image)

    print(label)
