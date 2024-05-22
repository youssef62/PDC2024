"""
    This module takes the received file, applies the decoding scheme and outputs the decoded string.
    Now, either the first or the second half of the received vector is pure noise. To decide which, we will
    apply the technique from ex. 4. However, instead of computing the argmin for each codeword, we will
    use the decoding scheme from ex.3 on each half of the received vector

    Version: 1.0, yuri
"""
import numpy as np

def decode_chunk(received_chunk,a):
    """
    This function decodes a received chunk using the decoding scheme described in the file header.
    :param received_chunk: the received chunk to decode
    :return: the decoded chunk

    method from ex.3 :
    Consider the following alternative decoding method. Pick a threshold t = α*sqrt(Energy) with
    0 <= α < 1. If there is exactly one j for which |Yj| > t, decide that the codeword sign(Yj)*Energy*ej was transmitted
    """
    # retrieve the codebook from the txt file
    codebook = np.loadtxt("codebook_for_chunks.txt")
    # retrieve the energy from the first line of the txt file
    energy = codebook[0]
    # compute the threshold
    t = a * np.sqrt(energy)
    # decode the chunk
    decoded_chunk = []
    n = 2**(len(received_chunk)-1) # Again, we have 2**l (l is the length of the chunk) possible codewords,
    # but in the notation of ex.3 we say we have 2n codewords

