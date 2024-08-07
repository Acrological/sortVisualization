from fastapi import FastAPI
from pydantic import BaseModel
import math

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
        elif l >= len(arr) / 2 :
            logNum[step] = 'right half'
        else:
            logNum[step] = 'full array'
        logArray[step] = [step]
        n1 = m - l + 1
        n2 = r - m
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
        
        compar1 = f"left array: {L}, right array: {R}"
        logArray[step].append(compar1)
        while i < n1 and j < n2:
            compar2 = f"compare {L[i]} vs {R[j]}"
            logArray[step].append(compar2)
            if L[i] <= R[j]:
                arr[k] = L[i]
                i += 1
            else:
                arr[k] = R[j]
                j += 1
            k += 1
        
        # Copy the remaining elements of L[], if there
        # are any
        
        while i < n1:
            arr[k] = L[i]
            i += 1
            k += 1
        
        # Copy the remaining elements of R[], if there
        # are any
        
        while j < n2:
            arr[k] = R[j]
            j += 1
            k += 1
    
        step += 1
    # l is for left index and r is right index of the
    # sub-array of arr to be sorted
    
    
    def mergeSort(arr, l, r):
        if l < r:
    
            # Same as (l+r)//2, but avoids overflow for
            # large l and h
            m = l+(r-l)//2
    
            # Sort first and second halves
            mergeSort(arr, l, m)
            mergeSort(arr, m+1, r)
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
    step = 1
    quick_log = {}
    def partition(array, low, high):
        nonlocal step
        quick_log[step] = [step]
        quick_log[step].append(f'array low: {low}, high: {high}')
    # choose the rightmost element as pivot
        pivot = array[high]
        quick_log[step].append(f'starting pivot value: {pivot} , index {high}')
        # pointer for greater element
        i = low - 1
    
        # traverse through all elements
        # compare each element with pivot
        for j in range(low, high):
            quick_log[step].append(f'{array[j]} vs {pivot}')
            if array[j] <= pivot:
    
                # If element smaller than pivot is found
                # swap it with the greater element pointed by i
                i = i + 1
                quick_log[step].append(f'swapping elements {array[i]}(index {i}) and {array[j]}(index {j})')
                # Swapping element at i with element at j
                (array[i], array[j]) = (array[j], array[i])
    
        # Swap the pivot element with the greater element specified by i
        quick_log[step].append(f'finished loop, swapping pivot, swapping places from {array[high]} to {array[i+1]}')
        (array[i + 1], array[high]) = (array[high], array[i + 1])
        step += 1
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
    return {"og_array":ogarr,"sorted_array": arrays.og_array,"steps":quick_log}
