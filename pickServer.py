#!/usr/bin/python
# Takes a list of servers and pings them to figure out
# which one is the "best" one to connect to.


import subprocess
import re

serverList = ["www.google.com", "www.yahoo.com", "www.bing.com"]
pingStats = []


def ping(server):
    ping = subprocess.Popen(
        ["ping", "-c", "4", server],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    out, error = ping.communicate()
    return out


def get_avg_ping(pingResults):
    match = re.search(r"(\d+.\d+)/(\d+.\d+)/(\d+.\d+)/(\d+.\d+)", pingResults)
    return match.group(2)


def get_packet_loss(pingResults):
    match = re.search(r"(\d+.\d+\%)", pingResults)
    return match.group().strip("%")

for server in serverList:
    tempDict = {}
    pingResults = ping(server)
    get_packet_loss(pingResults)
    tempDict = {"server": server, "avgPing": get_avg_ping(pingResults), "packetLoss": get_packet_loss(pingResults)}
    pingStats.append(tempDict)

print pingStats[0]
