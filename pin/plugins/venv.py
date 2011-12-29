import os
from argparse import ArgumentParser

from pin import registry, event, hook, PROJECT_FOLDER
from pin.event import eventhook
from pin.util import *

import virtualenv
virtualenv.logger = virtualenv.Logger(consumers=[])

VENV_FOLDER = 'env'

class VirtualEnvPinHook(hook.PinHook):
    '''Add new arguments to core init command for creating virtualenvs'''
    name = "venv"

    def __init__(self):
        self.options = None

    def write_env_path_file(self, root, venv):
        path_file = os.path.join(root, '.pin', 'venv.pth')
        with open(path_file, 'w') as file:
            file.write(venv)

    @eventhook('init-post-parser')
    def init_post_parser(self, parser):
        parser.add_argument('--mkenv', nargs="?", default=False,
               help='create virtualenv at .pin/env or supplied path')
        parser.add_argument('--lnenv', nargs=1, default=False,
               help='associate existing virtualenv at supplied path')

    @eventhook('init-post-args')
    def init_post_args(self, args, options):
        self.options = options

    @eventhook('init-post-exec')
    def init_post_exec(self, cwd, root):
        if self.options.mkenv is not False:
            print "Creating virtualenv..."
            if self.options.mkenv is None:
                self.options.mkenv = os.path.join(root, 
                                                 PROJECT_FOLDER, 
                                                 VENV_FOLDER)
            self.fire("pre-create", self.options.mkenv)
            if not os.path.isdir(self.options.mkenv):
                os.mkdir(self.options.mkenv)
            virtualenv.create_environment(self.options.mkenv, False, True)
            self.write_env_path_file(root, self.options.mkenv)
            self.fire("post-create", self.options.mkenv)
        elif self.options.lnenv is not False:
            print "Associating virtualenv..."
            self.fire("pre-link", self.options.lnenv)
            self.write_env_path_file(root, self.options.lnenv)
            self.fire("post-link", self.options.lnenv)

    @eventhook('destroy-post-script')
    def destroy_post_script(self, file):
        file.write("deactivate;")
hook.register(VirtualEnvPinHook)
