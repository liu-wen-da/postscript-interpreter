"""Parts of this code was adopted from https://composingprograms.com/. 
The code has been changed according to Postscript syntax. 
https://creativecommons.org/licenses/by-sa/3.0/
"""
class Expr:
    """
    When you type input into this interpreter, it is parsed (read) into an expression. 
    This expression is represented in our code as an instance of this `Expr` class.
    In our interpreter, there are four types of expressions:
        1.	Literal:  represents primitive constants : integers or booleans . The `value` attribute contains the fixed value the `Literal` refers to. 
        2.	Name: represents names of variables, functions, or operators .  The `var_name` attribute contains the name of the variable as a Python string, e.g., '/sq','sq','add','def'. If the `var_name` starts with a `/` character, Name represents a name constant, otherwise it represents a variable reference ,  function call, or a built-in operator call. 
        3.	StringExpr: represents strings. The `value` attribute contains the string value the `StringExpr` refers to e.g., '(CptS355)'.
        4.	Block: represents body of a function or if, ifelse, or for expressions. The `value` attribute is a Python list that includes the tokens of the PostScript code-array (block) it represents [Literal(10), Literal(5),Name(mul)]
    In our code, the four types of expressions are subclasses of the `Expr`
    class: `Literal`, `Name`, `StringExpr`, and `Block`.
    """

    def __init__(self, value):
        self.value = value

    def eval(self, psstacks):
        """
        Each subclass of Expr implements its own eval method.
        `psstacks` is the Stacks object that include the `opstack` and `dictstack`. 
        Subclasses of `Expr` should implement this method. (i.e., `Literal`, `Name`, `StringExpr`, and `Block`  )
        This method should return a `Value` instance, the result of  evaluating the expression.
        """
        raise NotImplementedError

    def __str__(self):
        """ Returns a parsable and human-readable string of this expression (i.e.    what you would type into the interpreter).  """
        raise NotImplementedError
    
    def __repr__(self):
        """  Returns how this expression is written in our Python representation.   """
        return "{}({})".format(type(self).__name__, self.value)

class Literal(Expr):
    """A literal is notation for representing a primitive constant value in code. 
    In our interpreter, a `Literal` evaluates to a number (int)  or a boolen. The evaluated value is pushed onto the stack. 
    The `value` attribute contains the fixed value the `Literal` refers to.
    """
    def __init__(self, value):
        Expr.__init__(self, value)
        self.value = value

    def eval(self, psstacks):
        """TO-DO (part2)"""
        psstacks.opPush(self.value)

    def __str__(self):
        return str(self.value)

class StringExpr(Expr):
    """A StringExpr is notation for representing a string constant in code. `
    In our interpreter, a `StringExpr` evaluates to a `StrConstant` object. The evaluated StrConstant value is pushed onto the stack. 
    The `value` attribute contains the string value the `StringExpr` refers to.
    """
    def __init__(self, value):
        Expr.__init__(self, value)
        self.value = value

    def eval(self, psstacks):
        """TO-DO (part2)"""
        psstacks.opPush(StrConstant(self.value))

    def __str__(self):
        return str(self.value)

class Name(Expr):
    """A `Name` is a variable , a built-in operator, or a function. 
        a.	If the `Name` represents a name constant (i.e., its `var_name` attribute starts with a `/`), it will be evaluated to a Python string having value `var_name` . The evaluated value will be pushed onto the opstack.
        b.	If the `Name` represents a built-in operator (i.e., its `var_name` attribute is one of the built-in operator names),  then we will evaluate it by executing the operator function defined in psbuiltins.py in the current environment (opstack). 
        c.	If the `Name` represents a variable or function, interpreter looks up the value of the variable in the current environment (dictstack).
            i.	If the variable value is a code-array (`CodeArray`), it should be applied (i.e., executed) by calling its `apply` method.  
            ii.	Otherwise, the variable value is a constant and it should be pushed onto the opstack. 

       The `var_name` attribute contains the name of the variable (as a Python string).
    """
    def __init__(self, var_name):
        Expr.__init__(self, var_name)
        self.var_name = var_name

    def eval(self,psstacks):
        """TO-DO (part2)"""
        if self.var_name.startswith('/'):
            psstacks.opPush(self.var_name)
        elif self.var_name in psstacks.builtin_operators:
            psstacks.builtin_operators[self.var_name]() 
        else:
            x = psstacks.lookup(self.var_name) 
            if isinstance(x, CodeArray):
                x.apply(psstacks)
            else:
                psstacks.opPush(x)

    def __str__(self):
        return str(self.var_name)

class Block(Expr):
    """A `Block` is a notation for representing a code block in PostScript, i.e., a function body, `if` block, `ifelse` block, or `for` loop block. 
    In our interpreter, a `Block` evaluates to a `CodeArray` object. The `CodeArray` value is pushed onto the stack.   
    The `value` attribute contains the list of tokens in the code array.
    """
    def __init__(self, value):
        Expr.__init__(self, value)
        self.value = value

    def eval(self, psstacks):
        """TO-DO (part2)"""
        psstacks.opPush(CodeArray(self.value))

    def __str__(self):
        return str(self.value)

## -----------------------------------------------------------------------------------
## -----------------------------------------------------------------------------------

class Value:
    """
    "Value" objects represent the string , dictionary, and code-array constants that are pushed onto the stack.  
    
    In our interpreter,
        -  For simplicity, the integers and boolean values are pushed onto the opstack as integers and booleans, respectively. 
        -  Similarly, name constants (e.g. '/x') are pushed to the opstack as strings. 
        -  The string, dictionary, and Block constants are represented as StrConstant, DictConstant, and CodeArray objects, 
           which are subclasses of the `Value`. 
        -  StrConstant, DictConstant, and CodeArray implement the following methods in the `Value` interface:
            * apply : Evaluates the value. `apply` is only applicable to CodeArray objects (applies the function, evaluates all the tokens in the function's code-array, i.e., CodeArray )  
            * __str__: Conversts the value to  a human-readable version (i.e., string) for printing.
    """
    def __init__(self, value):
        self.value = value

    def apply(self, psstack):
        """
        Each subclass of Value implements its own `apply` method.
        Note that only `CodeArray`s can be "applied"; attempting to apply a StrConstant or DictConstant will give an error. 
        """
        raise NotImplementedError

    def __str__(self):
        """ Returns a parsable and human-readable version of this value (i.e. the string to be displayed in the interpreter). """
        raise NotImplementedError

    def __repr__(self):
        """ Returns how this value is printed in our Python representation.   """
        return "{}({})".format(type(self).__name__, self.value)

class StrConstant(Value):
    """A  string constant delimited in paranthesis. Attempting to apply a `string constant` will give an error.
      The `value` attribute is the Python string that this value represents.

      You may add additional methods to this class as needed and use them in your operator implementations. 
    """
    def __init__(self, value):
        Value.__init__(self, value)
        self.value = value

    def apply(self, psstacks):
        raise TypeError("Ouch! Cannot apply `string constant` {} ".format(self.value))

    def __str__(self):
        return "{}('{}')".format(type(self).__name__, self.value)
    
    def __repr__(self):
        return "{}('{}')".format(type(self).__name__, self.value)

    # returns length of the string value
    def length(self):
        return len(self.value)

class DictConstant(Value):
    """A dictionary contant. Attempting to apply an `dictionary constant` will give an error.
      The `value` attribute is the Python dictionary that this value represents.
      You may add additional methods to this class as needed and use them in your operator implementations. 
    """
    def __init__(self, value):
        Value.__init__(self, value)
        self.value = value

    def apply(self, psstacks):
        raise TypeError("Ouch! Cannot apply `string constant` {} ".format(self.value))

    def __str__(self):
        return "{}({})".format(type(self).__name__, self.value)

    # returns length of the array value
    def length(self):
        return len(list(self.value.keys()))    

class CodeArray(Value):
    """The constant-array that represents the body of a (user-defined) function, or if, ifelse, for operators. 
    The `body` attribute is a nested list of expressions.
    The `apply` method will evaluate each expression in the `body` by calling token's `eval` method. 
    Expressions will be evaluated in the current referencing environment (psstacks).  
    """
    def __init__(self, body):
        Value.__init__(self, body)
        self.body = body

    def apply(self, psstacks):
        """ TO-DO in part2 """
        for expr in self.body: 
            expr.eval(psstacks) 

    def __str__(self):
        return "{}({})".format(type(self).__name__, self.body)




