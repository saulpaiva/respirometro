from terminalcolors import cstring, cprint
import types

class ProgBarTerm():
    default_color = 'NORMAL'
    complete_color = 'GREEN'
    not_complete_color = 'NORMAL'
    percentage_color = 'WHITE'
    limetation_color = 'WHITE'
    size = '15'

    def __init__(self, **kwargs):
        for key in kwargs.keys():
            setattr(self, str(key), str(kwargs[key]))

    # Creating a dict with atributes of this class
    def __iter__(self):
        # first start by grabbing the Class items
        iters = {x:y for x,y in ProgBarTerm.__dict__.items() 
                if not x.startswith('__') and type(y) != types.FunctionType}

        # then update the class items with the instance items
        iters.update(self.__dict__)

        # now 'yield' (Generator) through the items
        for x,y in iters.items():
            yield x,y

    def printDict(self):
        print(dict(self))

if __name__ == '__main__':
    a = ProgBarTerm()
    a.printDict()
    # print(dict(a))
