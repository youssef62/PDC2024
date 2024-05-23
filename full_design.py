import transmitter
import server_simulation
import receiver
import client




def send_locally(input_string_40_chars): 
    l = 12 # number of bits in each observation
    energy = 2000 # energy of the codewords for each observation
    output_file = "local/transmitted_signal.txt"
    transmitter.transmitter(input_string_40_chars, l, energy, output_file)

    rcvd_signal_txt = "local/rcvd_signal.txt"
    #simulated server
    server_simulation.server_simulation(output_file, rcvd_signal_txt)
    #

    a = 0.6 # threshold for the decoding
    decoded_string = receiver.receiver(l, a, energy, rcvd_signal_txt)
    
    print("Decoded string : ", decoded_string)
    
    if input_string_40_chars == decoded_string:
        print("The decoded string is correct")
    else:
        print("The decoded string is incorrect") 
        
    return decoded_string

if __name__ == '__main__':
    input_string_40_chars = "saluttoutlemonde40charscestlaviehuhuhu12"
    send_locally(input_string_40_chars)
