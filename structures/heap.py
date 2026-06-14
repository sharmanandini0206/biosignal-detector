'''
structures/heap.py
Implementing fixed capacity MinHeap from scratch using a plain Python list.
It acts like a Priority Queue to track the top K most severe alerts

Mechanics :
- Time Complexity: O(log k) for push and pop, O(1) to peek minimum.
- Space Complexity: O(k) where k is the maximum capacity of the heap.
- Principle: The parent node is always smaller than or equal to its children.

'''

class MinHeap :
    def __init__(self, capacity) :
    def size(self) :
    def is_empty(self) :
    def peek(self) :
    def insert(self, alert) :
    def _heapify_up(self, index) :
    def _heapify_down(self, index) :
    def get_sorted_elements(self) :
    