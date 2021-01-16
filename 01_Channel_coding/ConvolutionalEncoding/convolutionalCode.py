#!/usr/bin/python3

from operator import attrgetter
from pympler import asizeof
import numpy as npy
import uuid


state_chart = {'A': [{'state': 'A', 'in': npy.array([0, 0]), 'out':0}, {'state': 'B', 'in': npy.array([1, 1]), 'out':1}],
               'B': [{'state': 'C', 'in': npy.array([0, 1]), 'out':0}, {'state': 'D', 'in': npy.array([1, 0]), 'out':1}],
               'C': [{'state': 'A', 'in': npy.array([1, 1]), 'out':0}, {'state': 'B', 'in': npy.array([0, 0]), 'out':1}],
               'D': [{'state': 'C', 'in': npy.array([1, 0]), 'out':0}, {'state': 'D', 'in': npy.array([0, 1]), 'out':1}]}
viterbi_childs = []


class ConvolutionalCode(object):

    """Class to manage Convolutional Codes"""

    def __init__(self, L=2, n=2, k=1):
        """
        :param L: int (number of registers, socalled memory param)
        :param k: int (number of useful digits)
        :param n: int (number of total of digits)
        """
        self.L = npy.zeros(L, dtype=int)
        self.n = n
        self.k = k

    def ConvolutionalEncoder(self, bits):
        """
        Function to encode data with Convolutional encode block.

        vv Attention!!! It is not generalised because we have to follow a scheme vv

        [+] Scheme : https://github.com/davidcawork/DigitalCommunications-uah/blob/main/01_Channel_coding/ConvolutionalEncoding/scheme.png

        ^^ Attention!!! It is not generalised because we have to follow a scheme ^^


        :param bits: list (bits to encode)
        :returns: numpy.array (encoded data)
        """
        encoded_code = []
        code = npy.array(bits)

        for j in range(0, code.size):
            # Gimme, gimme, gimme a bit after midnight ~~
            # Let's calculate  xj_first and xj_second (mod 2)
            xj_first = (self.L[1] + code[j]) % 2
            xj_second = (((code[j] + self.L[0]) % 2) + self.L[1]) % 2

            encoded_code.extend((xj_first, xj_second))

            # Shift time :)
            self.L[1] = self.L[0]
            self.L[0] = code[j]

        return npy.hstack(encoded_code)

    def viterbiDecoder(self, code):
        """
        Function to decode data with Viterbi Algorithm

        :param code: numpy.array (bits to decode)
        :returns: numpy.array (decoded data)
        """
        depth = 0
        viterbiTree = Node(state='A', depth=depth, HammingDistance=0)

        for word in npy.split(npy.array(code), npy.array(code).size/self.n):
            ConvolutionalCode.viterbi_iter(viterbiTree, word, depth)
            ConvolutionalCode.pruning(viterbiTree, depth)
            depth += 1

        states = ConvolutionalCode.bestPath(viterbiTree)

        return [npy.hstack(ConvolutionalCode.getDecoded_code(states)), asizeof.asizeof(viterbiTree)]

    @staticmethod
    def HammingDistance(A, B):
        """
        Function to calculate Hamming distance 

        :param A: list (word)
        :param B: list (word)
        :returns: int (Hamming distance)
        """
        return sum(bit_a != bit_b for bit_a, bit_b in zip(A, B))

    @staticmethod
    def getDecoded_code(states):
        """
        Function to translate states into output bits 

        :param states: list (states from the best path)
        :returns: list (output bits )
        """
        decoded_code = []

        for i in range(0, len(states) - 1):
            current_state = state_chart[states[i]]
            path = [paths for paths in current_state if paths["state"] == states[i + 1]]
            decoded_code.append(path[0]["out"])
        return decoded_code

    @staticmethod
    def viterbi_iter(viterbiTree, word, depth):
        """
        Function to grow the Viterbi Tree (just a wrapper)

        :param viterbiTree: obj (viterbiTree)
        :param word: npy.array (current word)
        :param depth: int (actual depth of the tree)
        :returns: none
        """
        viterbiTree.grow(word, depth, 0)

    @staticmethod
    def pruning(viterbiTree, depth):
        """
        Function to prune the Viterbi Tree 

        :param viterbiTree: obj (viterbiTree)
        :param depth: int (actual depth of the tree)
        :returns: none
        """
        for state, value in state_chart.items():
            viterbiTree.find(state, depth + 1)
            if len(viterbi_childs) > 1:
                child_to_delete = max(viterbi_childs, key=attrgetter('HammingDistance'))
                viterbiTree.delete(child_to_delete.id)
            viterbi_childs.clear()

    @staticmethod
    def bestPath(viterbiTree):
        """
        Function to calculate the best path, init-end of the viterbi tree

        :param viterbiTree: obj (viterbiTree)
        :returns: list (states)
        """
        path = []
        current_node = viterbiTree

        while True:
            path.append(current_node.state)
            current_node = min(current_node.childs, key=attrgetter('HammingDistance'))
            if not current_node.childs:
                path.append(current_node.state)
                break
        return path


class Node(object):
    """
        Class to manage Viterbi nodes
    """

    def __init__(self, state, depth, HammingDistance):
        self.id = str(uuid.uuid4())
        self.state = state
        self.HammingDistance = HammingDistance
        self.depth = depth
        self.childs = []

    def grow(self, word, depth, total_HammingDistance):
        if not self.childs and self.depth == depth:
            for paths in state_chart[self.state]:
                self.childs.append(Node(state=paths["state"],
                                        depth=depth + 1,
                                        HammingDistance=total_HammingDistance + ConvolutionalCode.HammingDistance(word, paths["in"])))
        else:
            for child in self.childs:
                child.grow(word, depth, self.HammingDistance + total_HammingDistance)

    def find(self, state, depth):
        if self.state == state and self.depth == depth:
            viterbi_childs.append(self)
        else:
            for child in self.childs:
                child.find(state, depth)

    def delete(self, uid):
        for child in self.childs:
            if child.id == uid:
                self.childs.remove(child)
                return True

        for child in self.childs:
            if child.delete(uid):
                return True

        return False
