# Infix to Postfix and vice versa converter using build-in Python stack.

import operator
from collections import deque

from pprint import pprint

ops = {
    '+': operator.add,
    '-': operator.sub,
    '*': operator.mul,
    '/': operator.truediv,
    '%': operator.mod,
    '^': operator.xor
}


def infix_to_postfix(string):
    stack = deque()
    return str(stack)


def postfix_to_infix(string):
    stack, string = deque(), string.replace(' ', '')
    for s in string:
        if s in ops:
            op2, op1 = stack.pop(), stack.pop()
            stack.append(f"({op1} {s} {op2})")
            # stack.append(ops[s](op1, op2))
        else:
            stack.append(s)  # float(s)
    return stack.pop()


def main():
    infix_strings = (
        "(А-B-С)/D-E*F",
        "(A+B)*C-(D+E)/F",
        "A/(B-C)+D*(E-F)",
        "(A*B+C)/D-F/E"
    )

    postfix_strings = list(map(infix_to_postfix, infix_strings))
    postfix_strings = ["AB - C * DEF + / +"]
    new_infix_strings = list(map(postfix_to_infix, postfix_strings))

    pprint(infix_strings)
    pprint(postfix_strings)
    pprint(new_infix_strings)


if __name__ == "__main__":
    main()
