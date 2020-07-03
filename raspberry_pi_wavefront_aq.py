#!/usr/bin/env python3

# Air Quality Data Streaming to VMware Tanzu Observability by Wavefront

################################################################################
### Copyright (C) 2020 VMware, Inc.  All rights reserved.
### SPDX-License-Identifier: BSD-2-Clause
################################################################################

import serial, time
from time import gmtime, strftime
from datetime import datetime
 
ser = serial.Serial('/dev/ttyUSB0')
 
 
from wavefront_sdk import WavefrontProxyClient
wavefront_sender = WavefrontProxyClient(
   host="ec2-A-B-C-D.eu-west-2.compute.amazonaws.com",
   metrics_port=2878,
   distribution_port=2878,
   tracing_port=30000,
)
 
while True:
    now = datetime.now()
    timestamp_nico = datetime.timestamp(now)
    print("timestamp =", timestamp_nico)
    data = []
    for index in range(0,10):
        datum = ser.read()
        data.append(datum)
     
    pmtwofive = int.from_bytes(b''.join(data[2:4]), byteorder='little') / 10
    print(pmtwofive)
    wavefront_sender.send_metric(name="nvibert.pm2.5", value=pmtwofive, timestamp=timestamp_nico, tags={"city": "manchester"}, source="nvibert_rapsberrypi")
    print(strftime("%Y-%m-%d %H:%M:%S", gmtime()))
    pmten = int.from_bytes(b''.join(data[4:6]), byteorder='little') / 10
