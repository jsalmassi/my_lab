import unittest

def add(a, b):
    return a + b
print('we are in the  math_utils.py')

def sub(a, b):
    return a - b

class TestMathUtils(unittest.TestCase):
    def test_add(self):
        print('before assert in test_add')
        self.assertEqual(add(2, 3), 5)
        print('after assert in test_add')

    def test_sub(self):
        self.assertEqual(sub(5, 3), 2)

if __name__ == "__main__":
    unittest.main() 


