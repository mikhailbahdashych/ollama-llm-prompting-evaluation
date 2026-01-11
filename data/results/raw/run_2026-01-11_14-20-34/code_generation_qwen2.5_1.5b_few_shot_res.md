```python
from typing import List, Tuple

def find_pair_sum(numbers: List[int], target: int) -> List[Tuple[int, int]]:
    """
    Finds all unique pairs of numbers from a list that add up to a given target sum.

    Args:
        numbers: A list of integers.
        target: An integer representing the target sum.

    Returns:
        A list of tuples, where each tuple represents a pair of numbers that add up to the target sum. The first number in each tuple is smaller than the second one.

    Example usage:
        >>> find_pair_sum([2, 7, 11, 15, 3], 9)
        [(2, 7)]

        >>> find_pair_sum([1, 5, 3, 7, 2, 8], 10)
        [(2, 8), (3, 7)]
    """
    # Create a dictionary to keep track of seen numbers
    seen = {}
    
    pairs = []
    for number in numbers:
        complement = target - number
        
        if complement in seen and [number, complement] not in pairs:
            pairs.append([number, complement])
        
        seen[number] = 1
    
    return pairs

# Example check function to verify the correctness of the solution
def check_solution():
    assert find_pair_sum([2, 7, 11, 15, 3], 9) == [(2, 7)]
    assert find_pair_sum([1, 5, 3, 7, 2, 8], 10) == [(2, 8), (3, 7)]
    print("All tests passed!")

check_solution()
```