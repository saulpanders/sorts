# sorts.py
# Paul Sanders
# 1/10/17

## Designed to sort a list of unsorted number values (currently non-negative ints), where the input is provided via a text file.
## First line of the file tells the program which sort it should use (this is subject to change w revisions..)
## The goal is to create/maintain an assortment of sorting algorithms to familiarize myself with both python and various algorithms
## Each algorithm will have its own def statement(s) in a seperate section to improve code modularity & readability
## I chose python bc its close to pseudocode, and is therefore useful for algorithms (less pedantic syntax)
##
##Added the ability to time algorithms to compare asymptotic runtimes
##
##Most of the peusdocode came from reading the wikipedia entries for each sort. Cormen (Intro algorithms) helped too
##
##TO DO:    i) comment code better - GOOD ENOUGH (1/13/17)
##          ii) create a sort handler method (i.e. takes in sort_type and selects appropriate sort)- DONE (mostly)
##          iii) re-write recursion to iterative
##          iv) still to add: comb sort, shell sort, cyclesort, radix/counting, time controls
import random
import math
from timeit import default_timer as timer

def main():
    #file I/O
    file = open("in2.txt", "r")
    sort_type = file.readline()
    print(sort_type)
    unsorted_list = []
    for line in file:
        #if statement to check that line is not blank
        if line.split():
            #allow the user to input more than one number per line (allows greater flexibility)
            if len(line)>1:
                sub_line = line.split()
                sub_line = [int(x) for x in sub_line]
                unsorted_list = unsorted_list+ sub_line          #Funny that '+' can concatenate whole lists!
            #otherwise strip newline and add it to the list
            else:
                unsorted_list.append(int(line.rstrip('\n')))

    print (unsorted_list)
    ##time comparison of sorts
    start = timer()

    sorted_list = cyclesort(unsorted_list)

    end = timer()
    print(end - start)
    print (sorted_list)

    file.close()
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#sort handler
def sort_handler(sort_type, list):
    sorted_list = []
    size = len(list)
    if (sort_type == "bubblesort"):
        sorted_list = bubblesort(list)

    if (sort_type == "insertionsort"):
        sorted_list = insertionsort(list)

    if (sort_type == "mergesort"):
        sorted_list = mergesort(list)

    if (sort_type == "quicksort"):
        sorted_list = quicksort(list, 0, size-1)

    if (sort_type == "quicksort_r"):
        sorted_list = quicksort_r(list, 0, size -1)

    if (sort_type == "selectionsort"):
        sorted_list = selectionsort(list)

    if (sort_type == "heapsort"):
        sorted_list = heapsort(list)

    if (sort_type == "countingsort"):
        sorted_list = countingsort(list)

    if (sort_type == "radixsort"):
        print("tbd")

    if (sort_type == "bogosort"):
        sorted_list = bogosort(list)

    if (sort_type == "cyclesort"):
        sorted_list =   cyclesort(list)

    return sorted_list

###################################################################
#Bubblesort ( runs in O(n^2))
# Donald Knuth's "favorite", if you like permutations then this sort is the OG
# advantages of being in place, not much else (not adaptive)

def bubblesort(list):
    n = len(list)
    for i in range (n):
        for j in range (0, n-i-1):
            if list[j]> list[j+1]:
                list[j], list[j+1] = list[j+1], list[j]
    return list

##################################################################
#Insertionsort; runs in O(n^2)
# good for online uses and short lists, also in place

def insertionsort(list):
    size = len(list)
    i=1
    while i<size:
        j=i
        while j>0 and list[j-1]>list[j]:
            list[j-1], list[j]= list[j], list[j-1]
            j=j-1
        i=i+1
    return list

##################################################################
#Mergesort (runs in O(nlogn))-> iterative version; optimal for a comparison sort
# in place (O(1) additional space complexity)
# I like this version better, it is less code & still pretty clean to read
# also doesnt use the stack

def mergesort(list):
    size = len (list)
    step = 1
    while step<= len(list):
        i = 0
        for i in range (0, len(list), 2*step):
            left = i
            right = min (len(list), i + 2*step)
            mid = i + step
            j, k = left, mid
            while j< mid and k <right:
                if list[j]< list[k]:
                    j+=1
                else:
                    tmp = list[k]
                    list[j+ 1: k+ 1] = list[j:k]
                    list[j] = tmp
                    j, mid, k = j + 1, mid + 1, k + 1
        step*=2

    return  list

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#recursive mergesort (to contrast with above iterative)
#this version is not connected to the sorting controller, bc its objectively worse (in python) due to recursion constraints

def mergesort_rec (list):
    if len(list)<=1:
        return list
    left = []
    right = []
    for x in list:
        if list.index(x)< len(list)/2:
            left.append(x)
        else:
            right.append(x)
    left = mergesort(left)
    right = mergesort(right)
    return merge(left, right)

def merge(left, right):
    result = []
    while left and right:
        if left[0]<= right[0]:
            result.append(left[0])
            left = left[1:]
        else:
            result.append(right[0])
            right = right[1:]

    while left:
        result.append(left[0])
        left = left[1:]

    while right:
        result.append(right[0])
        right = right[1:]

    return result

###################################################################
#quicksort: naive partition; expected O(nlogn) worst case O(n^2)
# sorting is not a popularity contest, but if it were quicksort would win
# iterative version -> uses a user defined stack instead of runtime stack

def quicksort(list, low, high):
    height = high-low + 1
    stack = [0]*(height)
    top, l, h = 0,0,0
    stack[top] = low
    top+=1
    stack[top] = high

    while top >=0:
        h= stack[top]
        top-=1
        l = stack[top]
        top -=1

        p = partition(list, l, h)

        if p-1>l:
            top+=1
            stack[top] = l
            top+=1
            stack[top] = p-1
        if p+1< h:
            top+=1
            stack[top] = p+1
            top+=1
            stack[top] = h
    return  list

def partition(list, low, high):
    pivot = list[high]
    i = low-1
    for j in range(low, high):
        if list[j]<=pivot:
            i=i+1
            list[i], list[j] =list[j], list[i]
    if list[high]< list[i+1]:
        list[i+1], list[high] = list[high], list[i+1]
    return i+1

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#quicksort with random pivot, still same expected/avg time complexity O(nlogn) (and its a cool use of randomness)
#in some cases may be more practical than naive, medians of medians

def quicksort_r(list, low, high):
    height = high - low + 1
    stack = [0] * (height)
    top, l, h = 0, 0, 0
    stack[top] = low
    top += 1
    stack[top] = high

    while top >= 0:
        h = stack[top]
        top -= 1
        l = stack[top]
        top -= 1

        p = partition(list, l, h)

        if p - 1 > l:
            top += 1
            stack[top] = l
            top += 1
            stack[top] = p - 1
        if p + 1 < h:
            top += 1
            stack[top] = p + 1
            top += 1
            stack[top] = h
    return list

def partition_r(list, low, high):
    index = random.randint(low, high)
    list[index], list[high] = list[high], list[index]
    pivot = list[high]
    i = low-1
    for j in range(low, high):
        if list[j]<=pivot:
            i=i+1
            list[i], list[j] =list[j], list[i]
    if list[high]< list[i+1]:
        list[i+1], list[high] = list[high], list[i+1]
    return i+1

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# quicksort with median of medians pivot algorithm -----> still TODO
# theoretically "optimal", but the recursion makes it often worse in practice
# added this version for completeness, but didn't hook it into the controller bc recursion sucks in python (it needs quickselect)
# warning: if you use this version, keep the list very small (around 10 elements)

# quicksort, the basic recursive version. it's not used bc it will blow out the stack when |list|>16 but its still nice to see
def quicksort_rec(list, low, high):
    if low < high:
        p =partition_m(list, low, high)
        quicksort_rec(list, low, p-1)
        quicksort_rec(list, p+1,high)
    return list

def partition_m(list, low, high):
    print("tbd")



###################################################################
# selectionsort; runs in O(n^2) and performs worst on avg than bubblesort
# easy to implement seems to be only positive about this sort, also its in place

def selectionsort(list):
    size = len(list)
    for j in range (0, size-1):
        min_index = j
        for i in range(j+1, size ):
            if list[i]< list[min_index]:
                min_index = i
        if min_index != j:
            list[min_index], list[j] = list[j], list[min_index]
    return list

###################################################################
# heapsort; runs in time O(nlogn) so technically optimal comparison sort
# resource intensive on the space side, but still pretty  cool
# note that this is not a stable sort, but it is "in place" (not counting use of stack)
# also, due to the external function calls (and thus use of runtime stack) it may be slower in practice than other O(nlogn) sorts
# above situation may be remedied by function inlining where possible

def heapsort(list):
    count = len(list)
    heapify(list, count)
    end = count -1
    while end>0:
        list[0], list[end] = list[end], list[0]
        end-=1
        sift_down(list, 0, end)
    return list

def heapify(list, count):
    start = i_parent(count-1)
    while start >= 0:
        sift_down(list, start, count-1)
        start -=1

def sift_down(list, start, end):
    root = start
    while i_left_child(root)<= end:
        child = i_left_child(root)
        swap = root
        if list[swap]< list[child]:
            swap = child
        if child+1 <= end and list[swap]<list[child+1]:
            swap = child+1
        if swap == root:
            return
        else:
            list[root], list[swap] = list[swap], list[root]
            root = swap

def i_parent(i):
    return math.floor((i - 1) / 2)

def i_left_child(i):
    return 2 * i + 1

def i_right_child(i):
    return 2 * i + 2

###################################################################
#countingsort; runs in time O(n+k) where k= max(list)
#if k<<n this is basically linear (O(n)), n<<k don't use this sort
#only works well for non-negtative integers, so its a little limimted
#this stort is stable (so its useful for implementing radix sort)
def countingsort(list):
    k  = max(list)
    total = 0
    result = [0]*len(list)
    count= [0] *(k+1)
    for x in list:
        count[x] = count[x]+1

    for i in range (k+1):
        old_count = count[i]
        count[i] = total
        total +=old_count

    for x in list:
        result[count[x]] = x
        count[x]+=1
    return result

###################################################################
# radixsort (in base 10); runs in time O(d*(n+b)) where d:= digits in input, n:= input size, b:= base of representation
# better to use radix sort over counting sort when you have integers of a range >> n. In this case we expect ~ O(n) behavior
# we modify the above countingsort code to take in a base argument as a parameter
# note that the added space complexity (due to counting sort implemented as a subroutine) may be a turnoff, but it is stable
# this algorithm also has a cool history, radix sort has its roots in old mechanical calculators


###################################################################
# cyclesort; runs in O(n^2).. no exeptions
# really you should just use bubble/insertion if you are committed to being this slow
##needs fixing---- currently i think it gets stuck in an infinite loop

def cyclesort(list):
    size = len(list)
    for c_0 in range (0, size-1):
        item = list[c_0]
        index = c_0
        for  i in range ( c_0 +1, size):
            if list[i]< item:
                index+=1
        while item == list[index]:
            index+=1
            print(list)
            list[index], item = item, list[index]

        while index!=c_0:
            index=c_0
            for i in range (c_0+1, size):
                index+=1
            while item == list[index]:
                index += 1
                list[index], item = item, list[index]
    return list
###################################################################
# bogosort; runs on average in O((n+1)!).... yup that's a factorial
# If you're a gambler how can you not love bogo?!

def bogosort (list):
    while not is_sorted(list):
        random.shuffle(list)
    return list

def is_sorted(list):
    if len(list)< 2:
        return True
    for i in range(0, len(list)-1):
        if list[i]> list[i+1]:
            return False
    return True

###################################################################
# stoogesort; runs in O(n^(log3/log1.5)) ~ O(n^2.7) so its a trash tier sort
# also recursive so keep the lists small (~ 10 elements)
# for reasons above it is not hooked into the controller (but it was a fun excercise)
# idea is recursively sort first 2/3's, then last 2/3's, then first 2/3's again
# nevertheless, larry curly & moe would still be so proud

def stoogesort(list, low, high):
    if list[low]> list[high]:
        list[low], list[high] = list[high], list[low]
    if (high- low ) > 1:
        t = (high-low +1)//3
        stoogesort(list, low, high-t)
        stoogesort(list, low+t, high)
        stoogesort(list, low, high-t)

    return list

###################################################################
##the call to main
main()