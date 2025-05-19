def bubble_sort(arr, bar_color, bar_highlight, order="Ascending", log_callback=None):
    comparisons = swaps = accesses = 0
    n = len(arr)
    for i in range(n):
        for j in range(n - i - 1):
            comparisons += 1
            accesses += 2  # Two array accesses for comparison
            yield arr, [bar_highlight if x == j or x == j+1 else bar_color for x in range(n)], comparisons, swaps, accesses
            if (order == "Ascending" and arr[j] > arr[j + 1]) or (order == "Descending" and arr[j] < arr[j + 1]):
                if log_callback:
                    log_callback(f"Swapping {arr[j]} (index {j}) with {arr[j+1]} (index {j+1})")
                swaps += 1
                accesses += 2  # Two more accesses for swap
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                yield arr, [bar_highlight if x == j or x == j+1 else bar_color for x in range(n)], comparisons, swaps, accesses
    yield arr, [bar_color for _ in range(n)], comparisons, swaps, accesses

def insertion_sort(arr, bar_color, bar_highlight, order="Ascending", log_callback=None):
    comparisons = swaps = accesses = 0
    n = len(arr)
    for i in range(1, n):
        key = arr[i]
        accesses += 1
        j = i - 1
        while j >= 0:
            comparisons += 1
            accesses += 1
            if (order == "Ascending" and arr[j] > key) or (order == "Descending" and arr[j] < key):
                if log_callback:
                    log_callback(f"Moving {arr[j]} (index {j}) to index {j+1}")
                swaps += 1
                accesses += 1
                arr[j + 1] = arr[j]
                j -= 1
                yield arr, [bar_highlight if x == j+1 or x == i else bar_color for x in range(n)], comparisons, swaps, accesses
            else:
                break
        if j + 1 != i:
            if log_callback:
                log_callback(f"Placing {key} at index {j+1}")
            accesses += 1
            arr[j + 1] = key
            yield arr, [bar_highlight if x == j+1 else bar_color for x in range(n)], comparisons, swaps, accesses
    yield arr, [bar_color for _ in range(n)], comparisons, swaps, accesses

def selection_sort(arr, bar_color, bar_highlight, order="Ascending", log_callback=None):
    comparisons = swaps = accesses = 0
    n = len(arr)
    for i in range(n):
        extreme_idx = i
        for j in range(i + 1, n):
            comparisons += 1
            accesses += 2  # Two accesses for comparison
            yield arr, [bar_highlight if x == j or x == extreme_idx else bar_color for x in range(n)], comparisons, swaps, accesses
            if (order == "Ascending" and arr[j] < arr[extreme_idx]) or (order == "Descending" and arr[j] > arr[extreme_idx]):
                extreme_idx = j
        if i != extreme_idx:
            if log_callback:
                log_callback(f"Swapping {arr[i]} (index {i}) with {arr[extreme_idx]} (index {extreme_idx})")
            swaps += 1
            accesses += 2  # Two accesses for swap
            arr[i], arr[extreme_idx] = arr[extreme_idx], arr[i]
            yield arr, [bar_highlight if x == i or x == extreme_idx else bar_color for x in range(n)], comparisons, swaps, accesses
    yield arr, [bar_color for _ in range(n)], comparisons, swaps, accesses

def merge_sort(arr, bar_color, bar_highlight, order="Ascending", log_callback=None):
    yield from _merge_sort(arr, 0, len(arr)-1, bar_color, bar_highlight, order, log_callback)

def _merge_sort(arr, l, r, bar_color, bar_highlight, order, log_callback=None):
    comparisons = swaps = accesses = 0
    if l < r:
        m = (l + r) // 2
        yield from _merge_sort(arr, l, m, bar_color, bar_highlight, order, log_callback)
        yield from _merge_sort(arr, m + 1, r, bar_color, bar_highlight, order, log_callback)
        yield from _merge(arr, l, m, r, bar_color, bar_highlight, order, log_callback)
    yield arr, [bar_color for _ in range(len(arr))], comparisons, swaps, accesses

def _merge(arr, l, m, r, bar_color, bar_highlight, order, log_callback=None):
    comparisons = swaps = accesses = 0
    left = arr[l:m+1]
    right = arr[m+1:r+1]
    accesses += (m - l + 1) + (r - m)
    i = j = 0
    for k in range(l, r+1):
        if i < len(left) and (j >= len(right) or 
            (order == "Ascending" and left[i] <= right[j]) or 
            (order == "Descending" and left[i] >= right[j])):
            comparisons += 1
            accesses += 1
            arr[k] = left[i]
            i += 1
        else:
            comparisons += 1
            accesses += 1
            arr[k] = right[j]
            j += 1
        swaps += 1
        if log_callback:
            log_callback(f"Placing {arr[k]} at index {k}")
        yield arr, [bar_highlight if x == k else bar_color for x in range(len(arr))], comparisons, swaps, accesses

def quick_sort(arr, bar_color, bar_highlight, order="Ascending", log_callback=None):
    yield from _quick_sort(arr, 0, len(arr)-1, bar_color, bar_highlight, order, log_callback)

def _quick_sort(arr, low, high, bar_color, bar_highlight, order, log_callback=None):
    comparisons = swaps = accesses = 0
    if low < high:
        pi, arr, comp, sw, acc = _partition(arr, low, high, bar_color, bar_highlight, order, log_callback)
        comparisons += comp
        swaps += sw
        accesses += acc
        yield arr, [bar_highlight if x == pi else bar_color for x in range(len(arr))], comparisons, swaps, accesses
        yield from _quick_sort(arr, low, pi - 1, bar_color, bar_highlight, order, log_callback)
        yield from _quick_sort(arr, pi + 1, high, bar_color, bar_highlight, order, log_callback)
    yield arr, [bar_color for _ in range(len(arr))], comparisons, swaps, accesses

def _partition(arr, low, high, bar_color, bar_highlight, order, log_callback=None):
    comparisons = swaps = accesses = 0
    pivot = arr[high]
    accesses += 1
    i = low - 1
    for j in range(low, high):
        comparisons += 1
        accesses += 1
        if (order == "Ascending" and arr[j] < pivot) or (order == "Descending" and arr[j] > pivot):
            i += 1
            if log_callback:
                log_callback(f"Swapping {arr[i]} (index {i}) with {arr[j]} (index {j})")
            swaps += 1
            accesses += 2
            arr[i], arr[j] = arr[j], arr[i]
            yield arr, [bar_highlight if x == i or x == j else bar_color for x in range(len(arr))], comparisons, swaps, accesses
    if log_callback:
        log_callback(f"Swapping pivot {arr[i+1]} (index {i+1}) with {arr[high]} (index {high})")
    swaps += 1
    accesses += 2
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1, arr, comparisons, swaps, accesses

def heap_sort(arr, bar_color, bar_highlight, order="Ascending", log_callback=None):
    comparisons = swaps = accesses = 0
    n = len(arr)

    def heapify(n, i):
        nonlocal comparisons, swaps, accesses
        extreme = i
        l = 2 * i + 1
        r = 2 * i + 2

        if l < n:
            comparisons += 1
            accesses += 2
            if (order == "Ascending" and arr[l] > arr[extreme]) or (order == "Descending" and arr[l] < arr[extreme]):
                extreme = l
        if r < n:
            comparisons += 1
            accesses += 2
            if (order == "Ascending" and arr[r] > arr[extreme]) or (order == "Descending" and arr[r] < arr[extreme]):
                extreme = r

        if extreme != i:
            if log_callback:
                log_callback(f"Swapping {arr[i]} (index {i}) with {arr[extreme]} (index {extreme})")
            swaps += 1
            accesses += 2
            arr[i], arr[extreme] = arr[extreme], arr[i]
            yield arr, [bar_highlight if x == i or x == extreme else bar_color for x in range(len(arr))], comparisons, swaps, accesses
            yield from heapify(n, extreme)

    for i in range(n // 2 - 1, -1, -1):
        yield from heapify(n, i)

    for i in range(n - 1, 0, -1):
        if log_callback:
            log_callback(f"Swapping root {arr[0]} (index 0) with {arr[i]} (index {i})")
        swaps += 1
        accesses += 2
        arr[i], arr[0] = arr[0], arr[i]
        yield arr, [bar_highlight if x == i or x == 0 else bar_color for x in range(len(arr))], comparisons, swaps, accesses
        yield from heapify(i, 0)

    yield arr, [bar_color for _ in range(len(arr))], comparisons, swaps, accesses

def shell_sort(arr, bar_color, bar_highlight, order="Ascending", log_callback=None):
    comparisons = swaps = accesses = 0
    n = len(arr)
    gap = n // 2

    while gap > 0:
        for i in range(gap, n):
            temp = arr[i]
            accesses += 1
            j = i
            while j >= gap:
                comparisons += 1
                accesses += 1
                if (order == "Ascending" and arr[j - gap] > temp) or (order == "Descending" and arr[j - gap] < temp):
                    if log_callback:
                        log_callback(f"Moving {arr[j - gap]} (index {j-gap}) to index {j}")
                    swaps += 1
                    accesses += 1
                    arr[j] = arr[j - gap]
                    yield arr, [bar_highlight if x == j or x == j-gap else bar_color for x in range(len(arr))], comparisons, swaps, accesses
                    j -= gap
                else:
                    break
            if j != i:
                if log_callback:
                    log_callback(f"Placing {temp} at index {j}")
                accesses += 1
                arr[j] = temp
                yield arr, [bar_highlight if x == j else bar_color for x in range(len(arr))], comparisons, swaps, accesses
        gap //= 2

    yield arr, [bar_color for _ in range(len(arr))], comparisons, swaps, accesses

def counting_sort(arr, bar_color, bar_highlight, order="Ascending", log_callback=None):
    comparisons = swaps = accesses = 0
    max_val = max(arr)
    min_val = min(arr)
    range_val = max_val - min_val + 1
    count = [0] * range_val
    output = [0] * len(arr)
    
    # Count occurrences
    for num in arr:
        count[num - min_val] += 1
        accesses += 1
        yield arr, [bar_highlight if x == num else bar_color for x in range(len(arr))], comparisons, swaps, accesses
    
    # Modify count to store cumulative sum
    for i in range(1, len(count)):
        count[i] += count[i-1]
        yield arr, [bar_color for _ in range(len(arr))], comparisons, swaps, accesses
    
    # Build output array
    for num in reversed(arr) if order == "Ascending" else arr:
        output[count[num - min_val] - 1] = num
        count[num - min_val] -= 1
        accesses += 1
        swaps += 1
        yield output.copy(), [bar_highlight if x == num else bar_color for x in range(len(output))], comparisons, swaps, accesses
    
    # Final yield
    yield output, [bar_color for _ in range(len(output))], comparisons, swaps, accesses

def radix_sort(arr, bar_color, bar_highlight, order="Ascending", log_callback=None):
    comparisons = swaps = accesses = 0
    max_num = max(arr)
    exp = 1
    
    while max_num // exp > 0:
        output = [0] * len(arr)
        count = [0] * 10
        
        for num in arr:
            index = (num // exp) % 10
            count[index] += 1
            comparisons += 1
            accesses += 1
            yield arr, [bar_highlight if x == num else bar_color for x in range(len(arr))], comparisons, swaps, accesses
        
        for i in range(1, 10):
            count[i] += count[i-1]
            yield arr, [bar_color for _ in range(len(arr))], comparisons, swaps, accesses
        
        for num in reversed(arr) if order == "Ascending" else arr:
            index = (num // exp) % 10
            output[count[index] - 1] = num
            count[index] -= 1
            swaps += 1
            accesses += 1
            yield output.copy(), [bar_highlight if x == num else bar_color for x in range(len(output))], comparisons, swaps, accesses
        
        arr = output.copy()
        exp *= 10
    
    yield arr, [bar_color for _ in range(len(arr))], comparisons, swaps, accesses