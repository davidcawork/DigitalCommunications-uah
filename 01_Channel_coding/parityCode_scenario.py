#!/usr/bin/python3

from parityCode import ParityCode
from channel import Channel, randBits, getGood
import numpy as npy, random, time



def scenario(n=3, prob=0.02, frame_len = 10000):
    "Main method to simulate a noisy scenario using Parity codes"

    # Stats vars
    start_time = time.time()

    
    # Scenario behaviour
    print("Simulating Parity code scenario...\n")
    bitsTx  = randBits(frame_len)
    code_Tx = ParityCode.parityEncoder(bitsTx, n)
    code_Rx = Channel(prob).run(code_Tx)
    bitsRx,err_detected  = ParityCode.parityDecoder(code_Rx, n)

    # Print results
    print('------------------------------------')
    print('Time elapsed: '+str((time.time() - start_time)*1000) + ' ms')
    print('Frame length: '+str(frame_len))
    print('Repetition factor: '+str(n))
    print('Error probability: '+str(prob))
    print('\n------------ Results ---------------')
    print('[+] Total bits: '+str(frame_len))
    print('[+] Good: '+str(getGood(bitsTx,bitsRx)))
    print('[+] Errors (Total): '+str(code_Tx.size - getGood(code_Tx,code_Rx)))
    print('[+] Errors (Data): '+str(frame_len - getGood(bitsTx,bitsRx)))
    print('[+] Errors (Parity bits): '+str( (code_Tx.size - getGood(code_Tx,code_Rx)) - (frame_len - getGood(bitsTx,bitsRx))))
    print('[+] Errors detected: ' + str(err_detected))
    print('[+] Error probability (calculated): '+str((code_Tx.size - getGood(code_Tx,code_Rx))/code_Tx.size))
    print('[+] Non error detection probability (calculated): '+str(n*(n-1)*0.5*((code_Tx.size - getGood(code_Tx,code_Rx))/code_Tx.size)**2))



if __name__ == '__main__':
    scenario(n=3, prob=0.02, frame_len = 10000)