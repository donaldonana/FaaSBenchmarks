import os
import json
import csv

def energy():

    headers = ['duration_seconds', 'cpu0_package_joules', 'cpu0_core_joules', 'cpu0_uncore_joules', 'cpu0_dram_joules', 'video', 'library']
    data = []

    for dir in os.listdir("./Energy"):

        # For each subfolder in Energy folder (1Mb.avi)
        dir_path = os.path.join("./Energy", dir)
        video = dir.replace(".avi", "")
        for file in os.listdir(dir_path):

            # For each file in the subfolder (pillow1Mb.avi.txt)
            file_paht = os.path.join(dir_path, file)
            library = file.replace(video+".avi.txt", "")

            with open(file_paht, 'r') as file:
                lines = file.readlines()
            
            for line in lines:
                line = line.strip()
                if line.startswith('duration_seconds'):
                    duration_seconds = line.split('=')[1]
                if line.startswith('cpu0_package_joules'):
                    package_joules = line.split('=')[1]
                elif line.startswith('cpu0_core_joules'):
                    core_joules = line.split('=')[1]
                elif line.startswith('cpu0_uncore_joules'):
                    uncore_joules = line.split('=')[1]
                elif line.startswith('cpu0_dram_joules'):
                    dram_joules = line.split('=')[1]

                    # Append the extracted values to the data list
                    data.append([duration_seconds, package_joules, core_joules, uncore_joules, dram_joules, video, library])

    with open("energy.csv", 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(headers)  # Write the header
        writer.writerows(data)    # Write the data
 


def parse_json_objects(log_content):
    json_objects = []
    buffer = ""
    brace_count = 0

    for char in log_content:
        buffer += char
        if char == '{':
            brace_count += 1
        elif char == '}':
            brace_count -= 1
        
        if brace_count == 0 and buffer.strip():
            try:
                json_objects.append(json.loads(buffer.strip()))
                buffer = ""
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON: {e}")
                buffer = ""

    return json_objects



# Read the contents of the log file
with open('result.txt', 'r') as file:
    log_content = file.read()

# Parse the log content into JSON objects
json_objects = parse_json_objects(log_content)

# Define the CSV file headers
headers = ["compute_time", "download_size", "download_time", "video", "library", "upload_size", "upload_time"]

# Open the CSV file for writing
with open('result.csv', 'w', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=headers)
    writer.writeheader()

    # Process each JSON object
    for data in json_objects:
        try:
            body = data["body"]
            
            # Write the row to the CSV file
            writer.writerow({
                "compute_time": body["compute_time"],
                "download_size": body["download_size"],
                "download_time": body["download_time"],
                "video": body["video"].replace(".avi", ""),
                "library": body["library"],
                "upload_size": body["upload_size"],
                "upload_time": body["upload_time"]
            })
        except KeyError as e:
            print(f"Missing key in data: {e}")

print("CSV file has been created successfully.")


energy()