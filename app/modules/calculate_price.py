import json
from app.modules import config_parser, infer_image

config_file="resource/app.conf"
details_dict, logger = config_parser.get_config(config_file)

# testing
#config_file = "../resource/app.conf"
#details_dict, logger = config_parser.get_config(config_file)

size_calibration = dict()
price_lookup = dict()

def do_calibrate(request, inference_results):
    for result in inference_results:
        label = result['label']
        size = int(result['size']) # size in pixel area
        obj = json.loads(request.form[label]) # input object of label
        val = obj['size'] # size of object in calibration image
        input_size = int(val)
        conversion_rate = input_size / size
        # update calibration values
        size_calibration[label] = conversion_rate
        price_lookup[label] = float(obj['price'])

    print(size_calibration)
    print(price_lookup)

if __name__ == "__main__":
    print('something')