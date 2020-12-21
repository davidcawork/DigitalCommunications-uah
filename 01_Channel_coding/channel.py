#!/usr/bin/python3

import random, numpy as npy


class Channel(object):

    """Class to simulate a noise channel"""

    def __init__(self, prob=0.02):
        self.err_probability = prob

    def run(self, code_tx):

        code_rx = list()

        for bit in code_tx:
            if random.random() <= self.err_probability:
                bit = 0 if bit == 1 else 1
            code_rx.append(bit)

        return npy.array(code_rx)