import re
import os
import requests
import argparse

from dataclasses import dataclass


TEMPLATE_FILE = "src/template.ovpn"
TEMPLATE_PROTOCOL = "proto udp"
TEMPLATE_REMOTE = "remote"
VPNGATE_RE = (
    "do_openvpn\.aspx\?fqdn=(.*)&ip=(([0-9]{1,3}\.){3}[0-9]{1,3})&tcp=(\d*)&udp=(\d*)"
)

with open(TEMPLATE_FILE, "r") as f:
    TEMPLATE_CONFIG = f.read()


@dataclass
class VpnOption:
    ddns_hostname: str
    ip: str
    tcp_port: int
    udp_port: int

    def __init__(self, **kwargs):
        self.__dict__ |= kwargs

    @property
    def protocol(self):
        return "tcp" if self.tcp_port else "udp"

    @property
    def port(self):
        return self.tcp_port or self.udp_port


def parse(response):
    return [
        {
            "ddns_hostname": ddns_hostname,
            "ip": ip,
            "tcp_port": int(tcp_port) or None,
            "udp_port": int(udp_port) or None,
        }
        for ddns_hostname, ip, trash, tcp_port, udp_port in re.findall(
            VPNGATE_RE, response
        )
    ]


def create_openvpn_config_file(option, file_name):
    try:
        with open(file_name, "w") as f:
            vpn_config = TEMPLATE_CONFIG.replace(
                TEMPLATE_PROTOCOL, "proto {}".format(option.protocol)
            ).replace(
                TEMPLATE_REMOTE,
                "remote {} {}".format(option.ddns_hostname, option.port),
            )
            f.write(vpn_config)
    except Exception as e:
        print(e)
    return True


def main():
    parser = argparse.ArgumentParser(
        description="Generates openvpn config files using vpngate."
    )

    parser.add_argument(
        "-f", dest="file", type=str, required=False, help=".html file instead of request")
    parser.add_argument(
        "-d", dest="directory", type=str, required=True, help="Output files directory"
    )
    parser.add_argument(
            "-v", "--verbose", action="store_true", help="Add extra verbosity"
    )
    args = parser.parse_args()

    if not os.path.isdir(args.directory):
        print("{} Directory doesn't exists".format(args.directory))
        return 1

    if args.file:
        if os.path.isfile(args.file):
            with open(args.file, "r") as f:
                vpngate_response = f.read()
        else:
            print("{} File doesn't exists".format(args.file))
            return 1
    else:
        with requests.get("https://www.vpngate.net/en/") as r:
            vpngate_response = r.text

    vpn_options = [VpnOption(**option) for option in parse(vpngate_response)]

    count = 0
    new_count = 0
    
    for option in vpn_options:
        file_name = "{}_{}_{}.ovpn".format(
            option.ddns_hostname, option.protocol, option.port
        )
        full_path=os.path.join(args.directory, file_name)

        if args.verbose:
            print(full_path)
        if not os.path.isfile(full_path):
            new_count+= 1
        if create_openvpn_config_file(
            option, full_path 
        ):
            count += 1
    print("Done. A total of {} configuration files have been generated, and {} of them are new.".format(count, new_count))


if __name__ == "__main__":
    main()
