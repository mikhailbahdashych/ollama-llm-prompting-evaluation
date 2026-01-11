```python
from typing import List, Tuple

def find_pair_sum(numbers: List[int], target: int) -> List[Tuple[int, int]]:
    """
    Finds all unique pairs of numbers from the list that add up to the given target sum.
    
    Parameters:
    - numbers (List[int]): The list of integers to search through.
    - target (int): The target sum for the pairs.
    
    Returns:
    - List[Tuple[int, int]]: A list of tuples representing unique pairs that add up to the target sum.
    
    Example usage:
    >>> find_pair_sum([2, 7, 11, 15, 3], 9)
    [(2, 7)]
    >>> find_pair_sum([1, 5, 3, 7, 2, 8], 10)
    [(2, 8), (3, 7)]
    """
    seen = {}
    pairs = set()
    
    for number in numbers:
        complement = target - number
        if complement in seen:
            pairs.add((min(number, complement), max(number, complement)))
        
        seen[number] = True
    
    return list(pairs)

# Example check function to verify the correctness of the solution
def check_solution():
    assert find_pair_sum([2, 7, 11, 15, 3], 9) == [(2, 7)], "Test case 1 failed"
    assert find_pair_sum([1, 5, 3, 7, 2, 8], 10) == [(2, 8), (3, 7)], "Test case 2 failed"
    print("All test cases passed!")

check_solution()
```

This solution defines the `find_pair_sum` function that takes a list of integers and a target sum as inputs. It uses two sets: one to keep track of numbers seen so far (`seen`) and another to store unique pairs found (`pairs`). As it iterates through the list, it checks if the complement (to reach the target sum) of each number has already been seen. If so, it adds the pair to `pairs` and ensures no duplicates by converting the tuple to a set before adding it back into `pairs`. Finally, it returns the list of unique pairs.