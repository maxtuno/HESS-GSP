"""
MIT License

Copyright (c) 2012-2022 Oscar Riveros (https://twitter.com/maxtuno, Chile).

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

import random
import math
import hashlib

db = {}


def oracle(seq, sat, clauses):
    count = 0
    for clause in clauses:
        for (x, y) in clause:
            if (x, y) in list(zip(seq, sat)):
                count += 1
                break
    return len(clauses) - count


def next_orbit(seq, sat):
    global db
    for i in range(len(seq)):
        for j in range(len(seq)):
            for k in range(len(seq)):
                key = hashlib.sha1(''.join(list(map(str, seq + sat))).encode())
                if key not in db:
                    db[key] = True
                    return True
                step(i, j, k, seq, sat)
    return False


def step(i, j, k, seq, sat):
    seq[i], seq[j] = seq[j], seq[i]
    # sat[k] = random.randrange(0, b) # randomized
    sat[k] = (sat[k] + 1) % b # deterministic


def hess(clauses):
    seq = list(range(1, n + 1))
    sat = n * [0]
    cur = math.inf
    while next_orbit(seq, sat):
        for i in range(n):
            for j in range(n):
                glb = math.inf
                for k in range(n):
                    aux_1 = seq[:]
                    aux_2 = sat[:]
                    step(i, j, k, seq, sat)
                    loc = oracle(seq, sat, clauses)
                    if loc < glb:
                        glb = loc
                        if glb < cur:
                            cur = glb
                            print(cur)
                            if cur == 0:
                                return seq, sat
                    elif loc > glb:
                        seq = aux_1[:]
                        sat = aux_2[:]
    return []


if __name__ == '__main__':

    n = 100
    # SAT Traditional b = 2
    b = 5
    m = 100
    k = 10

    cls = []
    for i in range(m):
        cl = []
        while True:
            item = random.randint(1, n)
            if item not in cl:
                cl.append((item, random.randrange(0, b)))
            if len(cl) >= random.randint(1, k):
                break
        cls.append(cl)

    with open('test.gcnf', 'w') as file:
        for cl in cls:
            print(cl, file=file)

    seq, sat = hess(cls)

    print(list(zip(seq, sat)))
