import os
import time
import json
import numpy as np
import subprocess
from multiprocessing import Process
from pyJoules.device import DeviceFactory
from pyJoules.energy_meter import EnergyMeter
from pyJoules.energy_meter import measure_energy
from pyJoules.device.rapl_device import RaplPackageDomain, RaplDramDomain, RaplUncoreDomain, RaplCoreDomain


domains = [
    RaplPackageDomain(0), 
    RaplDramDomain(0), 
    RaplUncoreDomain(0),
    RaplCoreDomain(0)
]

devices = DeviceFactory.create_devices(domains)
meter = EnergyMeter(devices)


def append_to_log_file(json_dict, filename='energy.json'):
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



def action(bib):

    meter.start(tag=bib)
    result = subprocess.run(['wsk', 'action', 'invoke', 'thumb', '--param', 'bib', bib, '--result'], capture_output=True, text=True)
    meter.stop()

    measurement = meter.get_trace()[0]
    json_dict = {
        "tag": measurement.tag,
        "package_0": measurement.energy["package_0"] / 1e6,
        "dram_0": measurement.energy["dram_0"] / 1e6,
        "core_0": measurement.energy["core_0"] / 1e6,
        "uncore_0": measurement.energy["uncore_0"] / 1e6,
        "duration": measurement.duration,
        "measure": json.loads(result.stdout)  # Parse the measure part as JSON
        }
    # Append to log file for analyse
    append_to_log_file(json_dict)


def run(bib):

    """

    1. lambda_rate     : Le paramétre lambda désignant le nombre de requete par minute pour cette loi de Poisson
    2. duree           : La durée total  de la simulation
    3. 1 / lambda_rate : La durée moyenne entre deux événements successifs dans ce processus de Poisson (la moyenne des temps inter-arrivées)

    """
    lambda_rate = 10
    duree = 600  
    nbp = 2
    i = 0
    inter_arrival_times = np.random.exponential(1 / lambda_rate, int(lambda_rate * 1.5))*60

    # print(inter_arrival_times)
    
    debut = time.time()
    while (time.time() - debut) < duree:

        # List of process
        procs = []

        # Create and Start  nbp process following the poisson law
        for p in range(nbp):

            # Create
            proc = Process(target=action, args=(bib,))
            procs.append(proc)

            # Take account inter arrival time to start 
            time.sleep(inter_arrival_times[i])
            proc.start()

            # If we need more inter arrival time
            if i >= (len(inter_arrival_times) - 1):
                inter_arrival_times = np.append(inter_arrival_times, np.random.exponential(1 / lambda_rate, int(lambda_rate * 1.5))*60)
            i = i + 1

        # Complete the processes
        for proc in procs:
            proc.join() 
 
 
if __name__ == "__main__":

    bibs = ["pillow", "wand", "pygame", "opencv"]
    
    # For each library run an experiment
    for i, bib in enumerate(bibs):
        print(f"{i+1}...")
        run(bib)
    

 
