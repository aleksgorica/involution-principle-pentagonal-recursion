from collections.abc import Sequence
from typing import List

class Partition(Sequence):
    def __init__(self,parts: List[int] = []):
        self._parts = sorted(parts, reverse=True)
        super().__init__()
    def length(self):
        return len(self._parts)
    def __len__(self):
        return len(self._parts)
    def __getitem__(self, index):
        return self._parts[index]
    def copy(self):
        return Partition(self._parts[:])

    def __str__(self):
        return str(self._parts)
    def __repr__(self):
        return str(self._parts)
    def _check(self, parts: List[int]):
        if not all([x > 0 for x in parts]):
            raise ValueError("All parts must be positive")
    def size(self) -> int: 
        return sum(self._parts)
    def __eq__(self, other):
        return self._parts == other._parts
    def __hash__(self):
        return hash(tuple(self._parts))
    def append(self, value: int) -> None:
        self._parts.append(value)
        self._parts = sorted(self._parts, reverse=True)
    def pop(self) -> int:
        if len(self._parts) == 0:
            raise ValueError("Partition is empty")
        return self._parts.pop()
    def distinct(self) -> bool:
        return len(set(self._parts)) == len(self._parts)
    def smallest(self) -> int:
        return self._parts[-1]
    def largest(self) -> int:
        return self._parts[0] if len(self) > 0 else 0
    def bok(self) -> int:
        count = 1
        for i in range(1, len(self)):
            if self._parts[i] != self._parts[i-1] - 1:
                break
            count += 1
        return count
    def reduce_bok(self) -> None:
        for i in range(self.bok()):
            self._parts[i] -= 1

    def add_bok(self, bok_length: int) -> None:
        if bok_length > len(self):
            raise ValueError("Bok length is too long")
        for i in range(bok_length):
            self._parts[i] += 1

    """
    Modifies the partition according to the Franklin involution
    @return: boolean if the partition is a fixed point for Franklin involution. If True the partition is not changed
    """
    def franklin_involution(self) -> bool:
        if len(self) == 0: return True

        if self.bok() == len(self) and self.smallest() == self.bok():
            return True
        if self.bok() == len(self) and self.smallest() == self.bok() + 1:
            return True
        if self.smallest() <= self.bok():
            self.add_bok(self.pop())
        else:
            self.append(self.bok())
            self.reduce_bok()
        return False

    
    @staticmethod
    def pentagonal_partition(m: int, minus: bool) -> int:
        if minus:
            d = []
            for i in range(m):
                d.append(m + i)
            return Partition(d)
        else:
            d = []
            for i in range(m):
                d.append(m + 1 + i)
            return Partition(d)
        
    @staticmethod
    def partitions(n, I=1):
        yield (n,)
        for i in range(I, n//2 + 1):
            for p in Partition.partitions(n-i, i):
                yield (i,) + p
        
    


class PartitionPair:
    # partition 1 must be distinct
    # partition 2 can be arbitrary
    def __init__(self, partition1 : Partition, partition2 : Partition):
        if not partition1.distinct():
            raise ValueError("partition 1 must have all distinct parts")
        self.partition1 = partition1
        self.partition2 = partition2
    def __str__(self):
        return str(self.partition1) + " " + str(self.partition2)
    def __repr__(self):
        return str(self.partition1) + " " + str(self.partition2)
    def __eq__(self, other):
        return self.partition1 == other.partition1 and self.partition2 == other.partition2
    def copy(self):
        return PartitionPair(self.partition1.copy(), self.partition2.copy())
    def __hash__(self):
        return hash(tuple(self.partition1) + tuple(self.partition2))

    """
        It is fixed point only if both partitions are zero
        @return: boolean if the pair is a fixed point for Vahlen involution. If True the pair is not changed
    """
    def vahlen_involution(self) -> bool:
        if len(self.partition1) == 0 and len(self.partition2) == 0:
            return True
        if len(self.partition1) == 0:
            self.partition1.append(self.partition2.pop())
            return False
        if len(self.partition2) == 0:
            self.partition2.append(self.partition1.pop())
            return False
        if self.partition1[-1] <= self.partition2[-1]:
            self.partition2.append(self.partition1.pop())
        else:
            self.partition1.append(self.partition2.pop())
        return False
    
    """
        @return: boolean if the pair is a fixed point for Franklin involution. If True the pair is not changed
    """
    def franklin_involution(self) -> bool:
        return self.partition1.franklin_involution()
    
    def principle(self, printout=False) -> "PartitionPair":
        i, el = 0, None
        for i, el in enumerate(self.principle_generator()):
            if printout: print(i, el)
        return (i-1, el)

    
    def principle_generator(self, vahlen : bool = False) -> "PartitionPair":
        pair = self.copy()
        count = 0
        yield pair
        if not pair.franklin_involution():
            raise ValueError("You must provide fixed point partition")
        while True:
            pair = pair.copy()
            b = pair.vahlen_involution()
            if vahlen: yield pair.copy()
            b = pair.franklin_involution()
            yield pair
            if b: 
                break
            count += 1

if __name__ == '__main__':
    p = Partition([7,6,5])
    print(p)
    fixed = p.franklin_involution()
    print(f"Modified to: {p}" if not fixed else f"Fixed point: {p}")

    p = Partition([6,5,4])
    print(p)
    fixed = p.franklin_involution()
    print(f"Modified to: {p}" if not fixed else f"Fixed point: {p}")

