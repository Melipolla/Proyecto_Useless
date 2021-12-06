class LinkedStack:
    # Crear nodo
    class _Node:
        __slot__ = '_element', '_next'

        def __init__(self, element, next):
            self._element = element
            self._next = next

    # Establecer la parte superior de la pila
    def __init__(self):
        self._head = None
        self._size = 0

    # Pila de elementos
    def push(self, e):
        self._head = self._Node(e, self._head)
        self._size += 1


ls = LinkedStack()

ls.push(1)
ls.push(2)
