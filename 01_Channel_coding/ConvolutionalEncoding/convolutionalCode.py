#!/usr/bin/python3

from scipy import stats
import numpy as npy
import math


class HammingCode(object):

    """Class to manage Hamming Codes"""

    def __init__(self, q=3):
        """
        :param q: int (number of redundant digits)
        :param k: int (number of useful digits)
        :param n: int (number of total of digits)
        """
        self.q = q
        self.n = 2**(q) - 1
        self.k = self.n - q

        self.H, self.G = self.generateMatrix(self.q)

    @staticmethod
    def generateMatrix(q):
        """
        Function to generate H and G matrix

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
        Iq = npy.identity(q, dtype=int)

        H = npy.hstack((H_Pt, Iq))

        # Once we have parity check matrix, we can calculate generator matrix (G)
        P = H_Pt.T
        Ik = npy.identity(k, dtype=int)

        G = npy.concatenate((Ik, P), axis=1)

        return [H, G]

    @staticmethod
    def isPower2(number):
        """
        :returns: bool  ( True if number is power of two)
        """
        return (number & (number - 1) == 0) and number != 0

    @staticmethod
    def zeroPadding(vector, size):
        """
        :returns: numpy.array (Array with zero padding)
        """
        return npy.pad(vector, pad_width=(0, size), mode='constant')

    def hammingEncoder(self, bits):
        """
        Function to encode data

        :param bits: list (bits to encode) 
        :returns: numpy.array (Encoded code)
        """

        encoded_code = []
        code = npy.array(bits, dtype=int)

        # If the given bits are not multiples of K param, we'ill have to add zeros at the end to archive it (called zeropadding procedure)
        if not code.size % self.k == 0:
            code = self.zeroPadding(code, self.k - (code.size % self.k))

        # We've to use module operator due to we are working with integers, but we want binary result :)
        for word in npy.split(code, code.size / self.k):
            encoded_code.append(npy.dot(word, self.G) % 2)

        return npy.hstack(encoded_code)

    def hammingDecoder(self, code):
        """
        Function to decode encoded data

        :param code: numpy.array (bits encoded)
        :returns: [ numpy.array (bits decoded), int (fixed bits)]
        """
        decoded_code = list()
        fixed = 0

        for word in npy.split(npy.array(code), npy.array(code).size / self.n):

            syndrome = npy.dot(word, self.H.T) % 2

            if not npy.count_nonzero(syndrome) == 0:

                # Ref: The Art of Doing Science and Engineering: Learning to Learn (Chap 12 - Error correcting codes)
                #
                # We can create a table of errors associated to syndromes, following the ML criteria,
                # but what we would really be doing is generating vectors of the same length as
                # the received word with a single bit to one in the position from where the error has occurred.
                #
                # It is easier to see the position (columns) occupied by the value of the syndrome within the
                # parity checking matrix
                position = npy.where(
                    npy.all(self.H == syndrome[:, None], axis=0))[0]

                word[position] = 0 if word[position] == 1 else 1
                fixed += 1

            decoded_code.append(word[:self.k])

        return [npy.hstack(decoded_code), fixed]
