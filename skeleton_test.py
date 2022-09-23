import unittest

import skeleton_test
from dynamic_scope import get_dynamic_re


def test_late_local():
    def outer():
        a = "outer_a"

        def inner():
            dre = get_dynamic_re()
            a = "inner_a"
            return dre
        return inner()
    return outer()


def test():
    a = "test_a"
    b = "test_b"
    return get_dynamic_re()


if __name__ == "__main__":

    dre = test_late_local()
    #print(f"{dre['a']=}")

    suite = unittest.findTestCases(skeleton_test)
    result = unittest.TestResult()
    suite.run(result, debug=True)
    print(f"{result=}")
