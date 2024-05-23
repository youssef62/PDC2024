import transmitter
import server_simulation
import receiver
import client
import random
import string 



def send_locally(input_string_40_chars,Verbose=True): 
    l = 12 # number of bits in each observation
    energy = 2000 # energy of the codewords for each observation
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

def estimate_error_prob(): 
    alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 ." 
    n_samples = 1000  
    error_count = 0 
    for i in range(n_samples): 
        if i % 10 == 0: 
            print("Sample ", i) 
        msg = ''.join(random.choices(alphabet,k=40)) 
        decoded = send_locally(msg,Verbose=False)
        error_count += int(msg != decoded) 
    return error_count / n_samples 
        
if __name__ == '__main__':
    # input_string_40_chars = "saluttoutlemonde40charscestlaviehuhuhu12"
    # send_locally(input_string_40_chars)
   
    print("Estimated error probabilty: ", estimate_error_prob()) 
    
