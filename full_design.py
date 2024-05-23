import transmitter
import server_simulation
import receiver

if __name__ == '__main__':
    # Parameters
    l = 6 # number of bits in each observation
    energy = 900 # energy of the codewords for each observation
    input_string_40_chars = "proutproutproutprouthahahahahapipicacaca"
    output_file = "signal.txt"

    transmitter.transmitter(input_string_40_chars, l, energy, output_file)
    rcvd_signal_txt = "rcvd_signal.txt"
    server_simulation.server_simulation(output_file, rcvd_signal_txt)

    a = 0.6 # threshold for the decoding
    decoded_string = receiver.receiver(l, a, energy, rcvd_signal_txt)
