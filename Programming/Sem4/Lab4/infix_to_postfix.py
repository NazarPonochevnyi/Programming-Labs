# Infix to Postfix and vice versa converter using build-in Python stack.

import operator
from collections import deque

from pprint import pprint

ops = {
    '+': operator.add,
    '-': operator.sub,
    '*': operator.mul,
    '/': operator.truediv,
    '^': operator.xor
}
precedence = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3}


def infix_to_postfix(string):
    stack, output, string = deque(), '', string.replace(' ', '')
    for s in string:
        if s in ops:
            while stack and stack[-1] in ops \
                    and precedence[s] <= precedence[stack[-1]]:
                output += stack.pop()
            stack.append(s)
        elif s == '(':
            stack.append(s)
        elif s == ')':
            while stack and stack[-1] != '(':
                output += stack.pop()
            stack.pop()
        else:
            output += s
    while stack:
        output += stack.pop()
    return output


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
    print("Input infix strings:")
    pprint(infix_strings)

    postfix_strings = list(map(infix_to_postfix, infix_strings))
    print("\nConverted postfix strings:")
    pprint(postfix_strings)

    new_infix_strings = list(map(postfix_to_infix, postfix_strings))
    print("\nConverted infix strings to compare with input strings:")
    pprint(new_infix_strings)


if __name__ == "__main__":
    main()
