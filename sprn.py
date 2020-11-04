from collections import deque
from random import randrange

# Initialise global stack
main_stack = deque(maxlen=23)
legal_operators = ['+', '-', '*', '/', '%', '^']
comment_flag = False
random_ints = [1804289383,
               846930886,
               1681692777,
               1714636915,
               1957747793,
               424238335,
               719885386,
               1649760492,
               596516649,
               1189641421,
               1025202362,
               1350490027,
               783368690,
               1102520059,
               2044897763,
               1967513926,
               1365180540,
               1540383426,
               304089172,
               1303455736,
               35005211,
               521595368,
               1804289383]
random_int_counter = 0


def overflow_check(value):
    """
        This function provides a standin to check whether the value is within
        the int limits in the original sprn
    """
    if value > 2147483647:
        value = 2147483647
    elif value < -2147483648:
        value = -2147483648
    return value


def push_to_stack(val):
    """
        Checks if the stack is less than the max stack length, and if so
        pushes the value to the stack after checking for overflows.
    """
    if len(main_stack) < main_stack.maxlen:
        main_stack.append(overflow_check(val))
    else:
        print("Stack overflow.")


def exceptional_parse(input_to_parse):
    """
        Define an exceptional parse function for items that aren't covered
        by the typical parse where input is split by whitespace. This parses
        input character by character to build up a split expression that
        will be parsed.

        When input is not space separated, The parse order of the version to
        emulate runs:
        1) If it's a number, push it to the stack
        2) If it's a mathematical operator, perform them in reverse input order
        3) If it's a legal special operator perform it
        4) If it's anything else print the error message.
    """
    global legal_operators
    # Initialise temporary holders for numbers, and operators.
    temp_nums = []
    temp_ops = []
    temp_exp = []
    temp_number = ""
    negative_flag = False

    elements = list(input_to_parse)

    # This sets the negative flag if the first number is negative.
    if elements[0] == "-" and elements[1].isdigit():
        negative_flag = True

    # Iterate through characters in the input
    for j in list(input_to_parse):
        # If the character is a digit, concatenate with temporary number
        if j.isdigit():
            temp_number += j
        else:
            # End of the number has been reached, so append to numbers.
            # If there are two numbers in the temp_nums, fill out the temp
            # expression so far with numbers followed by operators in reverse
            # order.
            if temp_number != "":
                if negative_flag:
                    temp_nums.append("-" + temp_number)
                    temp_number = ""
                    temp_ops = []
                    negative_flag = False
                else:
                    temp_nums.append(temp_number)
                    temp_number = ""

                if len(temp_nums) == 2:
                    temp_exp += temp_nums
                    temp_exp += temp_ops[::-1]
                    temp_nums = []
                    temp_ops = []

            # If character is in the legal operators, add to the temporary operstors
            if j in legal_operators:
                temp_ops.append(j)
            elif j == "=":
                temp_exp += temp_nums
                temp_exp.append(j)
                temp_exp += temp_ops[::-1]
                temp_nums = []
                temp_ops = []
            elif j == "#":
                print("Unrecognised operator or operand \"" + j + "\".")
            elif j != " ":
                temp_exp += temp_nums
                temp_exp += temp_ops[::-1]
                temp_exp.append(j)
                temp_nums = []
                temp_ops = []

    if temp_number != "":
        temp_nums.append(temp_number)

    temp_exp += temp_nums + temp_ops[::-1]
    return temp_exp


def parse(element):
    """
        This function iterates through the operands in each statement and
        performs the functions accordingly.
    """
    global legal_operators
    global random_ints
    global random_int_counter
    global comment_flag

    # Check if number is octal, if so, convert from octal to int and continue
    '''
        This check is slightly ugly so it requires explanation. First
        the code checks if this element is flagged as an octal. Numbers are
        flagged as octal by the prefix '0'. If a number is prefixed '0' it is
        parsed as an octal. In order to do that the element is split into a
        list, checks if that list has more than two elements, then checks if
        the first element is a 0, or if the first two elements are -0, if so
        it tries to convert the element from a string to an octal.

        The difficulty is bad octals e.g., 09, are ignored by the sprn. So
        to mimic that behaviour, if an exception is thrown by the octal, but
        it could be parsed as a regular int the parse function exits with a 1
        error.

    '''
    # If comment symbol received switch comment flag and skip input until
    # the next comment symbol is received. Stop processing for '#' element.
    if element == '#':
        comment_flag = not comment_flag
        return
    if comment_flag:
        return

    octal_check = list(element)
    if len(octal_check) > 1:
        octal_bools = [
            (octal_check[0] == '0'),
            (octal_check[0] == '-' and octal_check[1] == '0')]

        if octal_bools[0] or octal_bools[1]:
            try:
                element = int(element, 8)
            except:
                try:
                    int(element)
                    return 1
                except:
                    pass

    # If value is an integer push to the stack, otherwise pass
    try:
        assert octal_check[0] != '+'
        val: int = int(element)
        push_to_stack(val)
        return 0
    except:
        pass

    # If value is in the legal operators check if there are sufficient
    # values on the stack then pop those and apply operand function
    if element in legal_operators:
        # Replace '^' with '**'. This is so powers are parsed properly
        # additionally ensure that the top of the stack is positive to show
        # an error if a negative power is called.
        if '^' in element:
            element = element.replace("^", "**")
            try:
                assert main_stack[-1] >= 1
            except:
                print("Negative power.")
                return 0
        if len(main_stack) > 1:
            val1 = main_stack.pop()
            val2 = main_stack.pop()
            operands(val1, val2, element)
        else:
            print("Stack underflow.")
        return 0

    # Parse '=' to print the last number from the stack without removing it.
    elif element == '=':
        try:
            print(main_stack[-1])
        except:
            print("Stack empty.")
        return 0

    # Parse 'd' to print the stack in order.
    elif element == 'd':
        if len(main_stack) == 0:
            print(-2147483648)
            return 0
        for element in main_stack:
            print(element)
        return 0

    # Parse 'r' to push random number on stack. For the first 23 calls
    # this will print the 23 randoms that are always produced by the SPRN to
    # emulate. After that a random int between 1 and 2147483647 is returned.
    elif element == 'r':
        if random_int_counter < 23:
            r = random_ints[random_int_counter]
            random_int_counter += 1
        else:
            r = randrange(2147483647)
        push_to_stack(r)
        return 0

    # If it's an illegal character print the char in question.
    elif len(element) == 1:
        print("Unrecognised operator or operand \"" + element + "\".")
        return 0

    # If none of the above could parse the element, return an error flag.
    else:
        return 1


def operands(val1, val2, operator):
    """
        This function takes two values popped from the stack, and seeks to
        perform the function indicated by the operator on them. It then pushes
        the result of that operation back onto the stack.
    """
    # Exceptional case for power operator to call pow function.
    expression = str(val2) + operator + str(val1)
    try:
        result = int(eval(expression))
        push_to_stack(result)
    except ZeroDivisionError:
        print("Divide by 0.")
        main_stack.append(val2)
        main_stack.append(val1)


def main():
    """
        The main function starts the calculator then while it is running
        accepts input. The input is split by whitespaces, the parser then
        attempts to parse each element. If the parser can parse that element
        it will return 0.

        If it gets to the end and the parser cannot parse the element it is
        likely that there is no whitespace and it is a complicated expression.
        That element is then passed to the exceptional parser which returns an
        array of elements split based on conditions that mimic the behaviour of
        the srpn.
    """
    print("You can now start interacting with the SRPN calculator")
    while True:

        input_to_parse = input()
        split_input = input_to_parse.split()
        for element in split_input:

            # Call the parse statement on the element and get the return value.
            # If the return value is 1 it means the expression needs to be
            # split by the exceptional parser, before being run through parse
            # again.
            result = parse(element)

            if result == 1:
                secondary_input = exceptional_parse(element)
                for item in secondary_input:
                    parse(item)


def test_main(calculation):
    """
    Function that imitates the main function on a test calculation input.
    """
    # Reset global variables that change so testing is consistent
    global random_int_counter
    main_stack.clear()
    random_int_counter = 0

    # Replicate main function code
    split_input = calculation.split()
    for element in split_input:

        # Call the parse statement on the element and get the return value.
        # If the return value is 1 it means the expression needs to be
        # split by the exceptional parser, before being run through parse
        # again.
        result = parse(element)

        if result == 1:
            secondary_input = exceptional_parse(element)
            for item in secondary_input:
                parse(item)
    return main_stack


# Finally call the main function to run the program and start the calculator
if __name__ == "__main__":
    main()
