'''This file handles all logging process'''

import logging

def set_logging(class_name):
    logger = logging.getLogger(class_name)
    f_handler = logging.FileHandler('../log/dl_service_log_v0.log')
    s_handler = logging.StreamHandler()
    _format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    f_handler.setFormatter(_format)
    s_handler.setFormatter(_format)
    logger.addHandler(f_handler)
    logger.addHandler(s_handler)

    return logger