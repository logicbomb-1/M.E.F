FROM python:3
COPY ./requirements.txt /requirements.txt
COPY ./endpoint_finder.py /endpoint_finder.py
WORKDIR /
RUN pip3 install -r requirements.txt
RUN apt-get update && apt-get install -y \ 
    nmap \
    vim
RUN wget https://github.com/projectdiscovery/subfinder/releases/download/v2.4.5/subfinder_2.4.5_linux_amd64.tar.gz
RUN tar -xzvf subfinder_2.4.5_linux_amd64.tar.gz && \
    mv subfinder /usr/local/bin/
