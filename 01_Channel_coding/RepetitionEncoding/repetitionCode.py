#!/usr/bin/python3

from scipy import stats
import numpy as npy


class RepetitionCode(object):

    """Class to manage Repetition Codes"""

    @staticmethod
    def repetitionEncoder(bits, n):
        """
        Function to encode data with Repetition

        :param bits: list (bits to encode)
        :param n: int (number of total digits)
        :returns: numpy.array (encoded data)
        """
        return npy.repeat(npy.array(bits), n)

    @staticmethod
    def repetitionDecoder(code, n):
        """
        Function to decode data with Repetition

        :param code: numpy.array (bits to decode)
        :param n: int (number of total digits)
        :returns: numpy.array (decoded data)
        """
        decoded_code = []

        for word in npy.split(npy.array(code), npy.array(code).size/n):

            # First, we will check if all elements of the given word are equal.
            # If there is one element different in word, we could say that an error has occurred.
            if not npy.all(word == word[0]):

                # By calculating the mode, we get the element that appears most often in the given word,
                # and then, we are able to "fix" the error :)
                word.fill(stats.mode(word)[0][0])

            # It just choose an element of the word, at this point, all the elements are equal
            decoded_code.append(word[0])

        return npy.array(decoded_code)
