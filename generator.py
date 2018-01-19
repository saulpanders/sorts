# generator.py
# Paul Sanders
# 1/13/117
#
## program that generates random integers & writes to a text file; to be used in conjunction with sorts.py
##we require the integers be non-negative so they can be compatible with any sort (e.g. counting, radix)

import random

def main():
    min_range= 0
    max_range = 100
    integers = []
    valid_sorts = [ "bubblesort", "insertionsort", "mergesort", "quicksort", "quicksort_r",
                    "selectionsort", "heapsort", "countingsort", "radixsort","cyclesort",
                    "bogosort"]

    file = open("example.txt", "w")

    print("Which type of sort do you want to use?")
    print("Options: bubblesort \n \t\t insertionsort \n \t\t mergesort \n \t\t quicksort \n \t\t quicksort_r (random pivot) "
          "\n \t\t selectionsort \n \t\t heapsort \n \t\t countingsort \n \t\t radixsort \n\t\t cyclesort \n \t\t bogosort")

    sort_type = input()
    while sort_type not in valid_sorts:
        print("Sorry, but you need to enter a sort from Options exactly as written")
        sort_type = input("Which type of sort do you want to use? ")

    count = input("How many randomly generated (non-negative) integers do you want? ")
    while not count.isdigit() or int(count) <=0:
        print("Count must be a positive integer")
        count = input("How many randomly generated (non-negative) integers do you want? ")

    max_range = input("What is the maximum range desired? ")
    while not max_range.isdigit() or int(max_range)<0 :
        print("Max range must be non-negative integer")
        max_range = input("What is the maximum range desired? ")

    for i in range (0, int(count)):
        integers.append( str(random.randint(min_range, int(max_range))))

    file.write(sort_type +"\n")
    for x in integers:
        file.write(x  +"\n")

    file.close()
main()