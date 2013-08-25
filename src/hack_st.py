#
# The Hack assembler symbol table module
#

class SymbolTable():

    def __init__(self):
        self.table = dict()
        self.ram_addr = 15

    def add(self, symbol, address):
        if not isinstance(symbol, str) or not isinstance(address, str):
            raise TypeError('Both symbol and address must be strings')
        elif symbol.isdigit() or len(address) < 15:
            raise ValueError('Symbol must be text and address must be 15-bits')

        self.table[symbol] = address

    def addvar(self, symbol):
        self.ram_addr += 1
        self.table[symbol] = self.ram_addr
        return self.ram_addr

    def contains(self, symbol):
        return self.table.has_key(symbol)

    def address(self, symbol):
        return self.table[symbol]
