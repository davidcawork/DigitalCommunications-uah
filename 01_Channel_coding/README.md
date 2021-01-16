# Channel coding assignments

Different encoders can be found in this repository:

- Repetition Code
- Parity Code
- Hamming Code (Generic)
- Convolution Code
- Viterbi algorithm (with recursion)

In order to test the different classes developed, different scenarios have been indicated, where each encoder is used to transmit a binary message through a noisy channel (Simulated with the Channel class).

Additionally, a scenario has been made where the Hamming encoder (7,4) is tested with a plain text so that the effect of recovery to channel-induced random errors can be seen better. The results can be seen at [``data.txt``](data/data.txt) and [``data_out.txt``](data/data_out.txt)

An additional scenario has been added to allow testing of the convolution encoders and the convolution decoder with the Viterbi algorithm. It should be mentioned that since the Viterbi algorithm has been implemented with recursion, very large frame sizes cannot be introduced into the scenario, otherwise the stack will overflow resulting in unpredictable outputs. 

