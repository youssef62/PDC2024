import transmitter
import server_simulation
import receiver
import client
if __name__ == '__main__':
    # Parameters
    l = 12 # number of bits in each observation
    energy = 2000 # energy of the codewords for each observation
    input_string_40_chars = "saluttoutlemonde40charscestlaviehuhuhu12"
    output_file = "signal.txt"
    transmitter.transmitter(input_string_40_chars, l, energy, output_file)

    rcvd_signal_txt = "rcvd_signal.txt"
    #simulated server
    server_simulation.server_simulation(output_file, rcvd_signal_txt)
    #

    a = 0.6 # threshold for the decoding
    decoded_string = receiver.receiver(l, a, energy, rcvd_signal_txt)
