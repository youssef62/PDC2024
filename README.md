# Principles of digital communication - Project 
**Authors**: 
- Mahdi Atallah 
- Youssef Boughizane 
- Yuri Chlebny 
- Thomas Muller
## Project description
Link to pdf file: [Project description](project-desc.pdf)

## System design 
1. Split the message into blocks of `k` bits. 
2. Encode each block with the method described in exercise 3. 
3. Concatenate the encoded blocks to form the transmitted signal. 
4. Send the signal through a channel.
5. Receive the signal and decode it block by block using the method described in exercise 3.

## Choice of constants
- Choosing `k`: Let us first notice that the size of transmitted message is given by: `len(message)` $= n = 2^{k-1} \cdot \frac{240}{k}$. Therefore, knowing that $n \leq 500000$ and $k>0$ and we find:
$$2^{k-1} \cdot \frac{240}{k} \leq 500000 \iff \frac{2^{k-1}}{k} \leq \frac{6250}{3}$$
By numerically testing values, we find that the biggest `k` that satisfies the above inequality is k = 16. Therefore, we must choose $0 < k \leq 16$.

## How to run the code 
You need to run the file `full_design,py` in order to run the code. 
Two command line arguments are required: 
- `--mode` followed by the chosen mode (`local`, `client` or `error_prob`) 
    - "local" mode is used to send a message on a simulated local channel. 
    - "client" mode is used to send a message to the provided server. 
    - "error_prob" mode is used to test the error probability of the channel(locally). 
- `--input_string` followed by the message you want to send. If not provided, the default message is `"saluttoutlemonde40charscestlaviehuhuhu12"`. Not required in the "error_prob" mode. 

Examples : 
1. `python full_design.py --mode local --input_string "1234567890123456789012345678901234567890"`
2. `python full_design.py --mode client --input_string "1234567890123456789012345678901234567890"`
3. `python full_design.py --mode error_prob`

## Code structure 
* `transmitter.py` : receives a message, encodes as described and outputs it to a file "client/transmitted_signal.txt" ("local/transmitted_signal.txt" in client mode). This file is then passed to the channel. 
* `receiver.py` : receives the signal from the channel, decodes it and outputs the decoded message to a file "client/received_message.txt" ("local/received_message.txt" in client mode).
* `full_design.py` : main file that describes the full communication system i.e runs the transmitter, channel and receiver.
