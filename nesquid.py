#!/usr/bin/python3 -u
# URL rewriter for squid
import re, sys, os
import json

with open("/etc/squid3/mirrors.json", "r") as f:
    mirror_sets = json.load(f)

def rewrite_url(url):
    for mirror_set in mirror_sets:
        for mirror in mirror_set["mirrors"]:
            if url.startswith(mirror):
                return url.replace(mirror, mirror_set["substitution"])
    return ""

for line in sys.stdin:
    url = line.split()[0]
    print(rewrite_url(url))
