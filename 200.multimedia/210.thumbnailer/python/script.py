import os
import time
import json
import numpy as np
import subprocess
from multiprocessing import Process
from pyJoules.device import DeviceFactory
from pyJoules.energy_meter import EnergyMeter
from pyJoules.device.rapl_device import RaplPackageDomain, RaplDramDomain, RaplUncoreDomain, RaplCoreDomain

domains = [
    RaplPackageDomain(0), 
    RaplDramDomain(0), 
    RaplUncoreDomain(0),
    RaplCoreDomain(0)
]

devices = DeviceFactory.create_devices(domains)
meter = EnergyMeter(devices)


def append_to_log_file(json_dict, filename='result.json'):
    # Check if the file exists
    if os.path.exists(filename):
        # Open the file and read the content
        with open(filename, 'r') as file:
            try:
                data = json.load(file)
                if not isinstance(data, list):
                    data = []
            except json.JSONDecodeError:
                data = []
    else:
        data = []

    # Append the new json_dict to the list
    data.append(json_dict)

    # Write the updated list back to the file
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)


def run(bib):
     
    i = 0
    
    while i < 10:

        meter.start(tag=bib)
        result = subprocess.run(['wsk', 'action', 'invoke', 'thumb', '--param', 'bib', bib, '--result'], capture_output=True, text=True) #invoke the action
        meter.stop()

        measurement = meter.get_trace()[0]

        json_dict = {
            "library" : bib,
            "measure": json.loads(result.stdout),  # Parse the measure part as JSON
            "package_0": measurement.energy["package_0"] / 1e6,
            "dram_0": measurement.energy["dram_0"] / 1e6,
            "core_0": measurement.energy["core_0"] / 1e6,
            "uncore_0": measurement.energy["uncore_0"] / 1e6,
        }
        # Append to log file for analyse
        if i >= 2: 
            append_to_log_file(json_dict)

        i = i + 1
        
 

if __name__ == "__main__":

    bibs = ["pillow", "wand", "pygame", "opencv"]
    
    # For each library run an experiment
    for i, bib in enumerate(bibs):
        
        print(f"{i+1}...")

        run(bib)
  