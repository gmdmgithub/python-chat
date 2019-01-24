import os

def str2bool(v):
    return v.lower() in ("yes", "true", "t", "1")


def getEnvVal(name):
    return os.environ.get(name)
