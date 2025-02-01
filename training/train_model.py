from ultralytics import YOLO
from ultralytics import settings
import os
from training import config_parser
from roboflow import Roboflow

def download_roboflow(config_file = "resource/app.conf"):
    details_dict, logger = config_parser.get_config(config_file)

    # NOTE: replace with code from roboflow. see resource/roboflow_download_dataset.png
    rf = Roboflow(api_key=details_dict['api_key'])
    project = rf.workspace(details_dict['workspace']).project(details_dict['project_name'])
    version = project.version(details_dict['workspace'])
    dataset = version.download(details_dict['dataset_version'])

def do_train_model(config_file = "resource/app.conf",
                   yolo_model_name = "yolov8", dataset_version = 1, project_name = "sword_n_bow",
                   epochs = 10, patience = 10, lr0 = 0.1, momentum = 0.937, dropout = 0.0, batch = 16, warmup_epochs = 3.0,
                   degree = 0, shear = 0, erasing = 0.4, bgr = 0.0,
                   mixup = 0.0, copy_paste = 0.0, copy_paste_mode = "flip"):
    cwd = os.getcwd()

    details_dict, logger = config_parser.get_config(config_file)
    device_val = device_val = details_dict['device_val']

    settings.update({"wandb": True,
                     "comet.ml": False,
                     "tensorboard": False})

    # Load a pre-trained YOLO model
    if yolo_model_name == 'yolov11':
        model = YOLO("yolo11n.pt")
    else:
        model = YOLO("yolov8s.pt")

    # do train
    result = model.train(data="{}/{}-{}/data.yaml".format(cwd, project_name, dataset_version),
                         epochs=epochs,
                         patience=patience,
                         lr0=lr0,
                         momentum=momentum,
                         dropout=dropout,
                         batch=batch,
                         warmup_epochs=warmup_epochs,

                         degrees=degree,
                         shear=shear,
                         erasing=erasing,
                         bgr=bgr,
                         mixup=mixup,
                         copy_paste=copy_paste,
                         copy_paste_mode=copy_paste_mode,

                         save_period=1,
                         save_json=True,
                         device=device_val,
                         project="test",
                         plots=True)

    train_params = f"\"yolo_model_name\" : \"{yolo_model_name}\", \"dataset_version\" : \"{dataset_version}\", \"project_name\" : \"{project_name}\", \"epochs\" : \"{epochs}\", \"patience\" : \"{patience}\", \"lr0\" : \"{lr0}\", \"momentum\" : \"{momentum}\", \"dropout\" : \"{dropout}\", \"batch\" : \"{batch}\", \"warmup_epochs\" : \"{warmup_epochs}\", \"degree\" : \"{degree}\", \"shear\" : \"{shear}\", \"erasing\" : \"{erasing}\", \"bgr\" : \"{bgr}\", \"mixup\" : \"{mixup}\", \"copy_paste\" : \"{copy_paste}\", \"copy_paste_mode\" : \"{copy_paste_mode}\""
    logger.info("train_params: {" + train_params + "}")
    logger.info("train_metrics: " + print_metrics(model))

def print_metrics(model):
    metrics = model.val()  # no arguments needed, dataset and settings remembered

    json = f"\"class\" : \"all\", \"P\" : {metrics.box.mp}, \"R\" : {metrics.box.mr}, \"map50\" : \"{metrics.box.map50}\", \"map50-95\" : \"{metrics.box.map}\""
    json_val = "{" + json + "}"
    for i in range(len(metrics.box.ap_class_index)):
        json = f"\"class\" : \"{metrics.names[i]}\", \"P\" : {metrics.box.class_result(i)[0]}, \"R\" : {metrics.box.class_result(i)[1]}, \"map50\" : \"{metrics.box.class_result(i)[2]}\", \"map50-95\" : \"{metrics.box.class_result(i)[3]}\""
        json_val += ", {" + json + "}"

    json_val = "[" + json_val + "]"
    return json_val

if __name__ == "__main__":
    #dataset = download_roboflow()
    do_train_model(dataset_version=3, epochs=1)
