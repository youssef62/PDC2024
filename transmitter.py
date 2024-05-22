"""
    This module takes an input string and generates a .txt that can then be used in client.py
    to be sent.
    The chosen encoding scheme is the one from exercise 3 in the theory :
    1) we encode each character in the string as a 6 bit binary number, then we concatenate all the binary numbers.
    2) we split this long binary number into l-bit chunks, l is arbitrary (optimal l is to be computed analytically).
    3) we convert each l-bit chunk into a decimal number, that will be the index of the codeword in the codebook for the chunks.
    4) we save the decimal numbers in a .txt file.
    Note : the codebook is generated in the function generate_codebook.
    That way, we have generated a n/l dimension vector that can be sent to the server.
    Version: 1.0, yuri
"""

import numpy as np

def chunk_string(input_string, l):
    """
    This functions splits a string into chunks. Each chunk is then encoded as a decimal number which is the index of the
    codeword in the codebook.
    :param input_string: the string to encode
    :param l: the number of bits in each chunk
    :return: the encoded string
    """
    # Step 1, encoding each character in the string as a 6 bit binary number
    binary_string = ""
    for char in input_string:
        binary_string += format(ord(char), '06b')
    # Step 2, splitting the binary string into l-bit chunks
    chunks = [binary_string[i:i+l] for i in range(0, len(binary_string), l)]
    # Step 3, converting each chunk into a decimal number (we will generate the codebook later)
    chunked_string = []
    for chunk in chunks:
        chunked_string.append(int(chunk, 2))
    return chunked_string

def generate_codebook(l,energy=40960):
    """
    This function generates the codebook for each chunk according to the encoding scheme of ex. 3.
    :param l: the number of bits in each chunk
    :param energy: the energy of the codewords, default is max Energy = 40960.
    Consider a communication system with 2n equally likely codewords ± sqrt(Energy) * ej,
    j = 1, . . . , n where e1, . . . , en are the unit coordinate vectors in Rn
    """
    codebook = {}
    n = 2**(l-1) # we have 2**l possible codewords, but in the notation of ex.3 we say we have 2n codewords
    for i in range(2*n): # iterate over the 2n codewords
        codebook[i] = np.sqrt(energy) * np.array([1 if j == i else 0 for j in range(2*n)])
    # for each line in the codebook, save the corresponding codeword in a line of the .txt file
    np.savetxt("codebook_for_chunks.txt", list(codebook.values()), fmt='%d')

def create_signal(chunked_string, output_file):
    """
    This function creates the signal that will be sent to the server. It takes the chunks that contains the
    indices of the corresponding codewords and the codebook. It generates the signal by putting each codeword in
    a different line of the .txt file.
    :param chunked_string: the string containing the indices of the codewords
    :param output_file: the path to the .txt file that will contain the signal
    """
    # retrieve the codebook and the energy from the txt file
    codebook = np.loadtxt("codebook_for_chunks.txt")
    signal = []
    for index in chunked_string:
        signal.append(codebook[index])
    np.savetxt(output_file, signal, fmt='%d')

if __name__ == '__main__':
    input_string_40_chars = "Hello, this is a test string with 40 characters."
    l = 4
    energy = 40960
    generate_codebook(l, energy)
    chunked_string = chunk_string(input_string_40_chars, l)
    create_signal(chunked_string, "signal.txt")
    print("Encoded string saved in signal.txt")
