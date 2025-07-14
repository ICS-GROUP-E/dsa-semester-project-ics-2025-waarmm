class Node:
    def __init__(self,patient_data):
        self.data=patient_data
        self.next=None


class AppointmentQueue:
    def __init__(self):
        self.front=self.rear=None

    def enqueue(self,patient_data):
        new_node=Node(patient_data)
        if self.rear is None:
            self.front=self.rear=new_node
        else:
            self.rear.next=new_node
            self.rear=new_node

    def dequeue(self):
        if self.front is None:
            return None
        removed=self.front.data
        self.front=self.front.next
        if self.front is None:
            self.rear=None
        return removed

    def viewQueue(self):
        appointments=[]
        current= self.front
        while current:
            appointments.append(current.data)
            current=current.next
        return appointments