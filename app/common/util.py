# -*- coding: utf-8 -*-

import os
import json

CONFIG_FILE = "/".join((os.path.split(os.path.realpath(__file__))[0]
                        ).split('/')[:-1]) + '/config.json'


class FontColor(object):
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    SKYBLUE = '\033[36m'
    EOC = '\033[0m'


def load_config():
    """
    Load configuration from config file
    """
    config = {}
    with open(CONFIG_FILE) as config_data:
        config = json.load(config_data)
    return config


def printc(color, content):
    print "{color}{content}{eoc}".format(
        color=color, content=content, eoc=FontColor.EOC)


def print_red(content):
    printc(FontColor.RED, content)


def print_green(content):
    printc(FontColor.GREEN, content)


def print_yellow(content):
    printc(FontColor.YELLOW, content)


def print_blue(content):
    printc(FontColor.BLUE, content)


def print_skyblue(content):
    printc(FontColor.SKYBLUE, content)
