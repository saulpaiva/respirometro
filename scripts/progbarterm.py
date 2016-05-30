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
        iters = dict((x,y) for x,y in ProgBarTerm.__dict__.items() 
                if not (x[:2] == '__' and type(y) == types.MethodType))

        this_dict = dict((x,y) for x,y in self.__dict__.items() 
                if not (x[:2] == '__' and type(y) == types.MethodType))
        # then update the class items with the instance items
        iters.update(this_dict)

        # now 'yield' (Generator) through the items
        for x,y in iters.items():
            if not(type(y) == types.MethodType):
                yield x,y

    def test(self):
        print(dict(self.__dict__))

if __name__ == '__main__':
    a = ProgBarTerm()
    print(a.test())
    print(dict(a))
