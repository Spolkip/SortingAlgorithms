def create_algorithm_info():
        return {
            "Bubble Sort": {
                "description": "Repeatedly steps through the list, compares adjacent elements and swaps them if in wrong order.",
                "pseudocode": """procedure bubbleSort(A : list)
        n = length(A)
        repeat
            swapped = false
            for i = 1 to n-1 do
                if A[i-1] > A[i] then
                    swap(A[i-1], A[i])
                    swapped = true
                end if
            end for
            n = n - 1
        until not swapped
    end procedure""",
                "complexity": "Time: O(n²)\nSpace: O(1)",
                "best_case": "O(n) - when array is already sorted",
                "worst_case": "O(n²) - when array is reverse sorted",
                "stable": True
            },
            "Insertion Sort": {
                "description": "Builds the final sorted array one item at a time by comparisons.",
                "pseudocode": """procedure insertionSort(A : list)
        for i = 1 to length(A)-1 do
            key = A[i]
            j = i - 1
            while j >= 0 and A[j] > key do
                A[j+1] = A[j]
                j = j - 1
            end while
            A[j+1] = key
        end for
    end procedure""",
                "complexity": "Time: O(n²)\nSpace: O(1)",
                "best_case": "O(n) - when array is already sorted",
                "worst_case": "O(n²) - when array is reverse sorted",
                "stable": True
            },
            "Selection Sort": {
                "description": "Repeatedly finds the minimum element from unsorted part and puts it at the beginning.",
                "pseudocode": """procedure selectionSort(A : list)
        for i = 0 to length(A)-1 do
            min_idx = i
            for j = i+1 to length(A)-1 do
                if A[j] < A[min_idx] then
                    min_idx = j
                end if
            end for
            swap(A[min_idx], A[i])
        end for
    end procedure""",
                "complexity": "Time: O(n²)\nSpace: O(1)",
                "best_case": "O(n²)",
                "worst_case": "O(n²)",
                "stable": False
            },
            "Merge Sort": {
                "description": "Divides the array into halves, sorts them, and then merges the sorted halves.",
                "pseudocode": """procedure mergeSort(A : list, left, right)
        if left < right then
            mid = (left + right) / 2
            mergeSort(A, left, mid)
            mergeSort(A, mid+1, right)
            merge(A, left, mid, right)
        end if
    end procedure

    procedure merge(A : list, left, mid, right)
        // Create temporary arrays and merge
    end procedure""",
                "complexity": "Time: O(n log n)\nSpace: O(n)",
                "best_case": "O(n log n)",
                "worst_case": "O(n log n)",
                "stable": True
            },
            "Quick Sort": {
                "description": "Picks a pivot element and partitions the array around the pivot.",
                "pseudocode": """procedure quickSort(A : list, low, high)
        if low < high then
            pi = partition(A, low, high)
            quickSort(A, low, pi-1)
            quickSort(A, pi+1, high)
        end if
    end procedure

    procedure partition(A : list, low, high)
        pivot = A[high]
        i = low - 1
        for j = low to high-1 do
            if A[j] < pivot then
                i = i + 1
                swap(A[i], A[j])
            end if
        end for
        swap(A[i+1], A[high])
        return i + 1
    end procedure""",
                "complexity": "Time: O(n log n) avg\nSpace: O(log n)",
                "best_case": "O(n log n)",
                "worst_case": "O(n²)",
                "stable": False
            },
            "Heap Sort": {
                "description": "Builds a heap from the array and repeatedly extracts the maximum element.",
                "pseudocode": """procedure heapSort(A : list)
        n = length(A)
        // Build heap
        for i = n/2 - 1 downto 0 do
            heapify(A, n, i)
        end for
        // Extract elements
        for i = n-1 downto 0 do
            swap(A[0], A[i])
            heapify(A, i, 0)
        end for
    end procedure

    procedure heapify(A : list, n, i)
        // Heapify subtree rooted at i
    end procedure""",
                "complexity": "Time: O(n log n)\nSpace: O(1)",
                "best_case": "O(n log n)",
                "worst_case": "O(n log n)",
                "stable": False
            },
            "Shell Sort": {
                "description": "Generalization of insertion sort that allows exchange of far items.",
                "pseudocode": """procedure shellSort(A : list)
        n = length(A)
        gap = n / 2
        while gap > 0 do
            for i = gap to n-1 do
                temp = A[i]
                j = i
                while j >= gap and A[j-gap] > temp do
                    A[j] = A[j-gap]
                    j = j - gap
                end while
                A[j] = temp
            end for
            gap = gap / 2
        end while
    end procedure""",
                "complexity": "Time: O(n^(3/2))\nSpace: O(1)",
                "best_case": "O(n log n)",
                "worst_case": "O(n²)",
                "stable": False
            },
            "Radix Sort": {
                "description": "Sorts numbers digit by digit starting from least significant digit.",
                "pseudocode": """procedure radixSort(A : list)
        max = find maximum number in A
        exp = 1
        while max/exp > 0 do
            countingSort(A, exp)
            exp = exp * 10
        end while
    end procedure""",
                "complexity": "Time: O(nk)\nSpace: O(n+k)",
                "best_case": "O(nk)",
                "worst_case": "O(nk)",
                "stable": True
            },
            "Counting Sort": {
                "description": "Counts occurrences of each element and calculates positions in output.",
                "pseudocode": """procedure countingSort(A : list)
        max = find maximum number in A
        count = array of size max+1 initialized to 0
        output = array of size length(A)
        
        // Store count of each element
        for i = 0 to length(A)-1 do
            count[A[i]] = count[A[i]] + 1
        end for
        
        // Change count[i] to position in output
        for i = 1 to max do
            count[i] = count[i] + count[i-1]
        end for
        
        // Build output array
        for i = length(A)-1 downto 0 do
            output[count[A[i]]-1] = A[i]
            count[A[i]] = count[A[i]] - 1
        end for
    end procedure""",
                "complexity": "Time: O(n+k)\nSpace: O(n+k)",
                "best_case": "O(n+k)",
                "worst_case": "O(n+k)",
                "stable": True
            }
        }


algorithm_info = create_algorithm_info()