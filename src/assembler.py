#!/usr/bin/env python

#
# The Hack assembler
#

import sys
import argparse

import hack_code
from hack_parser import Parser
from hack_st import SymbolTable

def main(f):
    '''Run the assembler on the specified file "f" and output to stdin.'''
    p = Parser(f)
    st = SymbolTable()

    # Initialise symbol table with predefined symbols
    st.add('SP', hack_code.address(0))
    st.add('LCL', hack_code.address(1))
    st.add('ARG', hack_code.address(2))
    st.add('THIS', hack_code.address(3))
    st.add('THAT', hack_code.address(4))
    st.add('R0', hack_code.address(0))
    st.add('R1', hack_code.address(1))
    st.add('R2', hack_code.address(2))
    st.add('R3', hack_code.address(3))
    st.add('R4', hack_code.address(4))
    st.add('R5', hack_code.address(5))
    st.add('R6', hack_code.address(6))
    st.add('R7', hack_code.address(7))
    st.add('R8', hack_code.address(8))
    st.add('R9', hack_code.address(9))
    st.add('R10', hack_code.address(10))
    st.add('R11', hack_code.address(11))
    st.add('R12', hack_code.address(12))
    st.add('R13', hack_code.address(13))
    st.add('R14', hack_code.address(14))
    st.add('R15', hack_code.address(15))
    st.add('SCREEN', hack_code.address(16384))
    st.add('KBD', hack_code.address(24576))

    # First pass (populate symbol table with L_COMMAND's)
    rom_addr = 0
    while True:
        try:
            (t, c) = p.advance()

            if t is 'A_COMMAND' or t is 'C_COMMAND':
                rom_addr += 1
            else:
                st.add(p.symbol, hack_code.address(rom_addr))
        except SyntaxError as err:
            sys.stderr.write('FATAL: ' + str(err) + '\n')
            sys.stderr.flush()
            return
        except EOFError:
            # finished first pass
            break

    # Second pass (final translation)
    p.reset()
    while True:
        try:
            (t, c) = p.advance()

            if t is 'A_COMMAND':
                if p.symbol.isdigit():
                    # Referencing direct address
                    print(hack_code.a_instruction(p.symbol))
                else:
                    # Referencing label or variable
                    try:
                        print(hack_code.a_instruction(st.address(p.symbol)))
                    except KeyError:
                        # Must be referencing a new variable
                        print(hack_code.a_instruction(st.addvar(p.symbol)))
            elif t is 'L_COMMAND':
                continue
            else:
                print(hack_code.c_instruction(p.dest, p.comp, p.jump))
        except EOFError:
            # finished second pass
            break

if __name__ == '__main__':
    p = argparse.ArgumentParser(
        description='The Hack computer platform assembler.'
    )
    p.add_argument('input', help='the ASM input file')
    args = p.parse_args()

    try:
        main(args.input)
    except IOError as err:
        sys.stderr.write('FATAL: ' + str(err) + '\n')
        sys.stderr.flush()
