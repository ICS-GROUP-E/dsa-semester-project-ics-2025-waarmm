import sys
import os
import pytest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'ds')))

from hashtable_patients import HashTable, Patient

@pytest.fixture
def hashtable():
    ht = HashTable()
    return ht

def test_add_patient_success(hashtable):
    patient = Patient("1", "Alice", 30, "Flu")
    is_added = hashtable.addPatient(patient)
    assert is_added == True
    assert hashtable.getPatient("1") == patient


def test_add_duplicate_patient(hashtable):
    patient = Patient("2", "Bob", 25, "Diabetes")
    hashtable.addPatient(patient)
    duplicate = Patient("2", "Bobby", 30, "Cold")
    is_added = hashtable.addPatient(duplicate)
    assert is_added is False
    assert hashtable.getPatient("2").name == "Bob"


def test_get_patient_not_found(hashtable):
    patient = hashtable.getPatient("999")
    assert patient is None


def test_remove_patient_success(hashtable):
    patient = Patient("3", "Charlie", 35, "Hypertension")
    hashtable.addPatient(patient)
    is_removed = hashtable.removePatient("3")
    assert is_removed is True
    assert hashtable.getPatient("3") is None


def test_remove_patient_not_found(hashtable):
    is_removed = hashtable.removePatient("999")
    assert is_removed is False


def test_get_all_patients(hashtable):
    patient1 = Patient("4", "David", 40, "Asthma")
    patient2 = Patient("5", "Eve", 45, "Cancer")
    hashtable.addPatient(patient1)
    hashtable.addPatient(patient2)
    
    all_patients = hashtable.getPatients()
    assert len(all_patients) == 2
    patient_ids = [patient.id for patient in all_patients]
    assert "4" in patient_ids and "5" in patient_ids