# priority_queue.py

class Patient:
    def __init__(self, name, priority, arrival_order):
        self.name = name
        self.priority = priority
        self.arrival_order = arrival_order

    def __lt__(self, other):
        if self.priority == other.priority:
            return self.arrival_order < other.arrival_order
        return self.priority < other.priority

    def __str__(self):
        return f"{self.name} (Priority {self.priority})"

# priority class to handle the heap
class PriorityQueue:
    def __init__(self):
        self.heap = []
        self.counter = 0  # will be used to track the arrival order

    def insert(self, name, priority):
        patient = Patient(name, priority, self.counter)
        self.counter += 1
        self.heap.append(patient)
        self._heapify_up(len(self.heap) - 1)  # fix the heap from the new position

    def remove_highest_priority(self):
        if not self.heap:
            return None
        self._swap(0, len(self.heap) - 1)  # swap root with the last item
        highest = self.heap.pop()
        self._heapify_down(0)  # fix the heap from the root down
        return highest

    def is_empty(self):
        return len(self.heap) == 0

    def size(self):
        return len(self.heap)

    def list_patients(self):
        return [str(p) for p in self.heap]

    def _heapify_up(self, index):
        parent = (index - 1) // 2
        if index > 0 and self.heap[index] < self.heap[parent]:
            self._swap(index, parent)
            self._heapify_up(parent)  # recursive

    def _heapify_down(self, index):
        smallest = index
        left = 2 * index + 1
        right = 2 * index + 2

        if left < len(self.heap) and self.heap[left] < self.heap[smallest]:
            smallest = left
        if right < len(self.heap) and self.heap[right] < self.heap[smallest]:
            smallest = right

        if smallest != index:
            self._swap(index, smallest)
            self._heapify_down(smallest)

    def _swap(self, i, j):
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]
