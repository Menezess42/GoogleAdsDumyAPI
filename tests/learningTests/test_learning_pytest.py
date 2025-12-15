# Tests for learning about pytest
import pytest


# Simple test of:
def func(x):
    return x + 1


# Pass
def test_answer_pass():
    assert func(3) == 4


# Failue
def test_answer_faild():
    assert func(3) == 5


# Assert that a certain exception is raised


def f():
    raise SystemExit(1)


def test_raised_exception():
    with pytest.raises(SystemExit):
        f()


# Grouping multiple tests in a class
class TestClass:
    def test_one(self):
        x = "this"
        assert "h" in x

    def test_two(self):
        x = "hello"
        assert hasattr(x, "check")


# Each test has a unique instance of the class. It is not good practice
# to share thing between tests
# The section bellow shows that
class TestClassDemoInstance:
    value = 0

    def test_one(self):
        self.value = 1
        assert self.value == 1

    def test_two(self):
        assert self.value == 1


# Compare floating-point values with pytest.approx
# It prevents small rounding erros from causing the test to fial
def test_sum():
    assert (0.1 + 0.2) == pytest.approx(0.3)
    # This works with scalars, lists, and NumPy arrays

# Request a unique temporary directory for functional tests
def test_needsfiles(tmp_path):
    print(tmp_path)
    assert 0
