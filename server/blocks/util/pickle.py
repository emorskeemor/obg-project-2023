import os.path
import pickle

from blocks.core import STATIC_ROOT


def build_pickle_path(file_name:str):
    return os.path.join(STATIC_ROOT, "%s.pickle" % file_name)

def dump_obj_to_static(file_name:str, obj:object):
    with open(build_pickle_path(file_name), "wb") as f:
        pickle.dump(obj, f, protocol=pickle.HIGHEST_PROTOCOL)

def load_obj_from_static(file_name:str):
    with open(build_pickle_path(file_name), "rb") as f:
        return pickle.load(f)
