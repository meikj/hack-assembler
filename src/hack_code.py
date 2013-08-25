#
# The Hack assembler code module
#

comp = {
    '':     '0000000',
    '0':    '0101010',
    '1':    '0111111',
    '-1':   '0111010',
    'D':    '0001100',
    'A':    '0110000',
    '!D':   '0001101',
    '!A':   '0110001',
    '-D':   '0001111',
    '-A':   '0110011',
    'D+1':  '0011111',
    'A+1':  '0110111',
    'D-1':  '0001110',
    'A-1':  '0110010',
    'D+A':  '0000010',
    'D-A':  '0010011',
    'A-D':  '0000111',
    'D&A':  '0000000',
    'D|A':  '0010101',
    'M':    '1110000',
    '!M':   '1110001',
    '-M':   '1110011',
    'M+1':  '1110111',
    'M-1':  '1110010',
    'D+M':  '1000010',
    'D-M':  '1010011',
    'M-D':  '1000111',
    'D&M':  '1000000',
    'D|M':  '1010101'
}

dest = {
    '':     '000',
    'null': '000',
    'M':    '001',
    'D':    '010',
    'MD':   '011',
    'A':    '100',
    'AM':   '101',
    'AD':   '110',
    'AMD':  '111'
}

jump = {
    '':     '000',
    'null': '000',
    'JGT':  '001',
    'JEQ':  '010',
    'JGE':  '011',
    'JLT':  '100',
    'JNE':  '101',
    'JLE':  '110',
    'JMP':  '111'
}

def address(dec):
    '''
    Convert a decimal (or decimal string) into a 15-bit Hack compatible memory
    address. The Hack address space is 2^15 (32K).
    '''
    dec = int(dec)
    if dec < 0 or dec >= 32768:
        raise ValueError('Invalid address: out of range.')

    addr = ''
    i = 15 # expand bit string 15 bits

    while i > 0:
        b = str(dec % 2)
        addr = b + addr
        dec = dec // 2
        i -= 1

    return addr

def a_instruction(addr):
    '''Return the A-instruction of the specified address'''
    if isinstance(addr, str) and len(addr) == 15 and addr.isdigit():
        return '0' + addr
    else:
        return '0' + address(addr)

def c_instruction(d, c, j):
    '''Return the C-instruction containing the specified dest, comp and jump'''
    return '111' + comp[c] + dest[d] + jump[j]
