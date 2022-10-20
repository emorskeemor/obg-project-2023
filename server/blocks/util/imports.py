import importlib
import os

ENVIRON_SETTINGS_KEY = "GENERATOR_SETTINGS_MODULE"
SETTINGS_LOOKUP_NAME = "BLOCK_GENERATOR_OPTIONS"

GEN_SETTINGS_MODULE = os.environ.get(ENVIRON_SETTINGS_KEY, None)

if GEN_SETTINGS_MODULE is None:
    raise AttributeError(
        "generator settings module must be set in os.environ with key matching '%s'" 
        % ENVIRON_SETTINGS_KEY
    )

def get_settings(module_name:str=None):
    '''get settings dict from settings file'''
    if module_name is None:
        module_name = GEN_SETTINGS_MODULE
    try:
        mod = importlib.import_module(module_name)
        options = getattr(mod, SETTINGS_LOOKUP_NAME, None)
        if type(options) is not dict:
            raise TypeError(
                "'%s' expected to be a dictionary not a '%s'" % (SETTINGS_LOOKUP_NAME, type(options))
            )
        return options
        
        
    except ImportError:
        raise ImportError("could not import settings module named '%s'" % module_name)

def import_from_settings(attribute:str, raise_exce=False, default=None):
    attr = get_settings().get(attribute, None)
    if attr is None:
        if not raise_exce and default is not None:
            return default
        raise AttributeError(
            "could not find attribute '%s' in '%s'"
            % (attribute, SETTINGS_LOOKUP_NAME)
            )
    return attr

    

