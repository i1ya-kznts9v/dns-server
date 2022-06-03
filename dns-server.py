import copy
import socket

import dns.message
import dns.name
import dns.query
import dns.rdata
import dns.rdataclass
import dns.rdatatype


cache = dict()

client_socket = dns.query._make_socket(
    af=socket.AF_INET,
    type=socket.SOCK_DGRAM,
    source=("localhost", 53),
)


def resolve(query):
    if query in cache:
        return cache[query]

    query_message = dns.message.make_query(
        qname=query,
        rdtype=dns.rdatatype.A,
        rdclass=dns.rdataclass.IN,
    )

    with open('./root_dns_servers.txt') as file:
        root_dns_servers = file.read().splitlines()

        for root_dns_server in root_dns_servers:
            response = rec_resolve(query_message, root_dns_server)

            if response:
                cache[query] = response
                return response


def rec_resolve(query, where):
    response = dns.query.udp(
        q=query,
        where=where,
        raise_on_truncation=False,
    )

    if response:
        if response.answer:
            return response
        elif response.additional:
            for additional in response.additional:
                if additional.rdtype != dns.rdatatype.A:
                    continue
                for add in additional:
                    new_response = rec_resolve(query, str(add))
                    if new_response:
                        return new_response
    return response


if __name__ == "__main__":
    while True:
        request, _, from_address = dns.query.receive_udp(client_socket)

        query = str(request.question[0]).split()[0]
        response = copy.deepcopy(request)

        result = resolve(dns.name.from_text(query))
        if result:
            response.answer = result.answer
            response.flags |= dns.flags.QR | dns.flags.RA
            if response.flags & dns.flags.AD:
                response.flags ^= dns.flags.AD

        dns.query.send_udp(client_socket, response, from_address)
