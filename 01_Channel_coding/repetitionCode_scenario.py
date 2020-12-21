#!/usr/bin/python3

from repetitionCode import RepetitionCode
from channel import Channel
import numpy as npy, random, time


def randBits(size):
    "Method to create a random binary frame"

    frame = npy.zeros(size, dtype=npy.int32)
    frame[:random.randint(0,size)]  = 1
    npy.random.shuffle(frame)
    
    return frame

def getGood(secuence_src, secuence_dst):
    "Method to count how much bits of a secuence are equal"
    total_good = 0

    for i in range(0, secuence_src.size):
        if secuence_src[i] == secuence_dst[i]:
            total_good +=1

    return total_good


def scenario(n=3, prob=0.02, frame_len = 10000):
    "Main method to simulate a noisy scenario using Repetition codes"

    # Stats vars
    start_time = time.time()

    
    # Scenario behaviour
    print("Simulating Repetition code scenario...\n")
    bitsTx  = randBits(frame_len)
    code_Tx = RepetitionCode.repetitionEncoder(bitsTx, n)
    code_Rx = Channel(prob).run(code_Tx)
    bitsRx  = RepetitionCode.repetitionDecoder(code_Rx, n)

    # Print results
    print('------------------------------------')
    print('Time elapsed: '+str((time.time() - start_time)*1000) + ' ms')
    print('Frame length: '+str(frame_len))
    print('Repetition factor: '+str(n))
    print('Error probability: '+str(prob))
    print('\n------------ Results ---------------')
    print('[+] Total bits: '+str(frame_len))
    print('[+] Good: '+str(getGood(bitsTx,bitsRx)))
    print('[+] Errors: '+str(code_Tx.size - getGood(code_Tx,code_Rx)))
    print('[+] Fixed: '+str(code_Rx.size - getGood(code_Rx,npy.repeat(npy.array(bitsRx), n))))
    print('[+] Error probability (calculated): '+str((code_Tx.size - getGood(code_Tx,code_Rx))/code_Tx.size))



if __name__ == '__main__':

    scenario(n=3, prob=0.02, frame_len = 10000)