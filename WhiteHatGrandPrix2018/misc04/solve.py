from pwn import *
import re

#from https://stackoverflow.com/questions/4223313/finding-abc-mod-m
def totient(n):          # n - unsigned int
    result = 1
    p = 2                 #prime numbers - 'iterator'
    while p**2 <= n:
        if n%p == 0:    # * (p-1)
            result *= (p-1)
            n /= p
        while n % p == 0: # * p^(k-1)
            result *= p
            n /= p
        p += 1
    if n != 1:
        result *= (n-1)
    return result

def modpow(p, z, b, c, m) : # (p^z)^(b^c) mod m
    cp = 0
    while m % p == 0 :
        cp += 1
        m /= p              # m = m' now
    t = totient(m)
    exponent = ((pow(b,c,t)*z)%t + t - (cp%t))%t
                            # exponent = z*(b^c)-cp mod t
    return pow(p, cp)*pow(p, exponent, m)

def solve(a,b,c,m) : # split and solve
    result = 1
    p = 2            # primes
    while p**2 <= a :
        z = 0
        while a % p == 0 :
                     # calculate z
            a /= p
            z += 1
        if z != 0 :
            result *=  modpow(p,z,b,c,m)
            result %= m
        p += 1
    if a != 1 :      # Possible last prime
        result *= modpow(a, 1, b, c, m)
    return result % m

r = remote('66.42.33.113', 1337)
count = 0
while 1:
    try:
        check = r.recvuntil('Face_index:')
        face_index = r.recvline()
        face_index = int(face_index.split(' ')[1].replace('\n', ''))
        r.recvline()
        values = r.recvlines(134)
        points = []
        for x in values:
            x = re.sub('\s+', ' ', x).split(' ')
            lip = int(x[1])
            nose = int(x[2])
            eyes = int(x[3])
            forehead = int(x[4])
            y = solve(pow(lip,nose,face_index),eyes,forehead,face_index)
            points.append((y,x[0]))
        points.sort(key=operator.itemgetter(0), reverse=True)
        r.recvuntil('face?')
        r.sendline(str(points[0][1]))
        r.recvuntil('point')
        r.sendline(str(points[0][0]))
    except EOFError:
        print r.recvall()
        break
r.close()
