import transmitter
import server_simulation
import receiver
import client
import random
import string 
import os 
import argparse 

def send_locally(input_string_40_chars,Verbose=True): 
    """
    Local simulation of the communication system. The input string is encoded, sent to the server, 
    received and decoded. The decoded string is then compared to the input string.
    :param input_string_40_chars: the string to encode
    :param Verbose: if True, the decoded string is printed and compared to the input string
    :return: the decoded string
    """
    l = 12 # number of bits in each observation
    energy = 2110 # energy of the codewords for each observation
    output_file = "local/transmitted_signal.txt"
    transmitter.transmitter(input_string_40_chars, l, energy, output_file, verbose=Verbose)

    rcvd_signal_txt = "local/rcvd_signal.txt"
    #simulated server
    server_simulation.server_simulation(output_file, rcvd_signal_txt)
    #

    a = 0.6 # threshold for the decoding
    decoded_string = receiver.receiver(l, a, energy, rcvd_signal_txt)
    
    if Verbose:
        print("Decoded string : ", decoded_string)
        
        if input_string_40_chars == decoded_string:
            print("The decoded string is correct")
        else:
            print("The decoded string is incorrect") 
            
    return decoded_string

def estimate_error_prob(n_samples): 
    """
    Estimate the error probability of the communication system by sending n_samples random messages. 
    :param n_samples: the number of samples to send
    :return: the estimated error probability 
    """
    alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 ." 
    error_count = 0 
    for i in range(n_samples): 
        if i % 10 == 0: 
            print("Sample ", i) 
        msg = ''.join(random.choices(alphabet,k=40)) 
        decoded = send_locally(msg,Verbose=False)
        error_count += int(msg != decoded) 
    return error_count / n_samples 
 
 
def send_over_client(input_string_40_chars,Verbose=True): 
    """
    Send the input string to the server using the client. 
    :param input_string_40_chars: the string to send 
    :param Verbose: if True, the decoded string is printed and compared to the input string 
    :return: the decoded string 
    """ 
    l = 12 # number of bits in each observation 
    energy = 2110 # energy of the codewords for each observation 
    output_file = "client/transmitted_signal.txt"
    transmitter.transmitter(input_string_40_chars, l, energy, output_file, verbose=Verbose)

    os.system("python client.py --input_file=client/transmitted_signal.txt --output_file=client/rcvd_signal.txt --srv_hostname=iscsrv72.epfl.ch --srv_port=80 ") 
    rcvd_signal_txt = "client/rcvd_signal.txt"
    a = 0.6 # threshold for the decoding
    decoded_string = receiver.receiver(l, a, energy, rcvd_signal_txt)
    if Verbose:
        print("Decoded string : ", decoded_string)
        if input_string_40_chars == decoded_string:
            print("The decoded string is correct")
        else:
            print("The decoded string is incorrect")
             
           
if __name__ == '__main__':
    
    # command line argument, first one is the mode 
    parser = argparse.ArgumentParser(description='Full design of the communication system')
    parser.add_argument('--mode', type=str, help='local or client or error_prob')
    parser.add_argument('--input_string', type=str, help='the input string to send') 
    
    args = parser.parse_args()
    
    input_string_40_chars = args.input_string 
    if args.input_string is None and args.mode != "error_prob": 
        input_string_40_chars = "saluttoutlemonde40charscestlaviehuhuhu12"
    
    
    if args.mode == "local":
        send_locally(input_string_40_chars) 
    elif args.mode == "client": 
        send_over_client(input_string_40_chars)
    elif args.mode == "error_prob":
        print("Estimated error probabilty: ", estimate_error_prob(100))

    
