import abc
from enum import Enum
from typing import List, Tuple, Any, Callable


def hex2bits(hexstr: str) -> str:
    return ''.join([format(int(s, 16), "04b") for s in list(hexstr.strip())])


def bits2int(bits: str) -> int:
    return int(bits, 2)


def prod(list_of_ints: List[int]) -> int:
    result = 1
    for el in list_of_ints:
        result *= el
    return result


OPS = [sum, prod, min, max, lambda x: x, lambda x: int(x[0] > x[1]), lambda x: int(x[0] < x[1]),
       lambda x: int(x[0] == x[1])]


class OpCode(Enum):
    PLUS = 0
    MUL = 1
    MIN = 2
    MAX = 3
    VAL = 4
    LT = 5
    GT = 6
    EQ = 7

    def __str__(self):
        return self.name

    def operator(self):
        return OPS[self.value]


class Packet:
    def __init__(self, version: int, op: OpCode):
        self.version = version
        self.op = op

    @abc.abstractmethod
    def value(self) -> int:
        pass

    @abc.abstractmethod
    def apply(self, fn: Callable) -> Any:
        pass

    @staticmethod
    def read_value(body) -> Tuple[int, str]:
        result = ''
        while len(body) >= 5:
            read_bit = body[0]
            result += body[1:5]
            body = body[5:]
            if read_bit == '0':
                break
        return bits2int(result), body

    @staticmethod
    def read_args(body) -> Tuple[List['Packet'], str]:
        length_bit = body[0]
        if length_bit == '0':
            nbits = bits2int(body[2:16])
            body = body[16:]
            return Packet.read_n_bits(body, nbits)
        else:
            npackets = bits2int(body[2:12])
            body = body[12:]
            return Packet.read_n_packets(body, npackets)

    @staticmethod
    def read_n_bits(bits: str, nbits:int) -> Tuple[List['Packet'], str]:
        final_length = len(bits) - nbits
        result =[]
        while len(bits) > final_length:
            packet, bits = Packet.parse_packet(bits)
            result.append(packet)
        return result, bits

    @staticmethod
    def read_n_packets(bits: str, npackets:int) -> Tuple[List['Packet'], str]:
        result =[]
        for _ in range(npackets):
            packet, bits = Packet.parse_packet(bits)
            result.append(packet)
        return result, bits

    @staticmethod
    def parse_packet(bitstring: str) -> Tuple['Packet', str]:
        version = bits2int(bitstring[:3])
        op = OpCode(bits2int(bitstring[3:6]))
        body = bitstring[6:]

        if op is OpCode.VAL:
            value, rem = Packet.read_value(body)
            return ValuePacket(version, op, value), rem
        else:
            args, rem = Packet.read_args(body)
            return OpPacket(version, op, args), rem


class ValuePacket(Packet):
    def __init__(self, version: int, op: OpCode, value: int):
        super().__init__(version, op)
        self._value = value

    def value(self) -> int:
        return self._value

    def apply(self, fn: Callable) -> Any:
        return [fn(self)]

    def __str__(self):
        return f"{self._value}"


class OpPacket(Packet):
    def __init__(self, version: int, op: OpCode, arguments: List[Packet]):
        super().__init__(version, op)
        self._args = arguments

    def value(self) -> int:
        return self.op.operator()([a.value() for a in self._args])

    def __str__(self):
        return "(" + str(self.op) + " " + " ".join([str(a) for a in self._args]) + ")"

    def apply(self, fn: Callable) -> Any:
        return [fn(self)] + sum([a.apply(fn) for a in self._args], [])





if __name__ == '__main__':
    def _main():
        with open('../inputs/day16.txt', 'r') as f:
            inp = hex2bits(f.readline().strip())
        packet, _ = Packet.parse_packet(inp)

        print(f"Star 1: {sum(packet.apply(lambda p: p.version))}")
        print(f"Star 2: {packet.value()}")






    _main()
