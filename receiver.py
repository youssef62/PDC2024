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
    chunks = np.array_split(sig, len(sig) // (2 ** (l - 1)))
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
            if max_index != -1:
                print("Error : multiple components larger than the threshold")
                return -1
            max_index = j
    if max_index == -1:
        print("Error : no component larger than the threshold")
        return -1
    print("Index of the largest component : ", max_index)
    # Since we have ordered the codewords in the codebook, we can directly return the index of the decided codeword
    if chunk[max_index] > 0:
        return 2* max_index
    else:
        return 2* max_index +1


def decode_signal(chunks, a, energy, sigma, tau):
    """
    We would like to be able to decide which part of the received signal is pure noise. To do so, we will use the
    method from ex.4. However, in exercise 4 the "chunks" were paired with the noise in the same vector, whereas here
    the chunks are either pure noise or contain a codeword. To make it equivalent, we will pair each chunk i with the
    n+i chunk, and apply the method from ex.4. Since either the first half of the total chunks or the second half will
    be pure noise, we know this pairing will ensure that we will always have a codeword and noise in the same pair.
    """
    decoded_chunks = []
    for chunk in chunks:
        i = decode_chunk_method_ex3(chunk, a, energy)
        if i == -1:
            print("Error : chunk can't be decoded.")
            continue
        decoded_chunks.append(i)
    #paired_chunks = []
    # for i in range(len(chunks) // 2):
    #     paired_chunks.append((chunks[i], chunks[i + len(chunks) // 2]))
    # decoded_chunks = []
    # for pair in paired_chunks:
    #     i1 = decode_chunk_method_ex3(pair[0], a, energy)
    #     i2 = decode_chunk_method_ex3(pair[1], a, energy)
    #     if i1 == -1 and i2 == -1:
    #         print("Error : both chunks can't be decoded.")
    #         return
    #     elif i1 == -1:
    #         decoded_chunks.append(i2)
    #     elif i2 == -1:
    #         decoded_chunks.append(i1)
        # else:
            # # Compute the distances to decide which one to keep
            # y1 = pair[0]
            # y2 = pair[1]
            # c_i1 = get_codeword_from_codebook(i1)
            # c_i2 = get_codeword_from_codebook(i2)
            # term1 = np.linalg.norm(y1 - c_i1) ** 2 / sigma ** 2
            # term2 = np.linalg.norm(y2) ** 2 / tau ** 2
            # d1 = term1 + term2
            # term1 = np.linalg.norm(y2 - c_i2) ** 2 / sigma ** 2
            # term2 = np.linalg.norm(y1) ** 2 / tau ** 2
            # d2 = term1 + term2
            # if d1 < d2:
            #     decoded_chunks.append(i1)
            # else:
            #     decoded_chunks.append(i2)
    return decoded_chunks


def un_chunk(decoded_chunks, l):
    """
    This function takes the decoded chunks and re-creates the string.
    :param decoded_chunks: the decoded chunks
    :param l: the number of bits in each chunk
    :return: the decoded string
    return decoded_string
    """
    decoded_string = ""
    alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 ."
    # convert back the chunks from decimal to binary
    binary_string = ""
    for chunk in decoded_chunks:
        base = '0' + str(l) + 'b'
        binary_string += format(chunk, base)
    print("Binary string : ", binary_string)
    # convert back the binary string to characters
    for i in range(0, len(binary_string), 6):
        decoded_string += alphabet[int(binary_string[i:i + 6], 2)]

    return decoded_string


if __name__ == '__main__':
    l = 4
    chunks = gather_signal(l, "rcvd_signal.txt")
    print("Received chunks : ", chunks)
    decoded_chunks = decode_signal(chunks, 0.9, 300000, 5, 5)
    decoded_string = un_chunk(decoded_chunks,l)
    print("Decoded string : ", decoded_string)

