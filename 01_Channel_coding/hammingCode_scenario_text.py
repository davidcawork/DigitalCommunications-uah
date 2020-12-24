#!/usr/bin/python3


from hammingCode import HammingCode
from channel import Channel, randBits, getGood
import numpy as npy
import random
import time


def prepareBitStreamFromFile(file_data):
    bitsTx_stream = list()
    charsTx = [npy.binary_repr(char, 8) for char in npy.fromfile(file_data, dtype='uint8')]
    for char in charsTx:
        for bit in char:
            bitsTx_stream.append(bit)
    return bitsTx_stream


def saveIntoFile(bits, file_output):
    code = npy.array(bits)
    with open(file_output, "w+") as ofile:
        if not code.size % 8 == 0:
            code = HammingCode.zeroPadding(code, 8 - (code.size % 8))

        for char in npy.split(code, code.size / 8):
            ofile.write(chr(int(''.join(char.astype(str).tolist()), 2)))


def scenario(q=3, prob=0.02):
    "Main method to simulate a noisy scenario using Hamming codes"

    # Stats vars
    start_time = time.time()

    # Scenario behaviour
    print("Simulating Hamming code scenario...\n")
    HammingBlock = HammingCode(q=3)
    bitsTx = prepareBitStreamFromFile('data.txt')
    code_Tx = HammingBlock.hammingEncoder(bitsTx)
    code_Rx = Channel(prob).run(code_Tx)
    bitsRx, fixed = HammingBlock.hammingDecoder(code_Rx)

    # Print results
    print('------------------------------------')
    print('Time elapsed: '+str((time.time() - start_time)*1000) + ' ms')
    print('Frame length: '+str(len(bitsTx)))
    print('Repetition factor: '+str(q))
    print('Error probability: '+str(prob))
    print('\n------------ Results ---------------')
    print('[+] Total bits: '+str(len(bitsTx)))
    print('[+] Good: '+str(getGood(npy.array(bitsTx), bitsRx)))
    print('[+] Errors: '+str(code_Tx.size - getGood(code_Tx, code_Rx)))
    print('[+] Fixed: '+str(fixed))
    print('[+] Error probability (calculated): ' +
          str((code_Tx.size - getGood(code_Tx, code_Rx)) / code_Tx.size))

    # Save Received  file
    saveIntoFile(bitsRx, 'data_out.txt')


if __name__ == '__main__':
    scenario(q=3, prob=0.02)
