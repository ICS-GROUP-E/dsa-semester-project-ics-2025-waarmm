import pytest
from src.ds.undo_redo_stack import Stack

def test_push_and_pop():
    s = Stack()
    s.push("A")
    s.push("B")
    assert s.pop() == "B"
    assert s.pop() == "A"

def test_peek():
    s = Stack()
    s.push("X")
    assert s.peek() == "X"
    s.push("Y")
    assert s.peek() == "Y"

def test_is_empty():
    s = Stack()
    assert s.is_empty()
    s.push(1)
    assert not s.is_empty()

def test_clear():
    s = Stack()
    s.push(1)
    s.push(2)
    s.clear()
    assert s.is_empty()

def test_size():
    s = Stack()
    assert s.size() == 0
    s.push(10)
    s.push(20)
    assert s.size() == 2
