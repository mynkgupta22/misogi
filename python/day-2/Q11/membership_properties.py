fruits_list = ["apple", "banana", "orange", "apple", "grape"]

fruits_tuple = ("apple", "banana", "orange")

fruits_set = {"apple", "banana", "orange", "grape"}

fruits_dict = {"apple": 5, "banana": 3, "orange": 8, "grape": 2}


# Check for Membership
# Test whether "apple" is present in each data structure.
print( "apple" in fruits_list)
print("apple" in fruits_tuple)
print("apple" in fruits_set)
print("apple" in fruits_dict)


# Find Length
# Display the number of elements in each structure using len().
print(len(fruits_list))
print(len(fruits_dict))
print(len(fruits_set))
print(len(fruits_tuple))




# Iterate and Print Elements
# Loop through each structure and print its contents.
print(item for item in fruits_list)
print(item for item in fruits_tuple)




# Compare Membership Testing Performance
# Briefly explain which data structures are more efficient for membership checks and why.
def membership_performance():
    """
    Membership testing performance:
    - Lists: O(n) time complexity, as it requires scanning through each element.
    - Tuples: O(n) time complexity, similar to lists.
    - Sets: O(1) average time complexity due to hash table implementation, making it the most efficient for membership checks.
    - Dictionaries: O(1) average time complexity for checking keys, also efficient.
    """
    return "Sets and dictionaries are more efficient for membership checks due to their average O(1) time complexity."





# Demonstrate Different Iteration Patterns
# Use appropriate iteration patterns (e.g., for item in set, for key in dict, etc.) to traverse each structure effectively.
def iterate_structures():
    print("Iterating through List:")
    for item in fruits_list:
        print(item)
    print("Iterating through Tuple:")
    for item in fruits_tuple:
        print(item)
    print("Iterating through Set:")
    for item in fruits_set:
        print(item)
    print("Iterating through Dictionary:")
    for key, value in fruits_dict.items():
        print(f"{key}: {value}")            
            




