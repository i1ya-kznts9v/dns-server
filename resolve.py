import dns.message
import dns.name
import dns.query
import dns.rdata
import dns.rdataclass


cache = dict()


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
