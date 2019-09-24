class MGListNode:
    """
    A node in a doubly-linked list.
    """
    def __init__(self, data=None, prev=None, next=None):
        self.data = data
        self.prev = prev
        self.next = next

    def __repr__(self):
        return repr(self.data)


class MarbleGameLinkedList:
    def __init__(self):
        """
        Create a new doubly linked list.
        Takes O(1) time.
        """
        self.head = None

    def __repr__(self):
        """
        Return a string representation of the list.
        Takes O(n) time.
        """
        nodes = []
        curr = self.head
        while curr:
            if(curr==self.head):
                nodes.append(f"**{repr(curr)}**")
            else:
                nodes.append(repr(curr))
            curr = curr.next
            if(curr == self.head): break
        return '[' + ', '.join(nodes) + ']'

    def add_marble(self, data):
        """
        Insert a new element between one_clockwise away from current and two clockwise
        away from clockwise.
        """
        if not self.head:
            first_node = MGListNode(data=data)
            self.head = first_node
            first_node.next = first_node
            first_node.prev = first_node
            return
        curr = self.head
        one_clock = curr.next
        two_clock = one_clock.next
        self.head = one_clock.next = two_clock.prev = MGListNode(data=data, prev=one_clock, next=two_clock)

    def remove_elem(self, node):
        """
        Unlink an element from the list.
        Takes O(1) time.
        """
        if node.prev:
            node.prev.next = node.next
        if node.next:
            node.next.prev = node.prev
        if node is self.head:
            self.head = node.next
        node.prev = None
        node.next = None
        

    def remove_seven(self):
        """
        Removes an element 7 prior to the head and resets head
        """
        curr = self.head
        for i in range(6):
            curr = curr.prev
        self.head=curr
        data = curr.prev.data
        self.remove_elem(curr.prev)
        return data