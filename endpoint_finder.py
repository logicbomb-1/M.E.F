import nmap
import json
import requests
import subprocess
import argparse
import warnings

warnings.filterwarnings("ignore", message="Unverified HTTPS request")


def port_scan(file_path):
    str = list()
    nm = nmap.PortScanner()
    file1 = open(file_path, "r")
    print("Scanning Port. Please wait.")
    Lines = file1.readlines()
    for line in Lines:
        str.append(line)
        str.append("-->")
        host = line.strip()
        res = nm.scan(
            hosts=host,
            arguments="-p21,22,23,25,3301,9001,9200,9201,5601,5602,5600,5601,9300,9301,9600,9601,8080,8090,27017,27018,27019,6379,16379,26379,6380,2375,2376,2374,3389,5500,6666,28015,6501,4369,6984,5050,5000,29015,9042,7199, --open",
        )
        res = res["scan"]
        for key in res:
            ip = key
            ports = res[ip]["tcp"].keys()
            for port in ports:
                str.append(port)
                str.append(": ")
                str.append(res[ip]["tcp"][port]["name"])
    print(str)

def subdomain_finder(file_path):
    print("Finding Subdomain. Please wait.")
    open("domains.txt", "w").close()
    command1 = "subfinder -silent -dL" + " " + file_path + " " + "-o domains.txt"
    process = subprocess.Popen(
        command1, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True
    )
    out, err = process.communicate()
    if err.decode() != "":
        print(err.decode())

def endpoint_check(file_path):
    print("Finding exposed endpoint. Please wait.")
    rep = list()
    endpoints = [
        "/info",
        "/auditevents",
        "/health",
        "/metrics",
        "/loggers",
        "/httptrace",
        "/env",
        "/flyway",
        "/liquidbase",
        "/mappings",
        "/scheduledtasks",
        "/logfile",
        "/heapdump",
        "/threaddump",
        "/features",
        "/.git/HEAD",
        "/beans",
        "/routes",
        "/.git/HEAD",
        "/.git/index",
        "/.git/config",
        "/.gitignore",
        "/.git-credentials",
        "/composer.lock",
        "/.svn/wc.db",
        "/.svnignore",
        "/CVS/Entries",
        "/.cvsignore",
        "/.idea/misc.xml",
        "/.idea/workspace.xml",
        "/.DS_Store",
        "/.svn/all-wcprops",
        "/.svn/entries",
        "/.bzr/README",
        "/.hg/store/fncache",
        "/.bzr/checkout/dirstate",
        "/config/",
        "/api/v1/nodes",
    ]
    file1 = open(file_path, "r")
    Lines = file1.readlines()
    protocols = ["https://"]
    for protocolType in protocols:
        for endpoint in endpoints:
            for line in Lines:
                line = line.strip()
                full_url = protocolType + line + endpoint
                try:
                    req = requests.get(full_url, timeout=5, verify=False)
                    if req.status_code == 200:
                        rep.append(full_url)
                        print(full_url)
                    else:
                        continue
                except Exception as e:
                    # Any exception apart from ConnectionError will be handled
                    continue
    print(rep)


if __name__ == "__main__":
    # Create the parser
    parser = argparse.ArgumentParser(description="Path of domain file")
    # Add the arguments
    parser.add_argument(
        "-p", "--path", type=str, required=True, help="Path of domain file"
    )
    args = parser.parse_args()
    file_path = args.path
    subdomain_finder(file_path)
    domains = "domains.txt"
    port_scan(domains)
    endpoint_check(domains)
