"""
    This module takes the received file, applies the decoding scheme and outputs the decoded string.
    Now, since we had to "spread" the codewords in the signal, we need to "gather" the components of each codeword
    and re-create the chunks. Because of the channel, half the chunks will be pure noise.
    Version: 1.0, yuri
"""
import numpy as np
def get_codeword_from_codebook(index):
    """
    This function retrieves the codeword from the codebook given its index.
    :param index: the index of the codeword
    :return: the codeword
    """
    codebook = np.loadtxt("codebook_for_chunks.txt")
    return codebook[index]
def gather_signal(l, signal):
    """
    This function gathers the components of each codeword in the signal and re-creates the chunks.
    :param l: the number of bits in each chunk
    :param signal: the path to the .txt file containing the signal
    :return: the chunks
    """
    sig = np.loadtxt(signal)
    # Since the codewords are in Rn, with n = 2**(l-1), we need to gather the components of each codeword
    # by taking the first n components, then the next n components and so on.
    chunks = np.array_split(sig, len(sig)//(2**(l-1)))
    return chunks
def decode_chunk_method_ex3(chunk, a, energy):
    """
    Pick a threshold t = α*sqrt(Energy) with 0<= α < 1. If there is exactly one j for which |Yj| > t,
    decide that the codeword sign(Yj)*Energy*ej was transmitted. If there is no j for which |Yj| > t or several j’s for
    which |Yj| > t, then the decoder declares an error.
    """
    t = a * np.sqrt(energy)
    # we need to find the index of the component that is the largest in absolute value
    # if there is exactly one component that is larger than t, we return its index
    # otherwise we return an error
    max_index = -1
    for j in range(len(chunk)):
        if abs(chunk[j]) > t:
                max_index = j
    if max_index == -1:
        print("Error : no component larger than the threshold")
        return -1
    return max_index

def decode_signal(chunks, a, energy, sigma, tau):
    """
    We would like to be able to decide which part of the received signal is pure noise. To do so, we will use the
    method from ex.4. However, in exercise 4 the "chunks" were paired with the noise in the same vector, whereas here
    the chunks are either pure noise or contain a codeword. To make it equivalent, we will pair each chunk i with the
    n+i chunk, and apply the method from ex.4. Since either the first half of the total chunks or the second half will
    be pure noise, we know this pairing will ensure that we will always have a codeword and noise in the same pair.
    """
    paired_chunks = []
    for i in range(len(chunks)//2):
        paired_chunks.append((chunks[i], chunks[i+len(chunks)//2]))
    decoded_chunks = []
    for pair in paired_chunks:
        i1 = decode_chunk_method_ex3(pair[0], a, energy)
        i2 = decode_chunk_method_ex3(pair[1], a, energy)
        # Compute the distances to decide which one to keep
        y1 = pair[0]
        y2 = pair[1]
        c_i1 = get_codeword_from_codebook(i1)
        c_i2 = get_codeword_from_codebook(i2)
        term1 = np.linalg.norm(y1 - c_i1) ** 2 / sigma ** 2
        term2 = np.linalg.norm(y2) ** 2 / tau ** 2
        d1 = term1 + term2
        term1 = np.linalg.norm(y2 - c_i2) ** 2 / sigma ** 2
        term2 = np.linalg.norm(y1) ** 2 / tau ** 2
        d2 = term1 + term2
        if d1 < d2:
            decoded_chunks.append(i1)

        else:
            decoded_chunks.append(i2)
    return decoded_chunks
def un_chunk(decoded_chunks):
    """
    This function takes the decoded chunks and re-creates the string.
    :param decoded_chunks: the decoded chunks
    :return: the decoded string
    return decoded_string
    """
    decoded_string = ""
    alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 ."
    for chunk in decoded_chunks:
        decimal = chunk
        print("Decimal : ", decimal)
        char = alphabet[decimal]
        print("Char : ", char)
        decoded_string += char
    return decoded_string

if __name__ == '__main__':
    chunks = gather_signal(4, "rcvd_signal.txt")
    print("We received this many chunks : ", len(chunks))
    print("Chunks : ", chunks)
    decoded_chunks = decode_signal(chunks, 0, 3000, 25, 25)
    decoded_string = un_chunk(decoded_chunks)
    print("Decoded string : ", decoded_string)


