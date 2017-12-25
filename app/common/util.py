# -*- coding: utf-8 -*-

import os
import json

CONFIG_FILE = "/".join((os.path.split(os.path.realpath(__file__))
                        [0]).split('/')[:-1]) + '/config.json'


def load_config():
    """
    Load configuration from config file
    """
    config = {}
    with open(CONFIG_FILE) as config_data:
        config = json.load(config_data)
    return config
