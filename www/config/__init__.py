'''
Configuration
'''

__author__ = 'Linjun'

import config.config_default

from collections import Mapping

class Config(dict):
    '''
    Simple setting support access as x.y style.
    '''

    def __init__(self, configs):
        super(Config, self).__init__(**configs)
        for k, v in configs.items():
            self[k] = Config(v) if isinstance(v, Mapping) else v

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(r"'Setting' has not attribute '%s'" % key)
    
    def __setattr__(self, key, value):
        self[key] = value

    def merge(self, u):
        for k, v in u.items():
            if isinstance(v, Mapping):
               self.get(k).merge(v)
            else:
                self[k] = v


try:
    configs = Config(config_default.configs)
    import config.config_override
    configs.merge(config_override.configs)
except ImportError as e:
    pass