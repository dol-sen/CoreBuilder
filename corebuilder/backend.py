#!/usr/bin/env python

'''
    CoreBuilder Backend
    hold our instance of the package manager backend.

    Copyright (C) 2012
    Brian Dolbec,

'''

import os

from pmbackends import PMBackend
from pmbackends.config import BackendConfig
from CoreBuilder.settings import BACKEND, INSTALL_TARGETS

Choices = {"portage": "portage_2_2", "pkgcore": 'pkgcore', "portage-2.2": "portage_2_2" }

config = BackendConfig(sync="pmaint --sync")



def load_target(target_name=None):
    """Set up our environment PORTAGE_CONFIGROOT
    so it can load the prefix target
    """
    if not target_name:
        return None
    target = INSTALL_TARGETS[target_name]
    if target_name in ["base_system"]:
        if 'PORTAGE_CONFIGROOT' in os.environ:
            os.environ.pop('PORTAGE_CONFIGROOT')
        if 'ROOT' in os.environ:
            os.environ.pop('ROOT')
    else:
        os.environ['PORTAGE_CONFIGROOT'] = target['PORTAGE_CONFIGROOT']
        os.environ["ROOT"] = target["ROOT"]
    baseconfig = None
    print 'backend.py, load_target():', target_name, target
    pms_instance = PMBackend()
    print 'backend.py, load_target(): PmBackend instance created', pms_instance
    pms_instance.load(Choices[BACKEND], baseconfig, config)
    print 'backend.py, load_target(): pms_instance initialized', pms_instance
    return pms_instance
