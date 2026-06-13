'''
structures/stack.py

Implementing an AlertStack with built-in Undo/Redo capability with Python lists.
It tracks system anomaly alerts.

Mechanics :
- Time Complexity: O(1) for push, pop, undo, redo operations.
- Space Complexity: O(n) where n is the historical number of alerts generated.
- Principle: Last in, First out (LIFO).
'''

class AlertStack : 
    def __init__(self) :
        # initialize empty alert stack and empty redo history stack
        # dict = {'type' : str, 'value' : float, 'timestamp' : float, 'severity' : float}
        self.stack = []
        self.redo_stack = []

    def is_empty(self) :
        # return true if there are no active alerts in history log
        return len(self.stack) == 0
    
    def push(self, alert) :
        # pushed new alert dict onto the top of stack
        # clear redo stack since new alert invalidates redo history
        self.stack.append(alert)
        self.redo_stack.clear()
    
    def pop(self) :
        # remove and return most recent alert from top of stack
        return self.stack.pop()
    
    def peep(self) :
        # return top/most recent alert without removing it from stack
        return self.stack[-1] if not self.is_empty() else None
    
    def size(self) :
        return len(self.stack)
    
    def undo(self) :
        # pop latest alert off main log and push into redo stack
        # allows user to revert to previous alert state through CLI
        undone_alert = self.stack.pop()
        self.redo_stack.append(undone_alert)
        return undone_alert
    
    def redo(self) :
        # pop latest alert off redo stack and push back into main log
        restored_alert = self.redo_stack.pop()
        self.stack.append(restored_alert)
        return restored_alert
    
    def get_all_alerts(self) :
        # return complete underlyin glist array
        # useful for iterating over historical incidents
        return self.stack