from ds.queue_appointments import AppointmentQueue

queue=AppointmentQueue()

queue.enqueue("Mark Tavin")
queue.enqueue("David Peter")
queue.enqueue("Aisha Mohammed")

print("Current queue:",queue.viewQueue())

served = queue.dequeue()
print("Served:",served)

print("Updated queue:",queue.viewQueue())