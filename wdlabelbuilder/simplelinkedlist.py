# -*- coding: UTF-8
from __future__ import print_function


class Node(object):

    def __init__(self, qnumber, label):
        self.qnumber = qnumber
        self.label = label
        self.next = None
        try:
            int(''.join(label.split()[-1:]))
            self.point_in_time = int(''.join(label.split()[-1:]))
        except ValueError:
            try:
                int(''.join(label.split()[:1]))
                self.point_in_time = ''.join(label.split()[:1])
            except ValueError:
                self.point_in_time = ' '.join(label.split()[2:])

    def print_me(self):
        print(self.point_in_time, '<', self.next._point_in_time)


class LinkedList(object):
    TAB = '	'

    def __init__(self):
        self.head = None
        self.tail = None
        self.length = 0
        self.qprint_len = 0
        self.value_print_len = 0

    def add_node(self, node):
        if self.length == 0:
            # Add node to an empty list
            self.head = node
            self.tail = node
            self.length += 1
        elif self.length == 1:
            # Add node to a list with one other node
            if node.point_in_time > self.head.point_in_time:
                self.add_tail(node)
            else:
                self.add_head(node)
        elif node.point_in_time < self.head.point_in_time:
            # Add new head
            self.add_head(node)
        elif node.point_in_time > self.tail.point_in_time:
            # Add new tail
            self.add_tail(node)
        else:
            # Add node to a list with at least two other nodes
            self.add_node_to_position(node)

    def add_head(self, node):
        '''
        Add a node as the new head of the list.
        '''
        tmp = self.head
        self.head = node
        node.next = tmp
        self.length += 1

    def add_tail(self, node):
        '''
        Add a node as the new tail of the list.
        '''
        tmp = self.tail
        self.tail = node
        tmp.next = node
        self.length += 1

    def add_node_to_position(self, node):
        '''
        Add a node to the list based on the
        value of point_in_time.
        '''
        item = self.head
        while item.point_in_time < node.point_in_time:
            prev = item
            item = item.next
        node.next = item
        prev.next = node
        self.length += 1
