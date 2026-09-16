import unittest


class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.assertEqual(True, False)  # add assertion here


if __name__ == '__main__':
    qq=MyTestCase
    # unittest.main()
    qq.test_something(1)
