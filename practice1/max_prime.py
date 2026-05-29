#!/usr/bin/env python3
def max_prime_up_to(n):
    sieve = [True] * (n+1)
    sieve[0:2] = [False, False]
    p = 2
    while p*p <= n:
        if sieve[p]:
            for i in range(p*p, n+1, p):
                sieve[i] = False
        p += 1
    for x in range(n, 1, -1):
        if sieve[x]:
            return x
    return None


if __name__ == "__main__":
    print(max_prime_up_to(1000))  # => 997
