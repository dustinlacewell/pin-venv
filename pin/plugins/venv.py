import os
from argparse import ArgumentParser

from pin import *
from pin import registry
from pin.event import register, eventhook
from pin.plugin import PinHook, register
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
    def create_venv(self, path, **kwargs):
        if self.options and self.options.venv:
            print "Creating virtualenv..."
            path = os.path.join(path, PROJECT_FOLDERNAME, VENV_FOLDERNAME)
            self.fire("pre-create", path)
            os.mkdir(path)
            create_virtualenv(path)
            self.fire("post-create", path)

register(VirtualEnvPinHook)
