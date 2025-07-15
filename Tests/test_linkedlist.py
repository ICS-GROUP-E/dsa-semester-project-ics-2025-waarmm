from src.ds.LinkedList_medication import MedicationHistory

def test_add_medication():
    med = MedicationHistory()
    med.add_medication("P001", "Paracetamol", "500mg", "2025-07-10")
    history = med.show_medication_history("P001")
    assert any("Paracetamol" in h for h in [x[1] for x in history])
