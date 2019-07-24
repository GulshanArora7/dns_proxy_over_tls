# dns_proxy_over_tls application

## Prerequisites

* Python3 or Greater
* Docker (To run application inside docker conatiner)

## Installation

* To install docker 
  * [Docker](https://docs.docker.com/install/)

* To Install Python
  * [Python](https://realpython.com/installing-python/)



## To run the dns_proxy_over_tls application

* To run it as Python application from CLI with default
    ```
    $ export PROXY_PATH=53
    $ export CA_CERT_PATH="/etc/ssl/cert.pem"
    $ cd dns_proxy_over_tls_python
    $ chmod +x dns_proxy_over_tls.py
    $ sudo ./dns_proxy_over_tls.py --port PROXY_PATH --ca_path $CA_CERT_PATH
    
    To test the code, use dig command
        example: dig @localhost google.com
    ```
* To run it as docker application with default proxy_port and certificate_path
    ```
    $ cd dns_proxy_over_tls_python
    $ docker build -t dns_proxy -f Dockerfile .
    $ docker run -d --name dns_proxy_default_port -p 53:53/tcp -p 53:53/udp dns_proxy
    
    To test the code, use dig command
        example: dig @localhost google.com
    ```
* To run it as docker application with external proxy_port
    $ cd dns_proxy_over_tls_python
    $ docker build -t dns_proxy -f Dockerfile .
    $ docker run -d --name dns_proxy_ext_port -e PROXY_PORT=94 -p 94:94/tcp -p 94:94/udp dns_proxy
    
     To test the code, use dig command
        example: dig @localhost -p 94 google.com
    ```
* To run it as docker application with external proxy_port and external certificate_path
    ```
    $ cd dns_proxy_over_tls_python
    $ docker build -t dns_proxy -f Dockerfile .
    $ docker run -d --name dns_proxy_ext_cert_port -e PROXY_PORT="port_number" CA_CERT_PATH="path-of-your-cert" -p "port_number":"port_number"/tcp -p "port_number":"port_number"/udp dns_proxy
    ```



## Directory Structure

1. `README.me`: README document
2. `Dockerfile`: Dockerfile to build your own image
3. `dns_proxy_over_tls.py`: python application for providing dns proxy over tls with cloudfare dns(1.1.1.1).
4. `docker_commands.txt`: Docker commands for reference

## Reference Links
* [Docker](https://docs.docker.com/)
* [Python-SSL](https://docs.python.org/3/library/ssl.html)
* [Python-Socket](https://docs.python.org/3/library/socket.html)
