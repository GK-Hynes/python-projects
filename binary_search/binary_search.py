import random
import time

# Essence of binary search:
# If you have a sorted list and you want to search this array for something,
# You could go through each item in the list and ask, is this equal to what we're looking for?
# But we can make this *faster* by leveraging the fact that our array is sorted!
# Binary search ~ O(log(n)), naive search ~ O(n)

# In these two examples, l is a list in ascending order, and target is something that we're looking for.
# Return -1 if not found

# A naive search scans every element in a list and checks if they match the target.
# If yes, return the index
# If no, return -1
def naive_search(l, target):
    for i in range(len(l)):
        if l[i] == target:
            return i
    return -1

# Binary search takes advantage of the fact that the list is sorted
def binary_search(l, target, low=None, high=None):
    if low is None:
        low = 0
    if high is None:
        high = len(l) - 1
    
    if high < low:
        return -1

    midpoint = (low + high) // 2

    # We'll check if l[midpoint] == target, and if not, we can find out if target will be to the left or right of midpoint
    # We know everything to the left of midpoint is smaller than the midpoint and everything to the right is larger
    if l[midpoint] == target:
        return midpoint
    elif target < l[midpoint]:
        return binary_search(l, target, low, midpoint - 1)
    else:
        # Target > l[midpoint]
        return binary_search(l, target, midpoint + 1, high)

if __name__ == "__main__":
    l = [1,3,5,10,12]
    target = 10
    print(naive_search(l, target))
    print(binary_search(l, target))

    # Build a sorted list of length 10000
    length = 10000
    sorted_list = set()
    while len(sorted_list) < length:
        sorted_list.add(random.randint(-3*length, 3*length))
    sorted_list = sorted(list(sorted_list))

    start = time.time()
    for target in sorted_list:
        naive_search(sorted_list, target)
    end = time.time()
    print("Naive search time: ", (end - start), "seconds")

    start = time.time()
    for target in sorted_list:
        binary_search(sorted_list, target)
    end = time.time()
    print("Binary search time: ", (end - start), "seconds")