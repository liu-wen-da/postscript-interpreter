import sys

from psparser import read
from psbuiltins import Stacks
from elements import StrConstant, DictConstant, Literal, Name, StringExpr
from colors import *

# Postscript examples that use arithmetic operators. 
testinput1 = """
    10 -2 add
    5 sub
    2 mul 
    20 3 mod
"""
#opstack : [6, 2]

# Postscript examples that use comparison operators. 
testinput2 = """
    10 20 lt
    20 15 gt
    (WSU) (WSU) eq
    (Go) dup eq 
    (Cougs) (cougs) eq
"""
# opstack : [True, True, True, True, False]

# Postscript examples that use def, dict, begin, end
testinput3 = """
    /x 1 def
    x
    /x 10 def
    x
"""
# opstack : [1, 10]

testinput4 = """
    /x 1 def
    1 dict begin /x 10 def x end
    x
"""
# opstack : [10, 1]

testinput5 = """
    /x 1 def
    1 dict begin /x 10 def  
        1 dict begin /x 100 def x end 
        x 
    end
    x
"""
# opstack : [100, 10, 1]

testinput6 = """
    /x 1 def
    /y 2 def
    1 dict begin /x 10 def  
        1 dict begin /x 100 def y end 
        y
    end
"""
# opstack : [2, 2]


# Postscript examples that use string operators. 

#test string creation
testinput7 = """
    3 string dup 
    0 80 put
"""
# opstack :  [StrConstant('(P)')]   --  i.e.,  [StrConstant('(P\x00\x00)')] where \x00 is the ASCII NUL character

#test string creation
testinput8 = """
    3 string dup dup dup
    0 80 put
    1 81 put
    2 83 put
"""
# opstack : [StrConstant('(PQS)')]   

testinput9 = """
    /s (WSU Cougs) def
    s length
    s 0 3 getinterval
    length
"""
# opstack : [9, 3]

testinput10 = """
     (CptS 355) dup 5 (451) putinterval
     dup 5 get
"""
# opstack : [StrConstant('(CptS 451)'), 52]

# Postscript examples that use dictionary operators. 

#test string creation
testinput11 = """
    /myd 1 dict def
    myd
"""
# opstack : [DictConstant({})]

#test string creation
testinput12 = """
    /myd 1 dict def
    myd
    myd 1 (one) put
    myd 2 (two) put
"""
# opstack : [DictConstant({1: StrConstant('(one)'), 2: StrConstant('(two)')})]

testinput13 = """
    /myd 1 dict def
    myd /x 1 put
    myd /y 2 put
    myd /x 10 put 
    myd /y get 
    myd /x get 
    myd
"""
# opstack : [2, 10, DictConstant({'/x': 10, '/y': 2})]

testinput14 = """
    /myd 1 dict def
    myd /x 10 put
    myd /y 20 put
    myd
    begin
    x 
    y 
    myd
"""
# opstack : [10, 20, DictConstant({'/x': 10, '/y': 20})]

testinput15 = """
    (355,322,451) (,) search 
"""
# opstack :  [StrConstant('(322,451)'), StrConstant('(,)'), StrConstant('(355 )'), True]  

testinput16 = """
    (355,322,451) (0) search 
"""
# opstack : [StrConstant('(355 ,322,451)'), False] 

# Postscript examples that use stack manipulation operators. 

testinput17 = """
     (WSU) dup /str exch def 
     (WSU) str eq
"""
# opstack : [StrConstant('(WSU)'), True]

testinput18 = """
     1 2 3 4 5 3 copy count 
"""
# opstack : [1, 2, 3, 4, 5, 3, 4, 5, 8]


testinput19 = """
    /isNeg { 0 lt } def  -5 dup isNeg { -1 mul } if
"""
# opstack : [5]

testinput20 = """
    /isNeg { 0 lt } def  -1 dup isNeg { -2 mul } { 3 mul} ifelse
"""
#opstack : [2]

testinput21 = """
    1 1 5 {  } for 
"""
#opstack : [1, 2, 3, 4, 5]

testinput22 = """
    2 2 8 {2 mul } for 
"""
#opstack : [4, 8, 12, 16]

testinput23 = """
    /square {dup mul} def
    /mydict 1 dict def
    mydict /in 1 put 
    mydict /out 100 put
    mydict /in 10 put
    mydict /in get 
    square  
    mydict /out get
    eq 
    {(equal)} {(different)} ifelse
"""
#opstack :[StrConstant('(equal)')]

testinput24 = """
    /x 1 def
    /y 2 def
    /x 10 def
    /y 20 def
    0 x 1 y {add} for
"""
#opstack :[165]

testinput25 = """
    /x 1 def
    /y 2 def
    /myd 1 dict def
    myd /x 10 put 
    myd /y 20 put
    myd begin
    x y mul
    end 
    x y mul 
"""
#opstack : [200, 2]

testinput26 = """
    /x 1 def
    /y 2 def
    1 dict begin
    /x 10 def
    1 dict begin /y 3 def x y end
    /y 20 def
    x y
    end
    x y
"""
#opstack : [10, 3, 10, 20, 1, 2]

testinput27 = """
        1 2 3 4 5 count copy 15 1 1 5 {pop exch sub} for 0 eq
"""
#opstack : [1, 2, 3, 4, 5, True]

testinput28 = """
    /first (CptS355 and CptS451) def
    /second (CptS321 and CptS322) def
    /cpy {  4 3 getinterval /str exch def 
            16 str putinterval } def
    first second cpy
    second first cpy
    first second 
"""   
#opstack : [StrConstant('(CptS355 and CptS321)'), StrConstant('(CptS321 and CptS355)')]
#    
testinput29 = """
    (WSU)
    dup dup dup 
    0 get 87 eq 
        {
            1 get 83 eq 
            { 
                2 get 85 eq 
                { (Go Cougs) }
                if
            } if
        } if
"""
#opstack : [StrConstant('(WSU)'), StrConstant('(Go Cougs)')]

testinput30 = """
        /n 5 def
        /fact {
            0 dict begin
            /n exch def
            n 2 lt
            { 1}
            {n 1 sub fact n mul }
            ifelse
            end
        } def
        n fact
"""
#opstack : [120]

testinput31 = """
    /fact {
            0 dict
            begin
                /n exch def
                1
                n -1 1 { mul /n n 1 sub def } for 
            end
        } def
        6 fact
"""
#opstack :  [720]

testinput32 = """
    3 string 
    dup
    0 87 put
    dup
    1 83 put
    dup 
    2 85 put  
    """
#opstack : [StrConstant('(WSU)')]

tests = [testinput1,testinput2,testinput3,testinput4,testinput5,testinput6,testinput7,testinput8,testinput9,testinput10,
         testinput11,testinput12,testinput13,testinput14,testinput15,testinput16,testinput17,testinput18,testinput19,testinput20,testinput21,
         testinput22,testinput23,testinput24,testinput25,testinput26,testinput27,testinput28,testinput29,testinput30,testinput31,testinput32]

opstack = {
    'test1': [6, 2], 
    'test2': [True, True, True, True, False], 
    'test3': [1, 10], 
    'test4': [10, 1], 
    'test5': [100, 10, 1], 
    'test6': [2, 2], 
    'test7': [StrConstant('(P)')], 
    'test8': [StrConstant('(PQS)')], 
    'test9': [9, 3], 
    'test10': [StrConstant('(CptS 451)'), 52], 
    'test11': [DictConstant({})], 
    'test12': [DictConstant({1: StrConstant('(one)'), 2: StrConstant('(two)')})], 
    'test13': [2, 10, DictConstant({'/x': 10, '/y': 2})], 
    'test14': [10, 20, DictConstant({'/x': 10, '/y': 20})], 
    'test15': [StrConstant('(322,451)'), StrConstant('(,)'), StrConstant('(355 )'), True], 
    'test16': [StrConstant('(355 ,322,451)'), False], 
    'test17': [StrConstant('(WSU)'), True], 
    'test18': [1, 2, 3, 4, 5, 3, 4, 5, 8], 
    'test19': [5], 
    'test20': [2], 
    'test21': [1, 2, 3, 4, 5], 
    'test22': [4, 8, 12, 16], 
    'test23': [StrConstant('(equal)')], 
    'test24': [165], 
    'test25': [200, 2], 
    'test26': [10, 3, 10, 20, 1, 2], 
    'test27': [1, 2, 3, 4, 5, True], 
    'test28': [StrConstant('(CptS355 and CptS321)'), StrConstant('(CptS321 and CptS355)')], 
    'test29': [StrConstant('(WSU)'), StrConstant('(Go Cougs)')], 
    'test30': [120], 
    'test31': [720], 
    'test32': [StrConstant('(WSU)')]}

"""
parse output = {
    'test1': [Literal(10), Literal(-2), Name(add), Literal(5), Name(sub), Literal(2), Name(mul), Literal(20), Literal(3), Name(mod)], 
    'test2': [Literal(10), Literal(20), Name(lt), Literal(20), Literal(15), Name(gt), StringExpr((WSU)), StringExpr((WSU)), Name(eq), StringExpr((Go)), Name(dup), Name(eq), StringExpr((Cougs)), StringExpr((cougs)), Name(eq)], 
    'test3': [Name(/x), Literal(1), Name(def), Name(x), Name(/x), Literal(10), Name(def), Name(x)], 
    'test4': [Name(/x), Literal(1), Name(def), Literal(1), Name(dict), Name(begin), Name(/x), Literal(10), Name(def), Name(x), Name(end), Name(x)], 
    'test5': [Name(/x), Literal(1), Name(def), Literal(1), Name(dict), Name(begin), Name(/x), Literal(10), Name(def), Literal(1), Name(dict), Name(begin), Name(/x), Literal(100), Name(def), Name(x), Name(end), Name(x), Name(end), Name(x)], 
    'test6': [Name(/x), Literal(1), Name(def), Name(/y), Literal(2), Name(def), Literal(1), Name(dict), Name(begin), Name(/x), Literal(10), Name(def), Literal(1), Name(dict), Name(begin), Name(/x), Literal(100), Name(def), Name(y), Name(end), Name(y), Name(end)], 
    'test7': [Literal(3), Name(string), Name(dup), Literal(0), Literal(80), Name(put)], 
    'test8': [Literal(3), Name(string), Name(dup), Name(dup), Name(dup), Literal(0), Literal(80), Name(put), Literal(1), Literal(81), Name(put), Literal(2), Literal(83), Name(put)], 
    'test9': [Name(/s), StringExpr((WSU Cougs)), Name(def), Name(s), Name(length), Name(s), Literal(0), Literal(3), Name(getinterval), Name(length)], 
    'test10': [StringExpr((CptS 355)), Name(dup), Literal(5), StringExpr((451)), Name(putinterval), Name(dup), Literal(5), Name(get)], 
    'test11': [Name(/myd), Literal(1), Name(dict), Name(def), Name(myd)], 
    'test12': [Name(/myd), Literal(1), Name(dict), Name(def), Name(myd), Name(myd), Literal(1), StringExpr((one)), Name(put), Name(myd), Literal(2), StringExpr((two)), Name(put)], 
    'test13': [Name(/myd), Literal(1), Name(dict), Name(def), Name(myd), Name(/x), Literal(1), Name(put), Name(myd), Name(/y), Literal(2), Name(put), Name(myd), Name(/x), Literal(10), Name(put), Name(myd), Name(/y), Name(get), Name(myd), Name(/x), Name(get), Name(myd)], 
    'test14': [Name(/myd), Literal(1), Name(dict), Name(def), Name(myd), Name(/x), Literal(10), Name(put), Name(myd), Name(/y), Literal(20), Name(put), Name(myd), Name(begin), Name(x), Name(y), Name(myd)], 
    'test15': [StringExpr((355 ,322,451)), StringExpr((,)), Name(search)], 
    'test16': [StringExpr((355 ,322,451)), StringExpr((0)), Name(search)], 
    'test17': [StringExpr((WSU)), Name(dup), Name(/str), Name(exch), Name(def), StringExpr((WSU)), Name(str), Name(eq)], 
    'test18': [Literal(1), Literal(2), Literal(3), Literal(4), Literal(5), Literal(3), Name(copy), Name(count)], 
    'test19': [Name(/isNeg), Block([Literal(0), Name(lt)]), Name(def), Literal(-5), Name(dup), Name(isNeg), Block([Literal(-1), Name(mul)]), Name(if)], 
    'test20': [Name(/isNeg), Block([Literal(0), Name(lt)]), Name(def), Literal(-1), Name(dup), Name(isNeg), Block([Literal(-2), Name(mul)]), Block([Literal(3), Name(mul)]), Name(ifelse)], 
    'test21': [Literal(1), Literal(1), Literal(5), Block([]), Name(for)], 
    'test22': [Literal(2), Literal(2), Literal(8), Block([Literal(2), Name(mul)]), Name(for)], 
    'test23': [Name(/square), Block([Name(dup), Name(mul)]), Name(def), Name(/mydict), Literal(1), Name(dict), Name(def), Name(mydict), Name(/in), Literal(1), Name(put), Name(mydict), Name(/out), Literal(100), Name(put), Name(mydict), Name(/in), Literal(10), Name(put), Name(mydict), Name(/in), Name(get), Name(square), Name(mydict), Name(/out), Name(get), Name(eq), Block([StringExpr((equal))]), Block([StringExpr((different))]), Name(ifelse)], 
    'test24': [Name(/x), Literal(1), Name(def), Name(/y), Literal(2), Name(def), Name(/x), Literal(10), Name(def), Name(/y), Literal(20), Name(def), Literal(0), Name(x), Literal(1), Name(y), Block([Name(add)]), Name(for)], 
    'test25': [Name(/x), Literal(1), Name(def), Name(/y), Literal(2), Name(def), Name(/myd), Literal(1), Name(dict), Name(def), Name(myd), Name(/x), Literal(10), Name(put), Name(myd), Name(/y), Literal(20), Name(put), Name(myd), Name(begin), Name(x), Name(y), Name(mul), Name(end), Name(x), Name(y), Name(mul)], 
    'test26': [Name(/x), Literal(1), Name(def), Name(/y), Literal(2), Name(def), Literal(1), Name(dict), Name(begin), Name(/x), Literal(10), Name(def), Literal(1), Name(dict), Name(begin), Name(/y), Literal(3), Name(def), Name(x), Name(y), Name(end), Name(/y), Literal(20), Name(def), Name(x), Name(y), Name(end), Name(x), Name(y)], 
    'test27': [Literal(1), Literal(2), Literal(3), Literal(4), Literal(5), Name(count), Name(copy), Literal(15), Literal(1), Literal(1), Literal(5), Block([Name(pop), Name(exch), Name(sub)]), Name(for), Literal(0), Name(eq)], 
    'test28': [Name(/first), StringExpr((CptS355 and CptS451)), Name(def), Name(/second), StringExpr((CptS321 and CptS322)), Name(def), Name(/cpy), Block([Literal(4), Literal(3), Name(getinterval), Name(/str), Name(exch), Name(def), Literal(16), Name(str), Name(putinterval)]), Name(def), Name(first), Name(second), Name(cpy), Name(second), Name(first), Name(cpy), Name(first), Name(second)], 
    'test29': [StringExpr((WSU)), Name(dup), Name(dup), Name(dup), Literal(0), Name(get), Literal(87), Name(eq), Block([Literal(1), Name(get), Literal(83), Name(eq), Block([Literal(2), Name(get), Literal(85), Name(eq), Block([StringExpr((Go Cougs))]), Name(if)]), Name(if)]), Name(if)], 
    'test30': [Name(/n), Literal(5), Name(def), Name(/fact), Block([Literal(0), Name(dict), Name(begin), Name(/n), Name(exch), Name(def), Name(n), Literal(2), Name(lt), Block([Literal(1)]), Block([Name(n), Literal(1), Name(sub), Name(fact), Name(n), Name(mul)]), Name(ifelse), Name(end)]), Name(def), Name(n), Name(fact)], 
    'test31': [Name(/fact), Block([Literal(0), Name(dict), Name(begin), Name(/n), Name(exch), Name(def), Literal(1), Name(n), Literal(-1), Literal(1), Block([Name(mul), Name(/n), Name(n), Literal(1), Name(sub), Name(def)]), Name(for), Name(end)]), Name(def), Literal(6), Name(fact)], 
    'test32': [Literal(3), Name(string), Name(dup), Literal(0), Literal(87), Name(put), Name(dup), Literal(1), Literal(83), Name(put), Name(dup), Literal(2), Literal(85), Name(put)]}
"""

from copy import deepcopy
# program start
if __name__ == '__main__':

    psstacks = Stacks()  
    testnum = 1
    for testcase in tests:
        print("--------------------------------------------------------")
        try:
            expr_list = read(testcase)
            for expr in expr_list:
                expr.eval(psstacks)
            print("--test {}--".format(testnum))
            testnum += 1
            print(CYAN+'opstack '+CEND, psstacks.opstack)
            print('dictstack ' , psstacks.dictstack)
            psstacks.clearBoth()
        except (SyntaxError, NameError, TypeError, Exception) as err:
            print(type(err).__name__ + ':', err)
            psstacks.clearBoth()
    