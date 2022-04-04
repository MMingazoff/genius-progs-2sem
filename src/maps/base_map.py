from abc import ABC, abstractmethod
from typing import Iterable, Tuple


class BaseMap(ABC):
    @abstractmethod
    def __getitem__(self, key: Tuple[int, str]) -> Tuple[int, str]: ...

    @abstractmethod
    def __setitem__(self, key: Tuple[int, str], value: Tuple[int, str]) -> None: ...

    @abstractmethod
    def __delitem__(self, key: Tuple[int, str]) -> None: ...

    @abstractmethod
    def __len__(self) -> int: ...

    @abstractmethod
    def __iter__(self) -> Iterable[Tuple[str, int]]: ...

    def write(self, path: str, mode='a') -> None:
        with open(path, mode, encoding='utf8') as file:
            for node in self:
                key, value = node.key, node.value
                file.write(f'{key}, {value}\n')

    @classmethod
    def read(cls, path: str) -> 'BaseMap':
        my_obj = cls()
        with open(path, 'r', encoding='utf8') as file:
            line = file.readline()
            while line != '':
                key, value = line.split()
                my_obj[key] = value
                line = file.readline()
        return my_obj


if __name__ == '__main__':
    pass
