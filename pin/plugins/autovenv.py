import os
from argparse import ArgumentParser

from capn.config import add_external_hook, remove_external_hook

from pin.config import config
from pin.event import eventhook
from pin.hook import PinHook, register
from pin.util import get_settings_path

# Capn auto-venv hooks

class CapnVenvPinHook(PinHook):

    name = "capn"
    default_hook_file = os.path.join(get_settings_path(), 'capnhooks')

    def __init__(self):
        self.options = None

    def isactive(self):
        if self.options: # have we parsed options?
            # were both required options present?
            return (getattr(self.options, 'mkenv', None) or
                    getattr(self.options, 'lnenv', None))
        return False

    @eventhook('init-post-parser')
    def post_parser(self, parser):
        parser.add_argument('--autoenv', action='store_true',
                            help='automatically de/activate virtualenv upon entering and exiting project directory (requires --mkenv or --lnenv)')


    @eventhook('init-post-args')
    # parse --autoenv flag
    def postargs(self, args, options):
        self.options = options

    @eventhook('venv-post-create')
    @eventhook('venv-post-link')
    # create capn hooks
    def install(self, path, **kwargs):
        if self.active: # only install if options were present
            activate_path = os.path.join(path, 'bin', 'activate')
            add_external_hook(self.default_hook_file, os.getcwd(), hooktype='tree',
                          enter=['source %s' % activate_path],
                          exit=['deactivate'], unique=True)

    @eventhook('init-post-script')
    # source venv and capn
    def activate_capn(self, file):
        if self.active:
            # source capn and activate venv
            file.write("source .pin/env/bin/activate;")
            file.write("source capn;")

    @eventhook('destroy-post-exec')
    # remove capn hooks
    def remove_capn(self, cwd, root):
        remove_external_hook(self.default_hook_file, root)

register(CapnVenvPinHook)
