#!/usr/bin/python3

import numpy as npy

class RepetitionCode(object):

    """Class to manage Repetition Codes"""
    
    @staticmethod
    def repetitionEncoder(bits, n):
        return npy.repeat(npy.array(bits), n)

