import os
from collections import Counter
from queue import PriorityQueue
from functools import reduce


EXAMPLE = """38006F45291200"""
EXAMPLE_2 = """EE00D40C823060"""
TEST = """8A004A801A8002F478"""
TEST_2 = """620080001611562C8802118E34"""
TEST_3 = """C0015000016115A2E0802F182340"""
TEST_4 = """A0016C880162017C3686B18A3D4780"""
COMPUTE = """9C0141080250320F1802104A08"""


def parse_packets(packets, max_rounds=-1):
    pks = []

    i = 0
    turn = 0
    while i < len(packets) and (max_rounds == -1 or turn < max_rounds) and packets[i:len(packets)] != '0' * (len(packets) - i):
        turn += 1
        version = int(packets[i:(i + 3)], 2)
        i += 3
        type_id = int(packets[i:(i + 3)], 2)
        i += 3

        if type_id == 4:
            literal_bits = ""
            while packets[i] != '0':
                i += 1
                literal_bits += packets[i:(i + 4)]
                i += 4
            i += 1
            literal_bits += packets[i:(i + 4)]
            i += 4

            pks.append({'version': version, 'type_id': type_id, 'literal': int(literal_bits, 2)})
        else:
            if packets[i] == '0':
                i += 1
                sub_packets_len = int(packets[i:(i + 15)], 2)
                i += 15

                # parse sub packets
                sub_packets, after_i = parse_packets(packets[i:(i + sub_packets_len)])
                i += after_i

                pks.append({'version': version, 'type_id': type_id, 'length_type_id': 0, 'sub_packets': sub_packets})
            elif packets[i] == '1':
                i += 1
                sub_packets_count = int(packets[i:(i + 11)], 2)
                i += 11

                # parse sub packets
                sub_packets, after_i = parse_packets(packets[i:], max_rounds=sub_packets_count)
                i += after_i

                pks.append({'version': version, 'type_id': type_id, 'length_type_id': 1, 'sub_packets': sub_packets})
            else:
                print("this shouldn't have happened")

    return pks, i


def compute(packet):
    if packet['type_id'] == 4:
        packet['subs'] = str(packet['literal'])
        return packet

    computed = [compute(pkt) for pkt in packet['sub_packets']]
    version = packet['version'] + sum(pkt['version'] for pkt in computed)
    literals = [pkt['literal'] for pkt in computed]
    subs = [pkt['subs'] for pkt in computed]

    operations = {
        0: sum,
        1: lambda xs: reduce(lambda x, y: x * y, xs),
        2: min,
        3: max,
        5: lambda xs: reduce(lambda x, y: x > y, xs),
        6: lambda xs: reduce(lambda x, y: x < y, xs),
        7: lambda xs: reduce(lambda x, y: x == y, xs),
    }

    representation = {
        0: lambda xs: '({})'.format('+'.join(xs)),
        1: lambda xs: '({})'.format('*'.join(xs)),
        2: lambda xs: 'min([{}])'.format(','.join(xs)),
        3: lambda xs: 'max([{}])'.format(','.join(xs)),
        5: lambda xs: '({} > {})'.format(xs[0], xs[1]),
        6: lambda xs: '({} < {})'.format(xs[0], xs[1]),
        7: lambda xs: '({} == {})'.format(xs[0], xs[1]),
    }

    return {'version': version,
            'literal': operations[packet['type_id']](literals),
            'subs': representation[packet['type_id']](subs)}


def solution():
    with open(os.path.join(os.path.dirname(__file__), './input.txt'), 'r') as fd:
        transmission = fd.read()

    # transmission = COMPUTE
    packets = ""
    for hexadecimal in transmission:
        packets += "{0:04b}".format(int(hexadecimal, 16))

    parsed = parse_packets(packets)[0]
    computed = compute(parsed[0])

    print("PART 1:", computed['version'])
    print("PART 2:", computed['literal'], '=', computed['subs'])


if __name__ == '__main__':
    solution()
