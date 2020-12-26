# Misconfigured Endpoint Finder (M.E.F)

This is M.E.F, a python project to detect exposed misconfigured enpoint in the given list of domains along with performing port scanning of critical ports. It scans the domains to get thier subdomains using subfinder and perform port scanning and find misconfigured enpoint in the subdomains of domains list.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

It needs the below packages to be in your system setup. To install packages, run pip3 install -r requirements.txt. Note - You need to install subfinder explicitly. 

```
Subfinder
certifi
chardet
idna
python-nmap
requests
urllib3
```

### Installing

A step by step series of examples that tell you how to get a development env running

Say what the step will be

```
Give the example
```

And repeat

```
until finished
```

End with an example of getting some data out of the system or using it for a little demo

## Deployment

To quickly run the docker image, run the below command 
```
docker run -it --rm --name eef16 -v /targets.txt:/targets.txt logicbomb1/docker-eef:latest python3 endpoint_finder.py -p targets.txt
```

where targets.txt is the file containing all the domains.


## Built With

* [Python](https://www.python.org/) - The scritping language used
* [Docker](https://www.docker.com/) - Used to dockerize

## Contributing

Please feel free to contribute to make it much better and faster.

## Versioning

I am  using [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/your/project/tags). 

## Authors

* **Avinash Jain** - [logicbomb-1](https://twitter.com/logicbomb_1)

See also the list of [contributors](https://github.com/logicbomb-1/M.E.F/contributors) who participated in this project.

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details

## Acknowledgments

* Subfinder from Projectdiscovery (https://github.com/projectdiscovery/subfinder)
