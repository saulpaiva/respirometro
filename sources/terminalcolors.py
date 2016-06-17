class TerminalColors:
    '''
        Reference http://ascii-table.com/ansi-escape-sequences.php
    '''
    class ATTRIBUTES:
        NORMAL      = ''
        BOLD        = ';1'
        UNDERSCORE  = ';4'
        BLINK       = ';5'
        REVERSE     = ';6'
        CONCEALED   = ';7'

    class FOREGROUND:
        NORMAL  = ''
        BLACK   = ';30'
        RED     = ';31'
        GREEN   = ';32'
        YELLOW  = ';33'
        BLUE    = ';34'
        MAGENTA = ';35'
        CYAN    = ';36'
        WHITE   = ';37'

    class BACKGROUND:
        NORMAL  = '' 
        BLACK   = ';40'
        RED     = ';41'
        GREEN   = ';42'
        YELLOW  = ';43'
        BLUE    = ';44'
        MAGENTA = ';45'
        CYAN    = ';46'
        WHITE   = ';47'

    @classmethod
    def cstring(cls, string, attr = 'NORMAL', fore = 'NORMAL', back = 'NORMAL'):
        attr = getattr(cls.ATTRIBUTES, attr.upper(), '')
        fore = getattr(cls.FOREGROUND, fore.upper(), '')
        back = getattr(cls.BACKGROUND, back.upper(), '')
        format_str = attr + fore + back
        if(format_str != ''):
            format_str = format_str[1:]
        return '\033[{}m{}\033[0m'.format(format_str, string)

    @classmethod
    def cprint(cls, string, attr = 'NORMAL', fore = 'NORMAL', back = 'NORMAL', 
            sep = ' ', end = '\n', flush = False):
            
        print(cls.cstring(string, attr, fore, back), end = end, sep = sep, flush = flush)
    
def colorprint(*args, **kwargs):
    TerminalColors.cprint(*args, **kwargs)
def colorstring(*args, **kwargs):
    return TerminalColors.cstring(*args, **kwargs)

if __name__ == '__main__':
    cprint('TEST', fore='green', back = 'blue')
    print(cstring('TESTE', fore='blue', back='green'))    
