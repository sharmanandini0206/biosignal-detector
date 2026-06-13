'''
structures/dequie.py

Implementing a fixed capacity circular deque using a python list.
It is optimized specifically for sliding window signal processing.

Mechanics:
- Time complexity: O(1) for push_right, pop_left, and random access.
- Space Complexity: O(n) where n is the max capacity.
- Optimization: Dynamically tracks running sum and running sum of squares to allow O(1) computation of mean and SD.
'''

import math

class CircularDeque :
    def __init__(self, capacity) :
        # initializing fixed capacity circular buffer. 
        # each storage slot will hold tuple (value, timestamp)
        self.capacity = capacity
        self.buffer = [None] * capacity
        # pointers
        self.head = 0       # points to oldest element aka front of deque
        self.tail = 0       # points to next empty slot to write aka back of deque
        self.size = 0       # curr num of elements filled
        # stats
        self.running_sum = 0.0
        self.running_sum_sq = 0.0

    def is_empty(self) :
        # returns true if deque is empty
        return self.size == 0
    
    def is_full(self) :
        # returns true if deque has reached max capacity
        return self.size == self.capacity
    
    def push_right(self, item) :
        # adds new (value, timestamp) tuple to back of deque
        if self.is_full() :
            raise IndexError("Push from right failed. CircularDeque is full.")
        value, timestamp = item
        # write item to current tail position
        self.buffer[self.tail] = (value, timestamp)
        # advance tail pointer
        self.tail = (self.tail + 1) % self.capacity
        self.size += 1
        # update stats
        self.running_sum += value
        self.running_sum_sq += value ** 2
    
    def pop_left(self) :
        # removes and returns the oldest (value, timestamp) tuple
        if self.is_empty() :
            raise IndexError("Pop from left failed. Circular Deque is empty.")
        # extract item at head position
        item = self.buffer[self.head]
        value, timestamp = item
        # clear memory slot
        self.buffer[self.head] = None
        # advance head pointer 
        self.head = (self.head + 1) % self.capacity
        self.size -= 1
        # update stats
        self.running_sum -= value
        self.running_sum_sq -= value ** 2

        return item
    
    def get_stats(self) :
        # compute and return (mean, std_dev) of current window
        if self.size == 0 :
            return 0.0, 0.0
        mean = self.running_sum / self.size
        # formula = E[X^2] - (E[X])^2
        variance = (self.running_sum_sq / self.size) - (mean ** 2)
        # to handle tiny floating point rounding errors that are slightly below zero
        if variance < 0 :
            variance = 0.0
        std_dev = math.sqrt(variance)
        return mean, std_dev
    
    def __getitem__(self, index) :
        # allows random access through brackets.
        # maps the logical index to the shifted physical index
        if index < 0 or index >= self.size :
            raise IndexError("CircularDeque index out of range")
        # calculate actual position relative to moving head pointer
        physical_index = (self.head + index) % self.capacity
        return self.buffer[physical_index]
    
    def get_values(self) :
        # returns list of numerical vals
        values = []
        for i in range(self.size):
            physical_index = (self.head + i) % self.capacity
            values.append(self.buffer[physical_index][0])
        return values
    
    def get_timestamps(self) :
        # return list of tumestamps
        timestamps = []
        for i in range(self.size) :
            physical_index = (self.head + i) % self.capacity
            timestamps.append(self.buffer[physical_index][1])
        return timestamps
    
    
