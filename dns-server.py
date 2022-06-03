import copy
import socket
import dns.rdatatype

from resolve import resolve


client_socket = dns.query._make_socket(
    af=socket.AF_INET,
    type=socket.SOCK_DGRAM,
    source=("localhost", 53),
)


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
