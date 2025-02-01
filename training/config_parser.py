import configparser
import logging

def get_config(configFilePath, conf_number=""):
    config = configparser.RawConfigParser()
    config.read(configFilePath)
    dictionary = dict(config.items("conf{}".format(conf_number)))

    log_name = dictionary['log_name']
    logger = define_logging(log_name)

    return dictionary, logger

def define_logging(log_name):
    logging.basicConfig(filename=log_name,
                        filemode='a',
                        format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                        datefmt='%y/%b/%Y %H:%M:%S',
                        level=logging.INFO)

    return logging.getLogger(log_name)
