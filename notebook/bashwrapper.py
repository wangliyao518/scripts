import sys
import subprocess

#def __getattr__(mod, fun): 
#    return lambda args: subprocess.check_output('{} {}'.format(fun, args),shell=True)

class Wrapper(object):
    def __init__(self, wrapped):
        self.wrapped = wrapped
    def __getattr__(self, fun):
        return lambda args: subprocess.check_output('{} {}'.format(fun, args), shell=True)

sys.modules[__name__] = Wrapper(sys.modules[__name__])
