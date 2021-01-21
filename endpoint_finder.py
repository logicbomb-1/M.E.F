import nmap
import json
import requests
import subprocess
import argparse
import warnings
from queue import Queue
from threading import Thread

warnings.filterwarnings("ignore", message="Unverified HTTPS request")
domain_q = Queue(maxsize=0)
port_q = Queue(maxsize=0)


def creating_nmap(file_path):
    num_threads = 100
    print("Scanning Port. Please wait....")
    for i in range(num_threads):
        worker = Thread(target=port_scan, args=(port_q,))
        worker.setDaemon(True)
        worker.start()
    file1 = open(file_path, "r")
    Lines = file1.readlines()
    for line in Lines:
        port_q.put(line)
    port_q.join()  # start ending the workers by monitoring the queue.


def port_scan(q1):
    str = list()
    nm = nmap.PortScanner()
    while True:
        line = q1.get()
        host = line
        res = nm.scan(
            hosts=host,
            arguments="-p21,22,23,25,3301,9001,9200,9201,5601,5602,5600,5601,9300,9301,9600,9601,8080,8090,27017,27018,27019,6379,16379,26379,6380,2375,2376,2374,3389,5500,6666,28015,6501,4369,6984,5050,5000,29015,9042,7199, --open",
        )
        res = res["scan"]
        for key in res:
            ip = key
            ports = res[ip]["tcp"].keys()
            for port in ports:
                str.append(line)
                str.append("-->")
                str.append(port)
                str.append(": ")
                str.append(res[ip]["tcp"][port]["name"])
        if str:
            print(str)
        q1.task_done()


def creating_endpoint(file_path):
    num_threads = 1000
    print("Finding misconfigured endpoint. Please wait....")
    for i in range(num_threads):
        worker = Thread(target=endpoint_check, args=(domain_q,))
        worker.setDaemon(True)
        worker.start()
    rep = list()
    endpoints = [
        "/env",
        "/.git/HEAD",
        "/beans",
        "/routes",
        "/.git/HEAD/logs",
        "/.git/index",
        "/.git/config",
        "/.git-credentials",
        "/.svn/entries",
    ]
    file1 = open(file_path, "r")
    Lines = file1.readlines()
    protocols = ["https://"]
    for protocolType in protocols:
        for endpoint in endpoints:
            for line in Lines:
                line = line.strip()
                full_url = protocolType + line + endpoint
                domain_q.put(full_url)
    domain_q.join()


def endpoint_check(q):
    while True:
        full_url = q.get()
        try:
            req = requests.get(full_url, timeout=5, verify=False, allow_redirects=False)
            if req.status_code == 200:
                print(full_url)
        except:
            pass
        q.task_done()


def subdomain_finder(file_path):
    print("Finding Subdomain. Please wait.")
    command1 = "subfinder -silent -dL" + " " + file_path + " " + "-o output.txt"
    process = subprocess.Popen(
        command1, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True
    )
    out, err = process.communicate()
    if err.decode() != "":
        print(err.decode())


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
    domains = "output.txt"
    creating_endpoint(domains)
    creating_nmap(domains)
