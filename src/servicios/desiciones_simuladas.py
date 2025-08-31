from collections import deque

class ProveedorScripted:
    def __init__(self, decisiones):
        self._q = deque(decisiones)

    def decidir(self, _estado):
        return self._q.popleft()