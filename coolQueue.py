"""Megan Perry
A quick implementation of a queue list
"""
class CoolQueue():
    def __init__(self):
        self.queue = []    #empty list is queue
    
    def push(self, value):    #add to end of queue
        self.queue.append(value)
        
    def pop(self):    #remove first item of the list
        return self.queue.pop(0)
    
    def is_empty(self):
        if len(self.queue) == 0:
            return True
        else:
            return False
        
    def look_at_top(self):
        return self.queue[0]

    


           