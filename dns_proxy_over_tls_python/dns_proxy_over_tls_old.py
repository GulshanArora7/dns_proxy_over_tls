#!/usr/bin/env python3
# Author : Gulshankumar Arora

import sys
import argparse
import binascii
import socket
import ssl
import threading
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def send_query(dns_address, query_data, ca_path):
    server = (dns_address, 853)
    socket_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_connection.settimeout(80)
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    context.load_verify_locations(ca_path)

    wrapped_socket = context.wrap_socket(socket_connection, server_hostname=dns_address)
    wrapped_socket.connect(server)
    logger.info("DNS Server Peer Certificate: %s", str(wrapped_socket.getpeercert()))

    tcp_query_details = "\x00".encode() + chr(len(query_data)).encode() + query_data
    logger.info("Client DNS Query Request: %s", str(tcp_query_details))
    wrapped_socket.send(tcp_query_details)
    response_data = wrapped_socket.recv(1024)
    return response_data


def thread_connection(query_data, address, socket_connection, dns_address, ca_path):

    query_answer = send_query(dns_address, query_data, ca_path)
    if query_answer is not None:
        logger.info("Reply from DNS with TLS Server: %s", str(query_answer))
        return_code_block = binascii.hexlify(query_answer[:6]).decode("utf-8")
        return_code = return_code_block[11:]
        if int(return_code, 16) == 1:
            logger.error("Unexpected Format: Error in processing the request, Return_Code = %s", return_code)
        elif int(return_code, 16) == 2:
            logger.error("Server Failure: Error in processing the request, Return_Code = %s", return_code)
        elif int(return_code, 16) == 3:
            logger.error("Domain Name Error: Error in processing the request, Return_Code = %s", return_code)
        elif int(return_code, 16) == 4:
            logger.error("Not Implemented: Error in processing the request, Return_Code = %s", return_code)
        elif int(return_code, 16) == 5:
            logger.error("Refused: Error in processing the request, Return_Code = %s", return_code)
        else:
            logger.info("Response from Proxy..Working..OK !!, Return_Code = %s", return_code)
            return_ans = query_answer[2:]
            socket_connection.sendto(return_ans, address)
    else:
        logger.warn("No Reply from the DNS Server")


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Script for DNS to DNS-over-TLS proxy")
    parser.add_argument("--port", type=int, default=53, required=False, help="Port Number to Listen [default: 53]")
    parser.add_argument("--address", type=str, default='0.0.0.0', required=False, help="External Proxy Interface Address [default: localhost(0.0.0.0)]")
    parser.add_argument("--dns", type=str, default="1.1.1.1", required=False, help="External DNS Server with TLS [default: 1.1.1.1]")
    parser.add_argument("--ca_path", type=str, default="/etc/ssl/cert.pem", required=False, help="CA Cert File path [default: /etc/ssl/cert.pem]")
    return parser.parse_args()

def main():
    try:
        arguments = parse_arguments()
        port_number = arguments.port
        host_address = arguments.address
        dns_address = arguments.dns
        ca_path = arguments.ca_path
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as socket_connection:
            socket_connection.bind((host_address, port_number))
            while True:
                query_data, address = socket_connection.recvfrom(4096)
                threading.Thread(
                    target=thread_connection, args=(query_data, address, socket_connection, dns_address, ca_path)
                ).start()
    except Exception as e:
        logger.error(e)

if __name__ == '__main__':
    try:
        main()
    except Exception as error:
        print(error)
        sys.exit(1)