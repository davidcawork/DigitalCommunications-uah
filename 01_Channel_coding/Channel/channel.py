#!/usr/bin/python3

import random
import numpy as npy


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


def randBits(size):
    "Method to create a random binary frame"

    frame = npy.zeros(size, dtype=npy.int32)
    frame[:random.randint(0, size)] = 1
    npy.random.shuffle(frame)

    return frame


def getGood(secuence_src, secuence_dst):
    "Method to count how much bits of a secuence are equal"
    total_good = 0

    try:
        for i in range(0, secuence_src.size):
            if secuence_src[i] == secuence_dst[i]:
                total_good += 1
    except:
        total_good = 0
    return total_good
