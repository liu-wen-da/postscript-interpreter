from colors import *
from elements import StrConstant, DictConstant, CodeArray

class Stacks:
    def __init__(self):
        #stack variables
        self.opstack = []  #assuming top of the stack is the end of the list
        self.dictstack = []  #assuming top of the stack is the end of the list
        # The environment that the REPL evaluates expressions in.
        # Uncomment this dictionary in part2
        self.builtin_operators = {
            "add":self.add,
            "sub":self.sub,
            "mul":self.mul,
            "mod":self.mod,
            "eq":self.eq,
            "lt": self.lt,
            "gt": self.gt,
            "dup": self.dup,
            "exch":self.exch,
            "pop":self.pop,
            "copy":self.copy,
            "count": self.count,
            "clear":self.clear,
            "stack":self.stack,
            "dict":self.psDict,
            "string":self.string,
            "length":self.length,
            "get":self.get,
            "put":self.put,
            "getinterval":self.getinterval,
            "putinterval":self.putinterval,
            "search" : self.search,
            "begin":self.begin,
            "end":self.end,
            "def":self.psDef,
            "if":self.psIf,
            "ifelse":self.psIfelse,
            "for":self.psFor
        }
    #------- Operand Stack Helper Functions --------------
    
    """
        Helper function. Pops the top value from opstack and returns it.
    """
    def opPop(self):
        if len(self.opstack) > 0:
            x = self.opstack[len(self.opstack) - 1]
            self.opstack.pop(len(self.opstack) - 1)
            return x
        else:
            print("Error: opPop - Operand stack is empty")

    """
       Helper function. Pushes the given value to the opstack.
    """
    def opPush(self,value):
        self.opstack.append(value)

    #------- Dict Stack Helper Functions --------------
    """
       Helper function. Pops the top dictionary from dictstack and returns it.
    """  
    def dictPop(self):
        if len(self.dictstack) > 1:
            return self.dictstack.pop()
        else:
            return print("Error")
        

    """
       Helper function. Pushes the given dictionary onto the dictstack. 
    """   
    def dictPush(self,d):
        return self.dictstack.append(d)

    """
       Helper function. Adds name:value pair to the top dictionary in the dictstack.
       (Note: If the dictstack is empty, first adds an empty dictionary to the dictstack then adds the name:value to that. 
    """  
    def define(self,name, value):
        if len(self.dictstack) == 0:
            new_dict = {}
            new_dict[name] = value
            self.dictstack.append(new_dict)
        else:
            self.dictstack[-1][name] = value

    """
       Helper function. Searches the dictstack for a variable or function and returns its value. 
       (Starts searching at the top of the dictstack; if name is not found returns None and prints an error message.
        Make sure to add '/' to the begining of the name.)
    """
    def lookup(self,name):
        for i in range(len(self.dictstack)):
            dict_S = self.dictstack[-1 - i ]
            if name in dict_S.keys():
                return dict_S[name]
            if "/" + name in dict_S.keys():
                return dict_S["/" + name]
    
    #------- Arithmetic Operators --------------

    """
       Pops 2 values from opstack; checks if they are numerical (int); adds them; then pushes the result back to opstack. 
    """  
    def add(self):
        if len(self.opstack) > 1:
            op1 = self.opPop()
            op2 = self.opPop()
            if isinstance(op1,int) and isinstance(op2,int):
                self.opPush(op1 + op2)
            else:
                print("Error: add - one of the operands is not a number value")
                self.opPush(op2)
                self.opPush(op1)

    """
       Pops 2 values from opstack; checks if they are numerical (int); subtracts them; and pushes the result back to opstack. 
    """ 
    def sub(self):
        if len(self.opstack) > 1:
            op1 = self.opPop()
            op2 = self.opPop()
            if isinstance(op1,int) and isinstance(op2,int):
                self.opPush(op2 - op1)
            else:
                print("Error: sub - one of the operands is not a number value")
                self.opPush(op2)
                self.opPush(op1) 
        else:
            print("Error: sub expects 2 operands")

    """
        Pops 2 values from opstack; checks if they are numerical (int); multiplies them; and pushes the result back to opstack. 
    """
    def mul(self):
        if len(self.opstack) > 1:
            op1 = self.opPop()
            op2 = self.opPop()
            if isinstance(op1,int) and isinstance(op2,int):
                self.opPush(op1 * op2)
            else:
                print("Error: mul - one of the operands is not a number value")
                self.opPush(op2)
                self.opPush(op1) 
        else:
            print("Error: Mul expects 2 operands")

    """
        Pops 2 values from stack; checks if they are int values; calculates the remainder of dividing the bottom value by the top one; 
        pushes the result back to opstack.
    """
    def mod(self):
        if len(self.opstack) > 1:
            op1 = self.opPop()
            op2 = self.opPop()
            if isinstance(op1,int) and isinstance(op2,int):
                self.opPush(op2 % op1)
            else:
                print("Error: mod - one of the operands is not a number value")
                self.opPush(op2)
                self.opPush(op1) 
        else:
            print("Error: mod expects 2 operands")

    """ Pops 2 values from stacks; if they are equal pushes True back onto stack, otherwise it pushes False.
          - if they are integers or booleans, compares their values. 
          - if they are StrConstant values, compares the `value` attributes of the StrConstant objects;
          - if they are DictConstant objects, compares the objects themselves (i.e., ids of the objects).
        """
    def eq(self):
        if len(self.opstack) > 0:
            op1 = self.opPop()
            op2 = self.opPop()
            if isinstance(op1,int) and isinstance(op2,int):
                self.opPush(op1 == op2)
            elif isinstance(op1,bool) and isinstance(op2,bool):
                self.opPush(op1 == op2)
            elif isinstance(op1,StrConstant) and isinstance(op2,StrConstant):
                self.opPush(op1.value == op2.value)
            elif isinstance(op1,DictConstant) and isinstance(op2,DictConstant):
                self.opPush(op1 == op2)
            else:
                self.opPush(False)
        else:
            print("Error: operand stack is empty")

    """ Pops 2 values from stacks; if the bottom value is less than the second, pushes True back onto stack, otherwise it pushes False.
          - if they are integers or booleans, compares their values. 
          - if they are StrConstant values, compares the `value` attributes of them;
          - if they are DictConstant objects, compares the objects themselves (i.e., ids of the objects).
    """  
    def lt(self):
        if len(self.opstack) >1:
            op1 = self.opPop()
            op2 = self.opPop()
            if isinstance(op1,int) and isinstance(op2,int):
                if op1 > op2:
                    self.opPush(True)
                else:
                    self.opPush(False)
        else:
            print("There was an Erorr")


    """ Pops 2 values from stacks; if the bottom value is greater than the second, pushes True back onto stack, otherwise it pushes False.
          - if they are integers or booleans, compares their values. 
          - if they are StrConstant values, compares the `value` attributes of them;
          - if they are DictConstant objects, compares the objects themselves (i.e., ids of the objects).
    """  
    def gt(self):
        if len(self.opstack) >1:
            op1 = self.opPop()
            op2 = self.opPop()
            if isinstance(op1,int) and isinstance(op2,int):
                if op1 < op2:
                    self.opPush(True)
                else:
                    self.opPush(False)
        else:
            print("There was an Erorr")

    #------- Stack Manipulation and Print Operators --------------
    """
       This function implements the Postscript "pop operator". Calls self.opPop() to pop the top value from the opstack and discards the value. 
    """
    def pop (self):
        if (len(self.opstack) > 0):
            self.opPop()
        else:
            print("Error: pop - not enough arguments")

    """
       Prints the opstack and dictstack. The end of the list is the top of the stack. 
    """
    def stack(self):
        print(OKGREEN+"**opstack**")
        for item in reversed(self.opstack):
            print(item)
        print("-----------------------"+CEND)
        print(RED+"**dictstack**")
        for item in reversed(self.dictstack):
            print(item)
        print("-----------------------"+ CEND)


    """
       Copies the top element in opstack.
    """
    def dup(self):
        if len(self.opstack) > 0:
            self.opPush(self.opstack[-1])
        else: 
            print("There was an Erorr")

    """
       Pops an integer count from opstack, copies count number of values in the opstack. 
    """
    def copy(self):
          if len(self.opstack) > 0:
            count = self.opPop()
            l = []
            for i in range(count):
                l.append(self.opstack[len(self.opstack)-1-i])
            l.reverse()
            for i in l:
                self.opPush(i)

    """
        Counts the number of elements in the opstack and pushes the count onto the top of the opstack.
    """
    def count(self):
        self.opPush(len(self.opstack))

    """
       Clears the opstack.
    """
    def clear(self):
        del self.opstack[:]
        del self.dictstack[:]
        
    """
       swaps the top two elements in opstack
    """
    def exch(self):
        if len(self.opstack) > 1:
            op1 = self.opPop()
            op2 = self.opPop()
            self.opPush(op1)
            self.opPush(op2)
        else:
            print("There was an Erorr")

    # ------- String and Dictionary creator operators --------------

    """ Creates a new empty string  pushes it on the opstack.
    Initializes the characters in the new string to \0 , i.e., ascii NUL """
    def string(self):
        if len(self.opstack) > 0:
            x = self.opPop()
            string = '('+'\0'*x+')'
            self.opPush(StrConstant(string))
        else: 
            print("Error")

    
    """Creates a new empty dictionary  pushes it on the opstack """
    def psDict(self):
        if len(self.opstack) > 0:
            self.opPop()
            self.opPush(DictConstant({}))

    # ------- String and Dictionary Operators --------------
    """ Pops a string or dictionary value from the operand stack and calculates the length of it. Pushes the length back onto the stack.
       The `length` method should support both DictConstant and StrConstant values.
    """
    def length(self):
        if len(self.opstack) > 0:
            elem = self.opPop()
            if isinstance(elem,StrConstant):
                x = elem.value[1:-1]
                self.opPush(len(x))
            elif isinstance(elem,DictConstant):
                y = elem.value
                self.opPush(len(y))
        else:
            print("Error - operand stack is empty")



    """ Pops either:
         -  "A (zero-based) index and an StrConstant value" from opstack OR 
         -  "A `name` (i.e., a key) and DictConstant value" from opstack.  
        If the argument is a StrConstant, pushes the ascii value of the the character in the string at the index onto the opstack;
        If the argument is an DictConstant, gets the value for the given `name` from DictConstant's dictionary value and pushes it onto the opstack
    """
    def get(self):
        if len(self.opstack) > 1:
            ind = self.opPop()
            elem = self.opPop()
            if isinstance(elem,StrConstant) and isinstance(ind,int):
                elem = elem.value[1:-1] 
                value = ord(elem[ind])
                self.opPush(value)
            elif isinstance(elem,DictConstant):
                value = elem.value[ind]
                self.opPush(value)
        else:
            print("Error - operand stack is not long enough")
   
    """
    Pops either:
    - "An `item`, a (zero-based) `index`, and an StrConstant value from  opstack", OR
    - "An `item`, a `name`, and a DictConstant value from  opstack". 
    If the argument is a StrConstant, replaces the character at `index` of the StrConstant's string with the character having the ASCII value of `item`.
    If the argument is an DictConstant, adds (or updates) "name:item" in DictConstant's dictionary `value`.
    """
    def put(self):
        if len(self.opstack) > 2: 
            item = self.opPop()
            ind = self.opPop()
            elem = self.opPop()
            if isinstance(elem,StrConstant) and isinstance(ind,int):
                x = elem.value
                elem.value = x[:(ind+1)] + chr(item) + x[(ind+2):]
            elif isinstance(elem,DictConstant):
                elem.value[ind] = item
        else:
            print("Error - operand stack is not long enough")

    """
    getinterval is a string only operator, i.e., works only with StrConstant values. 
    Pops a `count`, a (zero-based) `index`, and an StrConstant value from  opstack, and 
    extracts a substring of length count from the `value` of StrConstant starting from `index`,
    pushes the substring back to opstack as a StrConstant value. 
    """ 
    def getinterval(self):
        if len(self.opstack) > 2:
            cnt = self.opPop()
            ind = self.opPop()
            elem = self.opPop()
            if isinstance(elem,StrConstant):
                string = elem.value[1:-1] 
                new_s = '(' + string[ind: (ind+cnt)] + ')' 
                self.opPush(StrConstant(new_s))
        else:
            print("Error - operand stack is not long enough")

    """
    putinterval is a string only operator, i.e., works only with StrConstant values. 
    Pops a StrConstant value, a (zero-based) `index`, a `substring` from  opstack, and 
    replaces the slice in StrConstant's `value` from `index` to `index`+len(substring)  with the given `substring`s value. 
    """
    def putinterval(self):
        if len(self.opstack) > 2:
            substr = self.opPop()
            ind = self.opPop()
            elem = self.opPop()
            if isinstance(elem,StrConstant) and isinstance(substr,StrConstant):
                substr = substr.value[1:-1]
                x = elem.value
                elem.value = x[:(ind+1)] + substr + x[(ind+len(substr)+1):]
        else:
            print("Error - operand stack is not long enough")

    """
    search is a string only operator, i.e., works only with StrConstant values. 
    Pops two StrConstant values: delimiter and inputstr
    if delimiter is a sub-string of inputstr then, 
       - splits inputstr at the first occurence of delimeter and pushes the splitted strings to opstack as StrConstant values;
       - pushes True 
    else,
        - pushes  the original inputstr back to opstack
        - pushes False
    """
    def search(self):
        if len(self.opstack) > 1: # at least 2 elements
            delimiter = self.opPop()
            inputstr = self.opPop()
            if isinstance(delimiter, StrConstant) and isinstance(inputstr, StrConstant):
                dlmtr = delimiter.value[1:-1]
                ipstr = inputstr.value[1:-1]
                if dlmtr in ipstr:
                    ind = ipstr.index(dlmtr)
                    frontstr = '(' + ipstr[:ind] + ')'
                    tailstr = '(' + ipstr[(ind+len(dlmtr)):] + ')'
                    self.opPush(StrConstant(tailstr))
                    self.opPush(delimiter)
                    self.opPush(StrConstant(frontstr))
                    self.opPush(True)
                else:
                    self.opPush(inputstr)
                    self.opPush(False)
        else:
            print("Error - operand stack is not long enough")

    # ------- Operators that manipulate the dictstact --------------
    """ begin operator
        Pops a DictConstant value from opstack and pushes it's `value` to the dictstack."""
    def begin(self):
        if len(self.opstack) > 0:
            elem = self.opPop()
            if isinstance(elem,DictConstant):
                self.dictPush(elem.value)
        else:
            print("Error - operand stack is empty")

    """ end operator
        Pops the top dictionary from dictstack."""
    def end(self):
        if len(self.dictstack) > 0:
            self.dictPop()
        else: 
            print("There was am Erorr")
        
    """ Pops a name and a value from stack, adds the definition to the dictionary at the top of the dictstack. """
    def psDef(self):
        value = self.opPop()
        name = self.opPop()
        self.define(name, value)

    # ------- if/ifelse Operators --------------
    """ if operator
        Pops a Block and a boolean value, if the value is True, executes the code array by calling apply.
       Will be completed in part-2. 
    """
    def psIf(self):
        block = self.opPop()
        value = self.opPop()
        if value == True:
            CodeArray(block.value).apply(self)

        
        

    """ ifelse operator
        Pops two Blocks and a boolean value, if the value is True, executes the bottom Block otherwise executes the top Block.
        Will be completed in part-2. 
    """
    def psIfelse(self):
       T_block = self.opPop() 
       B_block = self.opPop()
       value = self.opPop()
       if value == True:
           CodeArray(B_block.value).apply(self)
       else: 
           CodeArray(T_block.value).apply(self)



    #------- Loop Operators --------------
    """
       Implements for operator.   
       Pops a Block, the end index (end), the increment (inc), and the begin index (begin) and 
       executes the code array for all loop index values ranging from `begin` to `end`. 
       Pushes the current loop index value to opstack before each execution of the Block. 
       Will be completed in part-2. 
    """ 
    def psFor(self):
       block = self.opPop()
       end = self.opPop()
       inc = self.opPop()
       begin = self.opPop()
       ind = begin
       while (begin <= ind <= end) or (end <= ind <= begin):
           self.opPush(ind)
           CodeArray(block.value).apply(self)
           ind += inc
  
    

   

    """ Cleans both stacks. """      
    def clearBoth(self):
        self.opstack[:] = []
        self.dictstack[:] = []

    """ Will be needed for part2"""
    def cleanTop(self):
        if len(self.opstack)>1:
            if self.opstack[-1] is None:
                self.opstack.pop()

