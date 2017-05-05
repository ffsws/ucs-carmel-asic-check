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
be provided via [Cisco Spark](https://www.ciscospark.com/)


## Requirements

* Python 2.7
* Paramiko 2.1.2
* Requests 2.13.0
* PyYAML 3.12


## Installation

```
git clone https://github.com/kecorbin/ucs-carmel-asic-check
cd ucs-carmel-asic-check
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt

```
Note: If you do not have virtualenv installed use pip to install

`pip install virtualenv`

## Configuration

Modify [config.yaml](./config.yaml) with the appropriate values for your environment

If you are using Cisco Spark for notifications, you can find your Spark token, and Room Id by visiting [Spark for Developers](https://developer.ciscospark.com/)


## Running

Execute the script

`python main.py`
