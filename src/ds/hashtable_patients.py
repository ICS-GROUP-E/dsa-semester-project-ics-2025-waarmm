class Patient:
    def __init__(self, id, name, age, condition):
        self.id = id
        self.name = name
        self.age = age
        self.condition = condition

    def __str__(self):
        return f"{self.id} - {self.name}"
    
    def __repr__(self):
        return self.__str__()
    

class HashTable:
    def __init__(self, size=10):
        self.size = size
        self.table = [[] for _ in range(size)]

    def _hash(self, key):
        return hash(key) % self.size
    

    def addPatient(self, patient):
        index = self._hash(patient.id)

        # Check for duplicates
        for existing in self.table[index]:
            if existing.id == patient.id:
                return False 
            
        self.table[index].append(patient)
        return True
    
    def getPatient(self, patient_id):
        index = self._hash(patient_id)
        for i, p in enumerate(self.table[index]):
            if p.id == patient_id:
                return p
            
        return None
    
    def removePatient(self, patient_id):
        index = self._hash(patient_id)

        for i, p in enumerate(self.table[index]):
            if p.id == patient_id:
                del self.table[index][i]
                return True
            
        return False
    
    def getPatients(self):
        all_patients = []
        for bucket in self.table:
            all_patients.extend(bucket)
        return all_patients
