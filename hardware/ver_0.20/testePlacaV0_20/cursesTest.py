# http://ascii-table.com/ansi-escape-sequences.php

def printAt(x, y, Str):
    '''
        Using ANSI escape sequence, 
        where ESC[y;xH moves curser to row y, col x:
    '''
    print("\033[{};{}H{}".format(x, y, Str))

def progressBar(percent, lenght):
    '''
        Cursor necessita estar na linha onde esta a barra de progresso.
        DOC dos ANSII caracters:
            http://ascii-table.com/ansi-escape-sequences.php
    '''
    highlight = " "*int((lenght-2)*percent/100)
    notHighlight = " "*(lenght-2- len(highlight))
    print("\033[{}D\t|\033[1;42m{}\033[0;0m{}|  {}%".format(lenght+5, highlight,notHighlight, percent), end="")

if __name__ == '__main__':
    #printAt(0, 0,"Hello Word")
    start = "\033[1;31m"
    end = "\033[0;0m"
    progressBar(50, 25)
    # print("\033[10B\033[10DFile is: " + start + "<placeholder>" + end)

