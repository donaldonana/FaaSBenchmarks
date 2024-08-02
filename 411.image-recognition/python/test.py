import datetime, json, os, uuid

# Extract zipped torch model - used in Python 3.8 and 3.9
# The reason is that torch versions supported for these Python
# versions are too large for Lambda packages.
if os.path.exists('function/torch.zip'):
    import zipfile, sys
    # we cannot write to the read-only filesystem
    zipfile.ZipFile('function/torch.zip').extractall('/tmp/')
    sys.path.append(os.path.join(os.path.dirname(__file__), '/tmp/.python_packages/lib/site-packages'))
    


import torch
    






