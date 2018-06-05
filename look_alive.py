#!/usr/local/bin/python3

'''
Program Name: look_alive.py

Synopsis:

        (1) Accepts a list of hostnames/domain names and attempts to resolve name to IP address
        (2) Next the program will determine, which systems are actually alive on the network using ping

'''

import os
import json
import sys
import getopt

filename = "names.txt"
host_dictionary = {}

def arguments(arguments):

    global filename

    try:
        opts, args = getopt.getopt(arguments[1:], "i", ["input"])
    except getopt.GetoptError as error:
        print(str(error))

    for opt, arg in opts:
        if opt == "i":
            filename = arg


# Generator function will create listing of hostnames
def list_file_contents():
    with open(filename) as handle:
        for line in handle:
            yield line.rstrip("\n")

# Function will create a dictionary with keys pointing toward hostnames
def create_dictionary_list():

        global host_dictionary

        hosts = list_file_contents()

        for host in hosts:
            host_dictionary[host] = []

        print("[+] Host Dictionary List Created:  %d  Entries" %len(host_dictionary))

# Split the addresses into array
def split_address_count(host,ranges):

    global host_dictionary

    split_address_list = ranges.split('\n')

    for index in range(len(split_address_list)):
        for ip in range(len(split_address_list[index].split(":",1))):
            if split_address_list[index].split(":",1)[ip] != "Address" and split_address_list[index].split(":",1)[ip] != "":
                host_dictionary[host].append(split_address_list[index].split(":",1)[ip])


# Function will take dictionary of host and perform nslookup on targets
def lookup_targets():

    global host_dictionary

    for host, fields in host_dictionary.items():

        ranges = os.popen("nslookup %s | tail -n +3 | grep -i 'address'" %host).read()
        split_address_count(host,ranges)


def write_results():

    with open("output_test.txt", "w") as handle:
            handle.write(json.dumps(host_dictionary, indent=4, sort_keys=True))


def ping_targets():

    for k,v in host_dictionary.items():
        for i in range(len(host_dictionary[k])):
            if os.system("ping -c 1 %s 1>/dev/null" %host_dictionary[k][i]) == 0:
                print("[+] %s alive at => %s" %(k, host_dictionary[k][i]))
                break

def main():

    create_dictionary_list()
    lookup_targets()
    write_results()
    ping_targets()

main()