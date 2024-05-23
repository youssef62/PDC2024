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
    :param l: the number of bits in each observation
    :param signal: the path to the .txt file containing the signal
    :return: the observations i.e a list of the noised versions of the all the received codewords
    """
    sig = np.loadtxt(signal)
    # Since the codewords are in Rn, with n = 2**(l-1), we need to gather the components of each codeword
    # by taking the first n components, then the next n components and so on.
    observations = np.array_split(sig, len(sig) // (2 ** (l - 1)))
    return observations


def decode_obs_method_ex3(observation, a, energy):
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
    for j in range(len(observation)):
        if abs(observation[j]) > t:
            if max_index != -1:
                #print("Error : multiple components larger than the threshold")
                return -1
            max_index = j
    if max_index == -1:
        #print("Error : no component larger than the threshold")
        return -1
    # Since we have ordered the codewords in the codebook, we can directly return the index of the decided codeword
    if observation[max_index] > 0:
        return 2* max_index
    else:
        return 2* max_index +1


def decode_signal(observations, a, energy):
    """
    This function decodes the observations (list of codewords) using the decoding scheme of ex. 3. If the observation can't be decoded, we skip it.
    """
    decoded_observations = []
    for observation in observations:
        i = decode_obs_method_ex3(observation, a, energy)
        if i == -1:
            #print("Error : observation can't be decoded.")
            continue
        decoded_observations.append(i)
    return decoded_observations



def recreate_string(decoded_observations, l):
    """
    This function takes the decoded observations (list of indices of codewords) and re-creates the string.
    :param decoded_observations: the list of decided codewords
    :param l: the number of bits used for chunking the string
    :return: the decoded string
    return decoded_string
    """
    decoded_string = ""
    alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 ."
    # convert back the index of codewords from decimal to binary
    binary_string = ""
    for codeword in decoded_observations:
        base = '0' + str(l) + 'b'
        binary_string += format(codeword, base)
    # convert back the binary string to characters
    for i in range(0, len(binary_string), 6):
        decoded_string += alphabet[int(binary_string[i:i + 6], 2)]

    return decoded_string

def receiver(l, a, energy, rcvd_signal_txt):
    chunks = gather_signal(l, rcvd_signal_txt)
    decoded_obs = decode_signal(chunks, a, energy)
    decoded_string = recreate_string(decoded_obs, l)
    print("Decoded string : ", decoded_string)


