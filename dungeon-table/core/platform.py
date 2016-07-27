"""
Put platform specific fixes here
"""
from os.path import expanduser

def get_config_path():
    return expanduser("~")
