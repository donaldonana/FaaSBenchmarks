import os
import time
import json
import numpy as np
import requests
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


def run(url, headers, data):

    i = 0
    while i < 10:

        meter.start()
        response = requests.post(url, headers=headers, json=data)
        meter.stop()

        emeasure = meter.get_trace()[0]
        json_dict = {
            "library" :  data.get("bib"),
            "package_0": emeasure.energy["package_0"] / 1e6,
            "dram_0":    emeasure.energy["dram_0"] / 1e6,
            "core_0":    emeasure.energy["core_0"] / 1e6,
            "uncore_0":  emeasure.energy["uncore_0"] / 1e6,
            "measure":   response.json()["body"],  # Parse the measure part as JSON
        }
        if i >= 2: 
            append_to_log_file(json_dict)
            
        i = i + 1
        



if __name__ == "__main__":

    url = "http://172.17.0.1:3233/api/v1/web/guest/default/thumb.json"
    headers = {'Content-Type': 'application/json'}
    
    bibs = ["pillow", "wand", "pygame", "opencv"]

    for i, bib in enumerate(bibs):

        data = {
            'bib': bib, 
            'access' :  os.getenv('AWS_SECRET_ACCESS_KEY'), 
            'key' : os.getenv('AWS_ACCESS_KEY_ID')
        }

        print(f"{i+1}...")

        run(url, headers, data)