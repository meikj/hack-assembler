#
# The Hack assembler parser module
#

class Parser():
    """
    Encapsulates access to the input code. Reads an assembly language command,
    parses it, and provides convienent access to the commands components.
    In addition, removes all white space and comments.

    Fields:
        file            = Name of ASM file
        commands        = List of all commands in file in form of (line, cmd)
        command_type    = The current command type (more details below)

        A_COMMAND for @Xxx where Xxx is either a symbol or decimal number
        C_COMMAND for dest=comp;jmp
        L_COMMAND (actually, pseudo-command) for (Xxx) where Xxx is a symbol

        symbol          = The symbol or decimal Xxx of the current command
                          @Xxx or (Xxx) (A_COMMAND or L_COMMAND only)
        dest            = The dest mnemonic in the current C-command (8
                          possibilities)
        comp            = The comp mnemonic in the current C-command (28
                          possibilities)
        jump            = The jump mnemonic in the current C-command (8
                          possibilities)
    """

    def __init__(self, file):
        """
        Opens the input file and gets ready to parse it.

        Raises an IOError upon file processing error.
        """
        self.commands = [] # command list
        self._c = 0 # current command
        self.file = file # name of file

        self.command_type = ''
        self.symbol = ''
        self.dest = ''
        self.comp = ''
        self.jump = ''

        if not self.file.endswith('.asm'):
            raise IOError('File is not of type ASM (.asm): %s' % self.file)

        with open(file, 'r') as f:
            for i, l in enumerate(f):
                l = l.strip().replace(' ', '').split('/')[0]
                if l:
                    self.commands.append((i+1, l)) # (line_no, command)

        if not self.commands:
            raise IOError('No commands present in file: %s' % file)

    def advance(self):
        """
        Reads and returns the next command from the input and makes it the
        current command.

        Returns a command type and command name pair.

        Raises an EOFError when end of command list is reached.
        Raises a SyntaxError when invalid syntax is encountered.
        """
        if self._c >= len(self.commands):
            raise EOFError('End of command list reached.')

        # Process command
        line_no = self.commands[self._c][0] # line number in file
        cmd = self.commands[self._c][1]

        # Reset fields
        self.command_type = ''
        self.symbol = ''
        self.dest = ''
        self.comp = ''
        self.jump = ''

        if cmd.startswith('@') and len(cmd) > 1:
            # @...
            self.command_type = 'A_COMMAND'
            self.symbol = cmd.split('@')[1]
        elif cmd.startswith('(') and cmd.endswith(')') and len(cmd) >= 3:
            # (...)
            self.command_type = 'L_COMMAND'
            self.symbol = cmd.split('(')[1].split(')')[0] # re perhaps?
        elif ('=' in cmd or ';' in cmd) and len(cmd) >= 3:
            # ...=...;...
            self.command_type = 'C_COMMAND'
            operands = cmd.replace('=', ' ').replace(';', ' ').split()

            if '=' in cmd and ';' in cmd:
                # dest=comp;jump
                self.dest = operands[0]
                self.comp = operands[1]
                self.jump = operands[2]
            elif '=' in cmd:
                # dest=comp
                self.dest = operands[0]
                self.comp = operands[1]
            elif ';' in cmd:
                # comp;jump
                self.comp = operands[0]
                self.jump = operands[1]
        else:
            raise SyntaxError('Invalid command on line %d (%s):\n\t=> %s' %
                (line_no, self.file, cmd))

        self._c += 1
        return (self.command_type, cmd)

    def reset(self):
        '''Reset the parser back to the beginning.'''
        self._c = 0
        self.command_type = ''
        self.symbol = ''
        self.dest = ''
        self.comp = ''
        self.jump = ''
