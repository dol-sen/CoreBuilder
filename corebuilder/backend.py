#!/usr/bin/env python

'''
    CoreBuilder Backend
    hold our instance of the package manager backend.

    Copyright (C) 2012
    Brian Dolbec,

'''

from pmbackends import PMBackend
from pmbackends.config import BackendConfig

Choices = {"portage": "portage_2_2", "pkgcore": 'pkgcore', "portage-2.2": "portage_2_2" }
BACKEND = Choices["pkgcore"]

config = BackendConfig(sync="pmaint --sync")

baseconfig = None #os.path.join(EPREFIX, "/etc/corebuilder", "commands.cfg")

pms_instance = PMBackend()
pms_instance.load(BACKEND, baseconfig, config)

