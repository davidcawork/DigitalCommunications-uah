#!/usr/bin/python3

from ConvolutionalEncoding.convolutionalCode import ConvolutionalCode
from Channel.channel import Channel, randBits, getGood
import numpy as npy
import random
import time


def scenario(prob=0.02, frame_len=20):
    "Main method to simulate a noisy scenario using Convolutional codes"

    # Stats vars
    start_time = time.time()

    # Scenario behaviour
    print("Simulating Convolutional code scenario (Viterbi)...\n")
    # Class Notes example sec:
    #bitsTx = npy.array([1, 1, 0, 1, 0, 1, 0, 0])
    bitsTx = randBits(frame_len)
    code_Tx = ConvolutionalCode(L=2, n=2, k=1).ConvolutionalEncoder(bitsTx)
    code_Rx = Channel(prob).run(code_Tx)
    bitsRx, memory = ConvolutionalCode(L=2, n=2, k=1).viterbiDecoder(code_Rx)

    # Print results
    print('------------------------------------')
    print('Time elapsed: '+str((time.time() - start_time)*1000) + ' ms')
    print('Frame length: '+str(frame_len))
    print('Error probability: '+str(prob))
    print('\n------------ Results ---------------')
    print('[+] Memory usage '+str(memory/1000)+' KB')
    print('[+] Total bits: '+str(frame_len))
    print('[+] Good: '+str(getGood(bitsTx, bitsRx)))
    print('[+] Errors (Total): '+str(code_Tx.size - getGood(code_Tx, code_Rx)))
    print('[+] Error probability (calculated): '+str((code_Tx.size - getGood(code_Tx, code_Rx))/code_Tx.size))


if __name__ == '__main__':
    scenario(prob=0.02, frame_len=20)
