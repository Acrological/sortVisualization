from fastapi import FastAPI
from pydantic import BaseModel
import math

#fastapi dev main.py
class ArrayObj(BaseModel):
    og_array: list[int]

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/bubble")
def get_bubblesort(arrays: ArrayObj):
    ogarr = [index for index in arrays.og_array]
    n = len(arrays.og_array)
    arr = arrays.og_array
    swapped_num = 0
    comparisons = 0
    bubble_log= {}
    step = 1
    # optimize code, so if the array is already sorted, it doesn't need
    # to go through the entire process
    # Traverse through all array elements
    for i in range(n-1):

        # range(n) also work but outer loop will
        # repeat one time more than needed.
        # Last i elements are already in place
        swapped = False
        for j in range(0, n-i-1):

            # traverse the array from 0 to n-i-1
            # Swap if the element found is greater
            # than the next element
            comparisons += 1
            compar = (f'compare ',arr[j],' vs ',arr[j+1])
            bubble_log[step] = [compar]
            if arr[j] > arr[j + 1]:
                swapped = True
                swapped_num += 1
                swap = f'{arr[j]} swapped with {arr[j+1]}'
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                bubble_log[step].append(swapped)
                bubble_log[step].append(swap)
                print(arr)
            step += 1
        if not swapped:
            # if we haven't needed to make a single swap, we
            # can just exit the main loop.
            return {"org_array": ogarr,"sorted_array": arr,"actual":swapped_num,"theoretical":(n*n-1),"comparisons":comparisons,"steps":bubble_log} 
        
    return {"org_array": ogarr,"sorted_array": arr,"actual":swapped_num,"theoretical":(n*n),"comparisons":comparisons,"steps":bubble_log}

@app.post("/merge")
def get_mergesort(arrays:ArrayObj):
    logArray = {}
    logNum = {}
    step = 1
    def merge(arr, l, m, r):
        nonlocal step
        if l < len(arr) / 2 and r != len(arr) -1 :
            logNum[step] = 'left half'
            print('left half')
        elif l >= len(arr) / 2 :
            logNum[step] = 'right half'
            print('right half')
        else:
            print(l,m,r)
            logNum[step] = 'full array'
            print('full array')
        logArray[step] = [step]
        n1 = m - l + 1
        n2 = r - m
        print('n1: ',n1,' n2: ',n2)
        # create temp arrays
        L = [0] * (n1)
        R = [0] * (n2)
    
        # Copy data to temp arrays L[] and R[]
        for i in range(0, n1):
            L[i] = arr[l + i]
    
        for j in range(0, n2):
            R[j] = arr[m + 1 + j]
    
        # Merge the temp arrays back into arr[l..r]
        i = 0     # Initial index of first subarray
        j = 0     # Initial index of second subarray
        k = l     # Initial index of merged subarray
        print('left array: ',L,' right array: ',R)
        compar1 = f"left array: {L}, right array: {R}"
        logArray[step].append(compar1)
        while i < n1 and j < n2:
            print('compare',L[i],' vs ',R[j])
            compar2 = f"compare {L[i]} vs {R[j]}"
            logArray[step].append(compar2)
            if L[i] <= R[j]:
                arr[k] = L[i]
                i += 1
            else:
                arr[k] = R[j]
                j += 1
            print(f'new index {k} value of {arr[k]}')
            k += 1
        print('current state of merge sort without checking remainders')
        print(arr)
        # Copy the remaining elements of L[], if there
        # are any
        print(f'current k:{k} and i:{i}')
        while i < n1:
            arr[k] = L[i]
            i += 1
            k += 1
        print('left array joined',arr)
        # Copy the remaining elements of R[], if there
        # are any
        print(f'current k:{k} and j:{j}')
        while j < n2:
            arr[k] = R[j]
            j += 1
            k += 1
        print('right array joined',arr)
        step += 1
    # l is for left index and r is right index of the
    # sub-array of arr to be sorted
    
    
    def mergeSort(arr, l, r):
        print('compare ',l , ' and ',r)
        if l < r:
    
            # Same as (l+r)//2, but avoids overflow for
            # large l and h
            m = l+(r-l)//2
    
            # Sort first and second halves
            print(f'split point for both arrays: index {m} which has a value of {arr[m]}\n(splits up to this value for the left array, over for the right)')
            mergeSort(arr, l, m)
            mergeSort(arr, m+1, r)
            print('reached merge function')
            merge(arr, l, m, r)
        
    
 
    # Driver code to test above
    arr = arrays.og_array
    ogarr = [index for index in arrays.og_array]
    n = len(arr)
    
    mergeSort(arr, 0, n-1)
    # "comparions":(math.ciel(n*math.log2(n)-(n-1)))
    return {"og_array":ogarr,"sorted_array": arrays.og_array,'steps':logArray,'steps_detailed':logNum}
@app.post("/quick")
def get_quicksort(arrays:ArrayObj):
    def partition(array, low, high):
 
    # choose the rightmost element as pivot
        pivot = array[high]
    
        # pointer for greater element
        i = low - 1
    
        # traverse through all elements
        # compare each element with pivot
        for j in range(low, high):
            if array[j] <= pivot:
    
                # If element smaller than pivot is found
                # swap it with the greater element pointed by i
                i = i + 1
    
                # Swapping element at i with element at j
                (array[i], array[j]) = (array[j], array[i])
    
        # Swap the pivot element with the greater element specified by i
        (array[i + 1], array[high]) = (array[high], array[i + 1])
    
        # Return the position from where partition is done
        return i + 1
 
    # function to perform quicksort
 
 
    def quickSort(array, low, high):
        if low < high:
    
            # Find pivot element such that
            # element smaller than pivot are on the left
            # element greater than pivot are on the right
            pi = partition(array, low, high)
    
            # Recursive call on the left of pivot
            quickSort(array, low, pi - 1)
    
            # Recursive call on the right of pivot
            quickSort(array, pi + 1, high)
    
    
    data = arrays.og_array
    ogarr = [item for item in arrays.og_array]
    size = len(data)
    quickSort(data, 0, size - 1)
    return {"og_array":ogarr,"sorted_array": arrays.og_array,}
