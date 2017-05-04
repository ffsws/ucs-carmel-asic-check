# Carmel ASIC CRC checker

This is a utility for collecting, structuring, and reporting any errors from the output of

`show hardware internal carmel crc`

from a list of Cisco UCS Fabric Interconnects.

This command for the carmel ASIC shows where CRC packets have been received and where they have been forwarded to, and more importantly whether they have been stomped or not.
Since both Nexus 5000 and UCS NX-OS operation is cut-through, switching mode frames with incorrect Frame Check Sequence (FCS) are only stomped before forwarding.
It is important to find out where the corrupted frames come from.


For more infomation on these errors see:
https://supportforums.cisco.com/discussion/13012591/definition-show-hardware-internal-carmel-crc


Optionally, if any of the interfaces report non-zero values, a notification can
be provided via spark


## Requirements

* Python 2.7
* Paramiko 2.1.2


## Installation

```
git clone https://github.com/kecorbin/carmel-crc-errors
cd carmel-crc-errors
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt

```

## Configuration

Modify [config.yaml](./config.yaml) with the appropriate values for your environment


## Running

Execute the script

`python main.py`
