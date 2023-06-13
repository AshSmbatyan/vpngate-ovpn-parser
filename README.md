# vpngate-ovpn-parser
Simple Python script for parsing the Vpngate website and generating OpenVpn configuration files.

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
-----
## Installation

```shell
git clone https://github.com/AshSmbatyan/vpngate-ovpn-parser.git
cd vpngate-ovpn-parser
pip install -r requirements.txt
```
## Usage
Config files are being generated from the vpngate source. If no.html file is given with the `-f` option, it will be retrieved from https://www.vpngate.net/en/
```shell
python generate_config_files.py -d path_to_directory
```
Alternatively, instead of requesting, provide a .html file
```shell
python generate_config_files.py -f index.html -d path_to_directory
```
The curl command example below may be used to acquire a .html file
```shell
curl -sLo index.html --url 'https://www.vpngate.net/en/'
```
Help message
```
$ python generate_config_files.py -h

usage: generate_config_files.py [-h] [-f FILE] -d DIRECTORY [-v]

Generates openvpn config files using vpngate.

options:
  -h, --help     show this help message and exit
  -f FILE        .html file instead of request
  -d DIRECTORY   Output files directory
  -v, --verbose  Add extra verbosity
```
## License
This application licensed under the terms of the GNU General Public License v3.0.
[License: GPL v3](https://www.gnu.org/licenses/gpl-3.0)
