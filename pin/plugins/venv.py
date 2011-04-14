import os
from argparse import ArgumentParser

from pin import *
from pin import registry
from pin.event import register, eventhook
from pin.hook import PinHook, register
from pin.util import *

import virtualenv
virtualenv.logger = virtualenv.Logger(consumers=[])

VENV_FOLDERNAME = 'env'

# Utility methods
@findroot
def create_virtualenv(path):
    if path:
        path = os.path.join(path,
                            PROJECT_FOLDERNAME,
                            VENV_FOLDERNAME)
        virtualenv.create_environment(path, False, True)

# Virtual environment hooks
class VirtualEnvPinHook(PinHook):

    name = "venv"

    def __init__(self):
        self.options = None

    @eventhook('init-post-args')
    def parse_args(self, args, **kwargs):
        parser = ArgumentParser()
        parser.add_argument('--venv', action='store_true')
        self.options, extargs  = parser.parse_known_args(args)

    @eventhook('init-post-exec')
    def create_venv(self, cwd, root):
        if self.options and self.options.venv:
            print "Creating virtualenv..."
            envpath = os.path.join(cwd, PROJECT_FOLDERNAME, VENV_FOLDERNAME)
            self.fire("pre-create", envpath)
            os.mkdir(envpath)
            create_virtualenv(envpath)
            self.fire("post-create", envpath)

    @eventhook('destroy-post-script')
    def deactivate(self, file):
        file.write("deactivate;")
        

register(VirtualEnvPinHook)
