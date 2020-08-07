# Course: CS 261 - Data Structures
# Student Name: Mallory Huston
# Assignment: 5, Part 2
# Description: Implementation of a min heap data structure.


# Import pre-written DynamicArray and LinkedList classes
from a5_include import *


class MinHeapException(Exception):
    """
    Custom exception to be used by MinHeap class
    DO NOT CHANGE THIS CLASS IN ANY WAY
    """
    pass


class MinHeap:
    def __init__(self, start_heap=None):
        """
        Initializes a new MinHeap
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.heap = DynamicArray()

        # populate MH with initial values (if provided)
        # before using this feature, implement add() method
        if start_heap:
            for node in start_heap:
                self.add(node)

    def __str__(self) -> str:
        """
        Return MH content in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return 'HEAP ' + str(self.heap)

    def is_empty(self) -> bool:
        """
        Return True if no elements in the heap, False otherwise
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self.heap.length() == 0

    def add(self, node: object) -> None:
        """
        Adds a new object to the MinHeap maintaining heap property
        """
        # insert node at the end of the DynamicArray
        self.heap.append(node)

        # handle case where MinHeap was empty
        if self.heap.length() == 1:
            return

        # swap new node with parent until new node > parent
        child = self.heap.length() - 1
        parent = (child - 1) // 2
        while self.heap.get_at_index(parent) > self.heap.get_at_index(child) and child != 0:
            self.heap.swap(parent, child)
            child = parent
            parent = (child - 1) // 2

    def get_min(self) -> object:
        """
        Returns an object with a minimum key without removing it from the heap
        """
        # handle case where MinHeap is empty
        if self.heap.length() == 0:
            raise MinHeapException

        # handle case where MinHeap is non-empty
        return self.heap.get_at_index(0)

    def remove_min(self) -> object:
        """
        Returns an object with a minimum key and removes it from the heap
        """
        # handle case where MinHeap is empty
        if self.heap.length() == 0:
            raise MinHeapException

        # swap min node with node at end of array, pop(), and reference for returning later
        self.heap.swap(0, self.heap.length() - 1)
        return_node = self.heap.pop()

        # handle case where resulting MinHeap is empty
        if self.heap.length() == 0:
            return return_node

        # prepare variables to help loop through MinHeap while re-organizing
        p_ind = 0
        p_val = self.heap.get_at_index(p_ind)
        c1_ind = 1
        c2_ind = 2
        min_ind = self.min_index(c1_ind, c2_ind)
        min_val = self.heap.get_at_index(min_ind)

        # loop through tree swapping replacement node with appropriate children
        while not self.out_range(c1_ind, c2_ind) and p_val > min_val:
            self.heap.swap(p_ind, min_ind)
            p_ind = min_ind
            p_val = self.heap.get_at_index(p_ind)
            c1_ind = (2 * p_ind) + 1
            c2_ind = (2 * p_ind) + 2
            min_ind = self.min_index(c1_ind, c2_ind)
            min_val = self.heap.get_at_index(min_ind)

        # MinHeap has been re-organized, so return original min value
        return return_node

    def build_heap(self, da: DynamicArray) -> None:
        """
        Receives a DynamicArray with objects in any order and builds a proper MinHeap from them
        """
        # build new DynamicArray to prevent destruction of original da
        da2 = DynamicArray()
        for index in range(da.length()):
            da2.append(da.get_at_index(index))

        # handle case where da is of length == 0, 1
        if da2.length() < 2:
            self.heap = da2
            return

        # initialize variables to help with terminating and controlling flow of outer loop
        count = 0
        root_bool = False

        # outer loop should continue until root element has been percolated down
        while root_bool == False:
            # if first iteration of outer loop, set parent node to first non-leaf node
            if count == 0:
                p_outer_ind = ((da2.length() // 2) - 1)
            # if NOT first iteration, set parent to current parent's parent
            else:
                p_outer_ind = p_outer_ind - 1

            # if we are currently handling root node, trip flag to stop outer loop
            if p_outer_ind == 0:
                root_bool = True

            # establish beginning variable references for inner loop
            p_ind = p_outer_ind
            p_val = da2.get_at_index(p_ind)
            c1_ind = (2 * p_outer_ind) + 1
            c2_ind = (2 * p_outer_ind) + 2
            min_ind = self.min_index_da(c1_ind, c2_ind, da2)
            min_val = da2.get_at_index(min_ind)

            # increment count variable to control flow for p_outer_ind
            count += 1

            # loop through tree percolating element down until we take care of the root
            while not self.out_range_da(c1_ind, c2_ind, da2) and p_val > min_val:
                da2.swap(p_ind, min_ind)
                p_ind = min_ind
                p_val = da2.get_at_index(p_ind)
                c1_ind = (2 * p_ind) + 1
                c2_ind = (2 * p_ind) + 2
                min_ind = self.min_index_da(c1_ind, c2_ind, da2)
                min_val = da2.get_at_index(min_ind)

        # outer loop has completed, so reference da w/ MinHeap.heap
        self.heap = da2

    # Helper Functions #

    def min_index_da(self, index_1: int, index_2: int, da: object) -> int:
        """
        Returns index with minimum value from two indices
        """
        # handle case where index_1 is out of range
        if index_1 > da.length() - 1 and index_2 < da.length():
            return index_2

        # handle case where index_2 is out of range
        if index_2 > da.length() - 1 and index_1 < da.length():
            return index_1

        # handle case where both indices are out of range
        if index_2 > da.length() - 1 and index_1 > da.length() - 1:
            return 0

        # define convenient variables to make code more readable
        value_1 = da.get_at_index(index_1)
        value_2 = da.get_at_index(index_2)

        # determine which value to return
        if value_1 < value_2:
            return index_1
        return index_2

    def out_range_da(self, index_1: int, index_2: int, da: object) -> bool:
        """
        Indicates whether both indices are out of range
        """
        if index_1 > da.length() - 1 and index_2 > da.length() - 1:
            return True
        return False

    def min_index(self, index_1: int, index_2: int) -> int:
        """
        Returns index with minimum value from two indices
        """
        # handle case where index_1 is out of range
        if index_1 > self.heap.length() - 1 and index_2 < self.heap.length():
            return index_2

        # handle case where index_2 is out of range
        if index_2 > self.heap.length() - 1 and index_1 < self.heap.length():
            return index_1

        # handle case where both indices are out of range
        if index_2 > self.heap.length() - 1 and index_1 > self.heap.length() - 1:
            return 0

        # define convenient variables to make code more readable
        value_1 = self.heap.get_at_index(index_1)
        value_2 = self.heap.get_at_index(index_2)

        # determine which value to return
        if value_1 < value_2:
            return index_1
        return index_2

    def out_range(self, index_1: int, index_2: int) -> bool:
        """
        Indicates whether both indices are out of range
        """
        if index_1 > self.heap.length() - 1 and index_2 > self.heap.length() - 1:
            return True
        return False


# BASIC TESTING
if __name__ == '__main__':

    print("\nPDF - add example 1")
    print("-------------------")
    h = MinHeap()
    print(h, h.is_empty())
    for value in range(300, 200, -15):
        h.add(value)
        print(h)

    print("\nPDF - add example 2")
    print("-------------------")
    h = MinHeap(['fish', 'bird'])
    print(h)
    for value in ['monkey', 'zebra', 'elephant', 'horse', 'bear']:
        h.add(value)
        print(h)

    print("\nPDF - get_min example 1")
    print("-----------------------")
    h = MinHeap(['fish', 'bird'])
    print(h)
    print(h.get_min(), h.get_min())

    print("\nPDF - remove_min example 1")
    print("--------------------------")
    h = MinHeap([1, 10, 2, 9, 3, 8, 4, 7, 5, 6])
    while not h.is_empty():
        print(h, end=' ')
        print(h.remove_min())

    print("\nPDF - build_heap example 1")
    print("--------------------------")
    da = DynamicArray([100, 20, 6, 200, 90, 150, 300])
    h = MinHeap(['zebra', 'apple'])
    print(h)
    h.build_heap(da)
    print(h)
    da.set_at_index(0, 500)
    print(da)
    print(h)
