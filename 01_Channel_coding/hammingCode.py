#!/usr/bin/python3

from scipy import stats
import numpy as npy
import math


class HammingCode(object):

    """Class to manage Hamming Codes"""

    def __init__(self, q=3):
        self.q = q
        self.n = 2**(q) - 1
        self.k = self.n - q

        self.H, self.G = self.generateMatrix(self.q)

    @staticmethod
    def generateMatrix(q):
        """

            - Def:  H = [ Pt | Iq ] ( q x n )
            - Def:  G = [ Ik |  P ] ( k x n )

        :param q: int (number of redundant digits)
        :returns: [ numpy.array, numpy.array] (H , G)
        """
        n = 2 ** (q) - 1
        k = n - q

        # First, we have to generate (H) matrix, called parity check matrix.
        H_Pt = npy.zeros((n - q, q), dtype=int)

        # As we know, q bits will be powers of two.. So we have just to fill H_Pt without them
        index = 0
        for i in range(q, n + 1):
            if not HammingCode.isPower2(i):
                H_Pt[index] = list(str(bin(i))[2:].zfill(q))
                index += 1

        # Just to correct order
        H_Pt = H_Pt.T

        H = npy.hstack((H_Pt, npy.identity(q, dtype=int)))

        # Once we have parity check matrix, we can calculate generator matrix (G)
        P = H_Pt.T
        G = npy.concatenate((npy.identity(k, dtype=int), P), axis=1)

        return [H, G]

    @staticmethod
    def isPower2(number):
        return (number & (number - 1) == 0) and number != 0

    @staticmethod
    def zeroPadding(vector, size):
        return npy.pad(vector, pad_width=(0, size), mode='constant')

    def hammingEncoder(self, bits):
        encoded_code = []
        code = npy.array(bits)

        if not code.size % self.k == 0:
            code = self.zeroPadding(code, self.k - (code.size % self.k))

        for word in npy.split(code, code.size / self.k):
            encoded_code.append(npy.dot(word, self.G))
            pass

        return npy.hstack(encoded_code)

    def hammingDecoder(self, code):
        pass
