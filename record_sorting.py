import time

class SortingRecorder:
    def __init__(self):
        self.start_time = 0
        self.comparisons = 0
        self.swaps = 0
        self.accesses = 0  # Add this line
    
    def start_recording(self):
        self.start_time = time.time()
        self.comparisons = 0
        self.swaps = 0
        self.accesses = 0  # Add this line
    
    def update_stats(self, comparisons, swaps, accesses):  # Update this method
        self.comparisons = comparisons
        self.swaps = swaps
        self.accesses = accesses
    
    def get_elapsed_time(self):
        return time.time() - self.start_time