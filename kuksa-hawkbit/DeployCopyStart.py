#!/usr/bin/python3

# Copyright (c) 2018 Eclipse KUKSA project
#
# This program and the accompanying materials are made available under the
# terms of the Eclipse Public License 2.0 which is available at
# http://www.eclipse.org/legal/epl-2.0
#
# SPDX-License-Identifier: EPL-2.0
#
# Contributors: Robert Bosch GmbH
#
# This is just an example for a deployment method. It expects a tar.bz2
# archive. The archis extrated to /usr/apps/<random_uuid> (make sure
# /usr/apps exists) and start.sh, which is expected to be at the top
# level of the archive is executed.
#
# This deployment module does not take care of starting the deployed 
# software during boot, but start.sh might take care of this

import subprocess
import uuid
from pathlib import Path

def deploy(f):
    target=str(uuid.uuid1())
    print("Trying to deploy "+str(f)+" as "+str(target))
    print("Extracting ");
    
    ret=subprocess.call("mkdir /usr/apps/"+target+" && tar -xvjf "+str(f)+" -C /usr/apps/"+target,shell=True)
    print("Return code "+str(ret))

    startScript=Path("/usr/apps/"+target+"/start.sh")
    if not startScript.is_file() :
        print("Can't start, no start script")
        return

    print("Starting....")
    ret=subprocess.call("chmod +x /usr/apps/"+target+"/start.sh",shell=True)
    print("Return code "+str(ret))
    ret=subprocess.call("cd  /usr/apps/"+target +" && /usr/apps/"+target+"/start.sh &",shell=True)
    print("Return code "+str(ret))

