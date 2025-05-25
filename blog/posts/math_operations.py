def add(a: float, b: float) -> float:
    """Add two numbers."""
    return a + b

def subtract(a: float, b: float) -> float:
    """Subtract b from a."""
    return a - b

def divide(a: float, b: float) -> float:
    """Divide a by b."""
    return a / b

def multiply(a: float, b: float) -> float:
    """Multiply a and b."""
    return a * b

def factorial(n: int) -> int:
    """Calculate the factorial of n."""
    if n == 0 or n == 1:
        return 1
    else:
        return n * factorial(n-1)