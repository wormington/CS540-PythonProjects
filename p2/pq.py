''' author: hobbes
    source: cs540 canvas
    TODO: complete the enqueue method
'''
class PriorityQueue(object):
    def __init__(self):
        self.queue = []
        self.max_len = 0

    def __str__(self):
        return ' '.join([str(i) for i in self.queue])

    def is_empty(self):
        return len(self.queue) == 0

    def enqueue(self, state_dict):
        """ Items in the priority queue are dictionaries:
             -  'state': the current state of the puzzle
             -      'h': the heuristic value for this state
             - 'parent': a reference to the item containing the parent state
             -      'g': the number of moves to get from the initial state to
                         this state, the "cost" of this state
             -      'f': the total estimated cost of this state, g(n)+h(n)

            For example, an item in the queue might look like this:
             {'state':[1,2,3,4,5,6,7,8,0], 'parent':[1,2,3,4,5,6,7,0,8],
              'h':0, 'g':14, 'f':14}

            Please be careful to use these keys exactly so we can test your
            queue, and so that the pop() method will work correctly.

            TODO: complete this method to handle the case where a state is
                  already present in the priority queue
        """

        # Checks to see if a state already exists in the priority queue and
        # sets in_open to true if it does.
        in_open = False
        match = None
        for item in self.queue:
            if item['state'] == state_dict['state']:
                in_open = True
                match = item
        
        # If a state is already in the queue, it checks the existing one to see
        # if the new one has a better path. If the new one has a better path,
        # the existing one is replaced with the new one. Otherwise, the existing
        # state stays.
        if in_open:
            if match['g'] > state_dict['g']:
                match['g'] = state_dict['g']
                match['parent'] = state_dict['parent']
                match['f'] = match['g'] + match['h']
            else:
                return
        
        if not in_open:
            self.queue.append(state_dict)

        # track the maximum queue length
        if len(self.queue) > self.max_len:
            self.max_len = len(self.queue)

    def requeue(self, from_closed):
        """ Re-queue a dictionary from the closed list (see lecture slide 21)
        """
        self.queue.append(from_closed)

        # track the maximum queue length
        if len(self.queue) > self.max_len:
            self.max_len = len(self.queue)

    def pop(self):
        """ Remove and return the dictionary with the smallest f(n)=g(n)+h(n)
        """
        minf = 0
        for i in range(1, len(self.queue)):
            if self.queue[i]['f'] < self.queue[minf]['f']:
                minf = i
        state = self.queue[minf]
        del self.queue[minf]
        return state

# pq = PriorityQueue()
# aState = {'state': [1,2,3,4,5,6,7,8,0], 'h': 0, 'g': 1, 'parent': None, 'f': 1}
# pq.enqueue(aState)
# pq.enqueue({'state': [1,2,3,4,5,6,7,8,0], 'h': 0, 'g': 0, 'parent': None, 'f': 0})
# print(aState)