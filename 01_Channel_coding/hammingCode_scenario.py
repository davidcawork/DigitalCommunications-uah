#!/usr/bin/python3

from HammingEncoding.hammingCode import HammingCode
from channel import Channel, randBits, getGood
import numpy as npy
import random
import time


def scenario(q=3, prob=0.02, frame_len=10000):
    "Main method to simulate a noisy scenario using Hamming codes"

    # Stats vars
    start_time = time.time()

    # Scenario behaviour
    print("Simulating Hamming code scenario...\n")
    HammingBlock = HammingCode(q=3)
    bitsTx = randBits(frame_len)
    code_Tx = HammingBlock.hammingEncoder(bitsTx)
    code_Rx = Channel(prob).run(code_Tx)
    bitsRx, fixed = HammingBlock.hammingDecoder(code_Rx)

    # Print results
    print('------------------------------------')
    print('Time elapsed: '+str((time.time() - start_time)*1000) + ' ms')
    print('Frame length: '+str(frame_len))
    print('Repetition factor: '+str(q))
    print('Error probability: '+str(prob))
    print('\n------------ Results ---------------')
    print('[+] Total bits: '+str(frame_len))
    print('[+] Good: '+str(getGood(bitsTx, bitsRx)))
    print('[+] Errors: '+str(code_Tx.size - getGood(code_Tx, code_Rx)))
    print('[+] Fixed: '+str(fixed))
    print('[+] Error probability (calculated): ' +
          str((code_Tx.size - getGood(code_Tx, code_Rx))/code_Tx.size))


if __name__ == '__main__':
    scenario(q=3, prob=0.02, frame_len=10000)
