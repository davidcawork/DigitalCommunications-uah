#!/usr/bin/python3

from repetitionCode import RepetitionCode

if __name__ == '__main__':

    print(RepetitionCode.repetitionEncoder([1 , 0, 1], 3))

    print(RepetitionCode.repetitionDecoder([1,1,1,0,0,1,1,1,1], 3))