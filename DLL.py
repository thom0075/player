#!python3

class Node:
    def __init__(self, data=None):
        self.data = data
        self.next = None
        self.prev = None
        self.playing = False


"""
#TODO
- Inserting Items to Empty List     X
- Inserting Items at the End        X
- Deleting Elements from the Start  X
- Deleting Elements from the End    X
- Traversing the Linked List        X
"""


class DLL:
    def __init__(self):
        self.head = None
        self.tail = None

    def InsertToEmptyDLL(self, data):
        if self.head is None:
            newNode = Node(data)
            self.head = newNode
            self.tail = self.head
            self.head.prev = self.tail
        else:
            print("List is empty")

    def InsertToEnd(self, data):
        if self.head is None:
            newNode = Node(data)
            self.head = newNode
            self.tail = newNode
            newNode.prev = self.tail
            newNode.next = self.head
            return
        newNode = Node(data)
        self.tail.next = newNode
        newNode.prev = self.tail
        self.tail = self.tail.next
        self.tail.next = self.head
        self.head.prev = self.tail
        print("")

    def DeleteFromHead(self):
        if self.head is None:
            print("List empty, nothing to delete")
            return
        if self.head.next is None:
            self.head = None
            return
        self.head = self.head.next
        # self.head.prev = None

    def DeleteFromTail(self):
        if self.head is None:
            print("List empty, nothing to delete")
            return
        self.tail.prev.next = self.head
        self.tail = self.tail.prev  # overwrites tail node with its previous one

    def TraverseDLL(self, FindPlaying=False, SetPlaying=False, RPlaying=False):
        if self.head is None:
            print("List empty, nothing to traverse")
            return
        if self.head.next is None:
            print(self.head.data)
            return
        n = self.head
        while True:
            print(n.data, end="\n")
            if n is self.tail:
                break
            if FindPlaying:
                if n.playing:
                    return n
            if SetPlaying:
                n.playing = True
                return
            if RPlaying:
                n.playing = False
                return
            n = n.next
        return

    # def push(self, data):
    #     newNode = Node(data)
    #     newNode.next = self.head
    #     if self.head is not None:


if __name__ == "__main__":
    listD = DLL()
    listD.InsertToEmptyDLL("Hello")
    listD.InsertToEnd("World")
    listD.InsertToEnd("!")
    listD.TraverseDLL()
