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
        # initialize fixed capacity min heap
        self.capacity = capacity
        self.heap = []
    
    def size(self) :
        # return the curr num of items stored in heap
        return len(self.heap)
    
    def is_empty(self) :
        # return true if heap contains zero elements
        return len(self.heap) == 0
   
    def peek(self) :
        # return min element (root) without removing it
        if self.is_empty() :
            return None
        return self.heap[0]
    
    def insert(self, alert) :
        # offers a new alert to heap
        # If heap isnt full, it appends alert and heapifies up
        # if heap is full, it compares severity to the root
        # if new alert is more severe, replace root and heapify down
        if self.size() < self.capacity :
            self.heap.append(alert)
            self._heapify_up(self.size() - 1)
            return True
        elif alert['severity'] > self.heap[0]['severity'] :
            self.heap[0] = alert
            self._heapify_down(0)
            return True
        return False
    
    def _heapify_up(self, index) :
        # move element up tree till heap contrainst are used
        parent_index = (index - 1) // 2
        if index > 0 and self.heap[index]['severity'] < self.heap[parent_index]['severity'] :
            # swap parent with child
            self.heap[index], self.heap[parent_index] = self.heap[parent_index], self.heap[index]
            # recursively walk up the tree
            self._heapify_up(parent_index)
    
    def _heapify_down(self, index) :
        # move element down tree till heap constraints are satisfied
        smallest = index
        left_child = 2 * index + 1
        right_child = 2 * index + 2
        # check if left child exists and is smaller than current smallest
        if left_child < self.size() and self.heap[left_child]['severity'] < self.heap[smallest]['severity'] :
            smallest = left_child
        # check if right child exists and is smaller than smallest
        if right_child < self.size() and self.heap[right_child]['severity'] < self.heap[smallest]['severity'] :
            smallest = right_child
        # if smallest node is not curr node, swap and keep bubbling down
        if smallest != index :
            self.heap[index], self.heap[smallest] = self.heap[smallest], self.heap[index]
            self._heapify_down(smallest)
    
    def get_sorted_elements(self) :
        # return sorted list of alerts in decending order (highest severity first).
        # since this is a min heap, we copy array and pop the min to do a miniature heap sort, then reverse results.
        # O(k log k) time complexity 
        temp_heap = list(self.heap)
        sorted_list = []

        sorted_list = sorted(temp_heap, key=lambda x: x['severity'], reverse=True)
        return sorted_list