#!/usr/bin/python3 -u
import re, sys, os
import requests
import json
import lxml.html

print("Fetching archive mirrors...", file=sys.stderr)
r = requests.get("https://launchpad.net/ubuntu/+archivemirrors")
h = lxml.html.fromstring(r.content)

archive_http_mirrors = set(x.attrib["href"] for x in h.xpath("//a[text()='http']"))
archive_ftp_mirrors = set(x.attrib["href"] for x in h.xpath("//a[text()='ftp']"))
assert archive_http_mirrors, "Could not get regular HTTP mirrors"
assert archive_ftp_mirrors, "Could not get regular FTP mirrors"

# Ensure all repositories are slash-ended
assert all(x.endswith("/") for x in archive_http_mirrors)
archive_ftp_mirrors = set(
    x if x.endswith("/") else x + "/"
    for x in archive_ftp_mirrors
)
assert all(x.endswith("/") for x in archive_ftp_mirrors)

print("Fetching packages.ubuntu.com mirrors...", file=sys.stderr)
r = requests.get("http://packages.ubuntu.com/trusty/all/openarena-data/download")
h = lxml.html.fromstring(r.content)

package_mirrors = set(
    re.sub(r"pool/universe/.*", "", x.attrib["href"])
    for x in h.xpath("//div[@class='cardleft' or @class='cardright']//a")
)
assert package_mirrors, "Could not get additional HTTP mirrors"
# Mix both mirrors
archive_http_mirrors = archive_http_mirrors.union(package_mirrors)
assert all(x.endswith("/") for x in archive_http_mirrors)

print("Fetching CD mirrors...", file=sys.stderr)
r = requests.get("https://launchpad.net/ubuntu/+cdmirrors")
h = lxml.html.fromstring(r.content)

cd_http_mirrors = set(x.attrib["href"] for x in h.xpath("//a[text()='http']"))
assert cd_http_mirrors, "Could not get CD HTTP mirrors"
assert all(x.endswith("/") for x in cd_http_mirrors)

json_output = json.dumps([{
    "mirrors": sorted(archive_http_mirrors),
    "substitution": "http://ubuntu.mirrors.ovh.net/ftp.ubuntu.com/ubuntu/",
}, {
    "mirrors": sorted(archive_ftp_mirrors),
    "substitution": "ftp://ubuntu.mirrors.ovh.net/ftp.ubuntu.com/ubuntu/",
}, {
    "mirrors": sorted(cd_http_mirrors),
    "substitution": "http://ubuntu-releases.mirrors.free.org/",
}], sort_keys=True, indent=4, separators=(',', ': '))

print(json_output)
