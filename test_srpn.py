import srpn

from io import StringIO
import sys

"""
Code snippet to capture standard output for validation testing taken from
https://stackoverflow.com/questions/16571150/how-to-capture-stdout-output-from-a-python-function-call
"""


class Capturing(list):
    def __enter__(self):
        self._stdout = sys.stdout
        sys.stdout = self._stringio = StringIO()
        return self

    def __exit__(self, *args):
        self.extend(self._stringio.getvalue().splitlines())
        del self._stringio  # free up some memory
        sys.stdout = self._stdout


def test_1():
    x = """
        10
        2
        +
        =
        """
    result = srpn.test_main(x)
    assert result[0] == 12


def test_2():
    x = """
        11
        3
        -
        =
        """
    result = srpn.test_main(x)
    assert result[0] == 8


def test_3():
    x = """
        9
        4
        *
        =
        """
    result = srpn.test_main(x)
    assert result[0] == 36


def test_4():
    x = """
        11
        3
        /
        =
        """
    result = srpn.test_main(x)
    assert result[0] == 3


def test_5():
    x = """
        11
        3
        %
        =
        """
    result = srpn.test_main(x)
    assert result[0] == 2


# -- Page two

def test_6():
    x = """
        3
        3
        *
        4
        4
        *
        +
        =
        """
    result = srpn.test_main(x)
    assert result[0] == 25


def test_7():
    x = """
        1234
        2345
        3456
        d
        +
        d
        +
        d
        =
        """
    result = srpn.test_main(x)
    assert result[0] == 7035


# -- Page three

def test_8():
    x = """
        2147483647
        1
        +
        =
        """
    result = srpn.test_main(x)
    assert result[0] == 2147483647


def test_9():
    x = """
        -2147483647
        1
        -
        =
        20
        -
        =
        """
    result = srpn.test_main(x)
    assert result[0] == -2147483648


def test_10():
    x = """
        100000
        0
        -
        d
        *
        =
        """
    with Capturing() as output:
        result = srpn.test_main(x)
    assert result[0] == 100000
    assert output == ["100000", "Stack underflow.", "100000"]


# -- Page four

def test_11():
    x = """
        1
        +
        """
    with Capturing() as output:
        result = srpn.test_main(x)
    assert result[0] == 1
    assert output == ["Stack underflow."]


def test_12():
    x = """
        10
        5
        -5
        +
        /
        """
    with Capturing() as output:
        result = srpn.test_main(x)
    assert result[-1] == 0
    assert output == ["Divide by 0."]


def test_13():
    x = """
        11+1+1+d
        """
    with Capturing() as output:
        result = srpn.test_main(x)
    assert result[-1] == 13
    assert output == ["Stack underflow.", "13"]


def test_14():
    x = """
        # This is a comment #
        1 2 + # And so is this #
        d
        """
    with Capturing() as output:
        result = srpn.test_main(x)
    assert result[-1] == 3
    assert output == ["3"]


def test_15():
    x = """
        3 3 ^ 3 ^ 3 ^=
        """
    with Capturing() as output:
        result = srpn.test_main(x)
    assert result[-1] == 2147483647
    assert output == ["3"]


def test_16():
    x = "rrrrrrrrrrrrrrrrrrrrrrdrrrd"
    y = ["1804289383",
         "846930886",
         "1681692777",
         "1714636915",
         "1957747793",
         "424238335",
         "719885386",
         "1649760492",
         "596516649",
         "1189641421",
         "1025202362",
         "1350490027",
         "783368690",
         "1102520059",
         "2044897763",
         "1967513926",
         "1365180540",
         "1540383426",
         "304089172",
         "1303455736",
         "35005211",
         "521595368",
         "Stack overflow.",
         "Stack overflow.",
         "1804289383",
         "846930886",
         "1681692777",
         "1714636915",
         "1957747793",
         "424238335",
         "719885386",
         "1649760492",
         "596516649",
         "1189641421",
         "1025202362",
         "1350490027",
         "783368690",
         "1102520059",
         "2044897763",
         "1967513926",
         "1365180540",
         "1540383426",
         "304089172",
         "1303455736",
         "35005211",
         "521595368",
         "1804289383"]
    with Capturing() as output:
        result = srpn.test_main(x)
    assert output == y


# -- My own tests
def test_17():
    x = """
        3dr-=d
        """
    y = ["3",
         "1804289383",
         "-1804289380"]
    with Capturing() as output:
        result = srpn.test_main(x)
    assert output == y


def test_18():
    x = "2#"
    with Capturing() as output:
        result = srpn.test_main(x)
    assert output == ["Unrecognised operator or operand \"#\"."]
    assert result[0] == 2


def test_19():
    x = "0105-345"
    with Capturing() as output:
        result = srpn.test_main(x)
    assert output == []
    assert result[-1] == -276


def test_20():
    x = """
        0109
        =
        """
    with Capturing() as output:
        result = srpn.test_main(x)
    assert output == ["Stack empty."]


def test_21():
    x = "84567*31-=+"
    y = ["2621577",
         "Stack underflow.",
         "Stack underflow."]
    with Capturing() as output:
        result = srpn.test_main(x)
    assert output == y
    assert result[-1] == 2621577


def test_22():
    x = "-0162-561"
    y = []
    with Capturing() as output:
        result = srpn.test_main(x)
    assert output == y
    assert result[-1] == -675


def test_23():
    x = "-14+0^45%"
    y = ["Stack underflow."]
    with Capturing() as output:
        result = srpn.test_main(x)
    assert output == y
    assert result[-1] == -14


def test_24():
    x = "9----4+123"
    y = ["Stack underflow.", "Stack underflow."]
    with Capturing() as output:
        result = srpn.test_main(x)
    assert output == y
    assert result[-1] == -110


def test_25():
    x = "-14+0^"
    y = ["Stack underflow."]
    with Capturing() as output:
        result = srpn.test_main(x)
    assert output == y
    assert result[-1] == 1

def test_26():
    x = "2+2^2*5"
    y = []
    with Capturing() as output:
        result = srpn.test_main(x)
    assert output == y
    assert result[-1] == 30
