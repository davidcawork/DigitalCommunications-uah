#!/usr/bin/python3

from repetitionCode import RepetitionCode
from channel import Channel


if __name__ == '__main__':

    print(RepetitionCode.repetitionEncoder([1 , 0, 1], 3))
    
    a = Channel(0.1).run(RepetitionCode.repetitionEncoder([1 , 0, 1], 3))
    print(a)

    print(RepetitionCode.repetitionDecoder(a, 3))