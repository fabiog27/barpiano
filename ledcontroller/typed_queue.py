from typing import TypeVar, Generic

T = TypeVar('T')


class TypedQueue(Generic[T]):
    def get(self, block=True, timeout=None) -> T:
        ...

    def put(self, item: T, block=True, timeout=None) -> None:
        ...

    def empty(self):
        ...
