#!/usr/bin/env python3
"""LISP interpreter from scratch -- pure Python. Lambda, recursion, map, filter."""
import operator

def tokenize(s):
    return s.replace("("," ( ").replace(")"," ) ").split()

def parse(tokens):
    if not tokens: raise SyntaxError("unexpected EOF")
    tok = tokens.pop(0)
    if tok == "(":
        lst = []
        while tokens[0] != ")": lst.append(parse(tokens))
        tokens.pop(0); return lst
    elif tok == ")": raise SyntaxError("unexpected )")
    else:
        for fn in (int, float):
            try: return fn(tok)
            except ValueError: pass
        return tok

def read(s): return parse(tokenize(s))

class Env(dict):
    def __init__(self, params=(), args=(), outer=None):
        super().__init__(); self.update(zip(params,args)); self.outer=outer
    def find(self, k):
        if k in self: return self
        if self.outer: return self.outer.find(k)
        raise NameError(f"undefined: {k}")

def std_env():
    e = Env()
    e.update({"+":operator.add,"-":operator.sub,"*":operator.mul,
              "/":operator.truediv,"//":operator.floordiv,"%":operator.mod,
              "<":operator.lt,">":operator.gt,"<=":operator.le,">=":operator.ge,
              "=":operator.eq,"abs":abs,"max":max,"min":min,
              "not":operator.not_,"list":lambda*x:list(x),
              "car":lambda x:x[0],"cdr":lambda x:x[1:],
              "cons":lambda a,b:[a]+(b if isinstance(b,list) else [b]),
              "null?":lambda x:x==[],"length":len,
              "map":lambda f,l:list(map(f,l)),
              "filter":lambda f,l:list(filter(f,l)),
              "begin":lambda*x:x[-1],
              "#t":True,"#f":False,"nil":[]})
    return e

GENV = std_env()

class Lambda:
    def __init__(self,p,b,e): self.p=p; self.b=b; self.e=e
    def __call__(self,*a): return evaluate(self.b, Env(self.p,a,self.e))

def evaluate(x, env=GENV):
    if isinstance(x, str): return env.find(x)[x]
    if not isinstance(x, list): return x
    h = x[0]
    if h=="quote": return x[1]
    if h=="if":
        alt = x[3] if len(x)>3 else None
        return evaluate(x[2] if evaluate(x[1],env) else alt, env)
    if h=="define": env[x[1]] = evaluate(x[2],env); return None
    if h=="lambda": return Lambda(x[1],x[2],env)
    if h=="let":
        ps=[b[0] for b in x[1]]; args=[evaluate(b[1],env) for b in x[1]]
        return evaluate(x[2], Env(ps,args,env))
    if h=="begin":
        r=None
        for e2 in x[1:]: r=evaluate(e2,env)
        return r
    proc = evaluate(h, env)
    args = [evaluate(a,env) for a in x[1:]]
    return proc(*args)

def lisp(s): return evaluate(read(s))

if __name__ == "__main__":
    print("LISP interpreter -- terminal-zero\n")
    lisp("(define fact (lambda (n) (if (<= n 1) 1 (* n (fact (- n 1))))))")
    print("Factorial:")
    for n in [0,1,5,10]: print(f"  (fact {n}) => {lisp(f'(fact {n})')}")
    lisp("(define fib (lambda (n) (if (< n 2) n (+ (fib (- n 1)) (fib (- n 2))))))")
    print("\nFibonacci:")
    for n in [0,1,5,10,15]: print(f"  (fib {n}) => {lisp(f'(fib {n})')}")
    r = lisp("(map (lambda (x) (* x x)) (list 1 2 3 4 5))")
    print(f"\n  (map square [1..5]) => {r}")
    r = lisp("(filter (lambda (x) (= (% x 2) 0)) (list 1 2 3 4 5 6))")
    print(f"  (filter even  [1..6]) => {r}")
    r = lisp("(let ((x 10) (y 20)) (+ x y))")
    print(f"  (let x=10 y=20)  => {r}")
    print("\nAll LISP demos OK.")
