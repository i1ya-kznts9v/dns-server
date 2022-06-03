# DNS server on Python

A DNS server refers to the server component of the Domain Name System (DNS), 
one of the two principal namespaces of the Internet. The most important 
function of DNS servers is the translation (resolution) of human-memorable 
domain names (example.com) and hostnames into the corresponding numeric 
Internet Protocol (IP) addresses (93.184.216.34), the second principal
name space of the Internet, which is used to identify and locate computer 
systems and resources on the Internet.

# Requirements

- Python 3.9 or later
- `pip install -r requirements.txt`

# Usage

To run DNS server from repository root use

```
sudo python3 dns-server.py
```

In the file `root_dns_servers.txt` you can configure root DNS servers
while it is running. Initially, well-known root DNS servers are 
configured there, but you can specify others (for example, `1.1.1.1` 
or `8.8.8.8`).

To start using the DNS server, run in another terminal

- On Linux `dig [domain] @127.0.0.1`
- On MacOS `dig @127.0.0.1 [domain]`
- On Windows `nslookup [domain] 127.0.0.1`
