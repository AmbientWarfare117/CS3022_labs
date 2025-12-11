"""
------------------------------------------------------------------------------------------------------------------------
File Name: PeaseNumber_Andersen.py
Author: Tyler Andersen
Description: This program will prompt the user to enter Your Birthday which includes an array with a Month, Day, 
and Year. After which, the program will calculate the Fibonacci Birthday Constant (FBC) for the YB, which is an array 
of the fibonacci number for the first and second YB elements. It will then calculate the Collatz Fibonacci Birthday 
(CFB) number that is comprised of an array with the Collatz of the first and second FBC elements and the third YB 
element. Finally, the program will output the Pease Number (PN) which is the sum of the CFB array elements. 
------------------------------------------------------------------------------------------------------------------------
"""

from typing import List, Any, Callable, Set

#------------------------------------------------------------------------------------------------------------------------
#                                                  M O N A D  C L A S S (Extra Credit # 1)
#------------------------------------------------------------------------------------------------------------------------
class Monad:
    def __init__(self, value: Any):
        self.value = value

    def bind(self, func: Callable[[Any], Any]) -> "Monad":
        return Monad(func(self.value))

#------------------------------------------------------------------------------------------------------------------------
#                                               C L O S U R E  P A T T E R N (Extra Credit # 3)
#------------------------------------------------------------------------------------------------------------------------
def Fib_Lookup_Closure() -> Callable[[int], int]:
    lookup: dict[int, int] = {0: 0, 1: 1}
    def fibonacci(n: int) -> int:
        if n in lookup:
            return lookup[n]
        value = fibonacci(n - 1) + fibonacci(n - 2)
        lookup[n] = value
        return value
    return fibonacci

def Collatz_Lookup_Closure() -> Callable[[int], int]:
    lookup: dict[int, int] = {1: 0}
    def collatz(n: int) -> int:
        if n in lookup:
            return lookup[n]
        if n % 2 == 0:
            next_n = n // 2
        else:
            next_n = 3 * n + 1
        steps = 1 + collatz(next_n)
        lookup[n] = steps   
        return steps
    return collatz

fibonacci = Fib_Lookup_Closure()      # Fibonacci closure instance
collatz = Collatz_Lookup_Closure()    # Collatz closure instance

#------------------------------------------------------------------------------------------------------------------------
#                                               P U R E  F U N C T I O N S
#------------------------------------------------------------------------------------------------------------------------

def FBC(YB: List[int]) -> List[int]: 
    month, day, _ = YB                
    return [fibonacci(month), fibonacci(day)]

def CFB(FBC_values: List[int], YB: List[int]) -> List[int]:
    year = YB[2]
    return [
        collatz(FBC_values[0]),
        collatz(FBC_values[1]),
        collatz(year),
    ]

def Pease_Number(CFB_values: List[int]) -> int:
    if not CFB_values:
        return 0
    return CFB_values[0] + Pease_Number(CFB_values[1:])

#------------------------------------------------------------------------------------------------------------------------
# Extra Credit 1#: Monadic chaining operations
#------------------------------------------------------------------------------------------------------------------------
def pease_monadic(YB: List[int]) -> int:
    return (
        Monad(YB)
        .bind(lambda yb: (yb, FBC(yb)))                                         # (YB, FBC)
        .bind(lambda yb_fbc: (yb_fbc[0], yb_fbc[1], CFB(yb_fbc[1], yb_fbc[0]))) # (YB, FBC, CFB)
        .bind(lambda triple: Pease_Number(triple[2]))                           # PN
        .value
    )

#------------------------------------------------------------------------------------------------------------------------
# Extra Credit 2#: Boolean function to detect Collatz convergence.
# I discovered that all positive integers are believed to converge to 1 under the Collatz conjecture and it currently 
# remains unsolved. All outputs for positive integers will return True!
#------------------------------------------------------------------------------------------------------------------------
def collatz_detection(n: int, seen: set[int] = None) -> bool:
    if n <= 0:
        return False    # Collatz conjecture is defined for positive integers only.
    else:
        return True     # All positive integers are believed to converge to 1.

#------------------------------------------------------------------------------------------------------------------------
#                                                       M A I N
#------------------------------------------------------------------------------------------------------------------------
def main() -> None: # Mutations/ side-effects confined to main
    month = int(input("Enter a Birth Month (1-12): "))
    if month not in range(1, 13):
        print("Invalid month. Please enter a month between 1 and 12.")
        return

    day = int(input("Enter a Birth Day (1-31): "))
    if day not in range(1, 32):
        print("Invalid day. Please enter a day between 1 and 31.")
        return

    year = int(input("Enter a Birth Year (ex: 1990): "))
    if year < 0:
        print("Invalid year. Please enter a positive year.")
        return 

    YB = [month, day, year]

    # Use monadic operations to calculate Pease Number
    PN = pease_monadic(YB)
    print(f"Your Pease Number is: {PN}")
    print(f"Does {year} converge to 1 under Collatz? {collatz_detection(year)}") # (refer to Extra Credit 2#)

def recursive_loop():   # Allows rerunning the program after calculating a Pease Number
    main()
    again = input("Compute another Pease Number? (y/n): ").strip().lower()
    if again in ("y", "yes"):
        recursive_loop()
    if again in ("n", "no"):
        print("Goodbye!")
        return

if __name__ == "__main__":
    recursive_loop()
