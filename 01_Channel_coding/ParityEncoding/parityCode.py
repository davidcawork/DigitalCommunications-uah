#!/usr/bin/python3

from scipy import stats
import numpy as npy


class ParityCode(object):

    """Class to manage Parity Codes (even parity)"""
    
    @staticmethod
    def parityEncoder(bits, n):
        encoded_code = []

        # If there is a even number of ones in (n-1) tuple, parity bit -> 0
        for word in npy.split(npy.array(bits), npy.array(bits).size/(n-1)):
            parity_bit = 0 if npy.count_nonzero(word == 1) % 2 == 0 else 1
            encoded_code.append(npy.append(word, parity_bit))
        
        return npy.hstack(encoded_code)

    @staticmethod
    def parityDecoder(code, n):

        decoded_code = list()
        err_detected = 0

        for word in npy.split(npy.array(code),npy.array(code).size/n):

            # Check parity bit
            parity_bit = 0 if npy.count_nonzero(word[0:2] == 1) % 2 == 0 else 1
            if not parity_bit == word[2]:
                err_detected +=1

            
            decoded_code.append(word[0:2])
        
        return [npy.hstack(decoded_code), err_detected]



                