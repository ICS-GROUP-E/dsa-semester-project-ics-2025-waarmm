import unittest
# Corrected import statement to get Patient and PriorityQueue from the ds.priorityQueue module
from ..ds.priorityQueue import Patient, PriorityQueue

class TestPriorityQueue(unittest.TestCase):

    def setUp(self):
        """Set up a new PriorityQueue before each test method."""
        self.pq = PriorityQueue()

    def test_insert_and_size(self):
        """Test that insert adds patients and size updates correctly."""
        self.assertTrue(self.pq.is_empty())
        self.assertEqual(self.pq.size(), 0)

        self.pq.insert("Alice", 3)
        self.assertEqual(self.pq.size(), 1)
        self.assertFalse(self.pq.is_empty())
        # The heap property means the root is the smallest, so we check the actual object
        # rather than assuming a specific name order if multiple items are present.
        # For a single item, it will be at index 0.
        self.assertEqual(self.pq.heap[0].name, "Alice")

        self.pq.insert("Bob", 1)
        self.assertEqual(self.pq.size(), 2)
        # With Bob (P1) inserted, Bob should be at the root (index 0)
        self.assertEqual(self.pq.heap[0].name, "Bob")
        # Alice should be the child
        self.assertEqual(self.pq.heap[1].name, "Alice")


    def test_remove_from_empty_queue(self):
        """Test removing from an empty queue returns None."""
        self.assertIsNone(self.pq.remove_highest_priority())
        self.assertTrue(self.pq.is_empty())

    def test_remove_single_patient(self):
        """Test removing the only patient in the queue."""
        self.pq.insert("Charlie", 2)
        patient = self.pq.remove_highest_priority()
        self.assertIsNotNone(patient)
        self.assertEqual(patient.name, "Charlie")
        self.assertEqual(patient.priority, 2)
        self.assertTrue(self.pq.is_empty())

    def test_remove_multiple_patients_priority_order(self):
        """Test removal maintains priority order (lower number is higher priority)."""
        self.pq.insert("Patient A", 5)
        self.pq.insert("Patient B", 1)
        self.pq.insert("Patient C", 3)
        self.pq.insert("Patient D", 2)

        # Expected order: B (1), D (2), C (3), A (5)
        p1 = self.pq.remove_highest_priority()
        self.assertEqual(p1.name, "Patient B")
        self.assertEqual(self.pq.size(), 3)

        p2 = self.pq.remove_highest_priority()
        self.assertEqual(p2.name, "Patient D")
        self.assertEqual(self.pq.size(), 2)

        p3 = self.pq.remove_highest_priority()
        self.assertEqual(p3.name, "Patient C")
        self.assertEqual(self.pq.size(), 1)

        p4 = self.pq.remove_highest_priority()
        self.assertEqual(p4.name, "Patient A")
        self.assertEqual(self.pq.size(), 0)
        self.assertTrue(self.pq.is_empty())

    def test_remove_multiple_patients_arrival_order_tie_breaking(self):
        """Test removal respects arrival order for tie-breaking priorities."""
        self.pq.insert("First A", 3) # arrival_order 0
        self.pq.insert("Second B", 1) # arrival_order 1
        self.pq.insert("Third C", 3) # arrival_order 2
        self.pq.insert("Fourth D", 1) # arrival_order 3
        self.pq.insert("Fifth E", 2) # arrival_order 4

        # Expected order based on priority then arrival:
        # Second B (P1, A1)
        # Fourth D (P1, A3)
        # Fifth E (P2, A4)
        # First A (P3, A0)
        # Third C (P3, A2)

        p1 = self.pq.remove_highest_priority()
        self.assertEqual(p1.name, "Second B")
        self.assertEqual(p1.priority, 1)
        self.assertEqual(p1.arrival_order, 1)

        p2 = self.pq.remove_highest_priority()
        self.assertEqual(p2.name, "Fourth D")
        self.assertEqual(p2.priority, 1)
        self.assertEqual(p2.arrival_order, 3)

        p3 = self.pq.remove_highest_priority()
        self.assertEqual(p3.name, "Fifth E")
        self.assertEqual(p3.priority, 2)
        self.assertEqual(p3.arrival_order, 4)

        p4 = self.pq.remove_highest_priority()
        self.assertEqual(p4.name, "First A")
        self.assertEqual(p4.priority, 3)
        self.assertEqual(p4.arrival_order, 0)

        p5 = self.pq.remove_highest_priority()
        self.assertEqual(p5.name, "Third C")
        self.assertEqual(p5.priority, 3)
        self.assertEqual(p5.arrival_order, 2)

        self.assertTrue(self.pq.is_empty())

    def test_list_patients(self):
        """Test the list_patients method returns correct string representations."""
        self.assertEqual(self.pq.list_patients(), [])

        self.pq.insert("Alice", 3)
        self.pq.insert("Bob", 1)
        self.pq.insert("Charlie", 2)

        # The order here is the internal heap order, not necessarily sorted by priority.
        # We just check if the correct string representations are present.
        self.assertIn("Bob (Priority 1)", self.pq.list_patients())
        self.assertIn("Alice (Priority 3)", self.pq.list_patients())
        self.assertIn("Charlie (Priority 2)", self.pq.list_patients())
        self.assertEqual(len(self.pq.list_patients()), 3)

        # After removing, the list should reflect the new heap state
        self.pq.remove_highest_priority() # Removes Bob
        self.assertNotIn("Bob (Priority 1)", self.pq.list_patients())
        self.assertEqual(len(self.pq.list_patients()), 2)


    def test_patient_comparison(self):
        """Test the __lt__ method of the Patient class directly."""
        p1 = Patient("P1", 2, 0)
        p2 = Patient("P2", 1, 1)
        p3 = Patient("P3", 2, 2) # Same priority as P1, but later arrival
        p4 = Patient("P4", 3, 3)

        self.assertTrue(p2 < p1) # P2 (P1) is higher priority than P1 (P2)
        self.assertFalse(p1 < p2)

        self.assertTrue(p1 < p3) # Same priority, P1 arrived earlier
        self.assertFalse(p3 < p1)

        self.assertTrue(p2 < p4) # P2 (P1) is higher priority than P4 (P3)

        self.assertFalse(p1 < p1) # A patient is not less than itself

# This allows you to run the tests directly from the command line
if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)

