# ############################################################################
# client.py
# =========
# Author : Sepand KASHANI [sepand.kashani@epfl.ch]
# ############################################################################

import struct
import numpy as np
import io
import socket
import errno


def send_msg(sock, header, data):
    """
    Send a packet over the network.

    Parameters
    ----------
    sock : :py:class:`~socket.socket`
    header : bytes
        (4,) byte string.
    data : :py:class:`~numpy.ndarray`
    """
    if len(header) != 4:
        raise ValueError('Parameter[header]: expected byte() of length 4.')

    with io.BytesIO() as f:
        np.save(f, data)
        byte_data = f.getvalue()

    # Pack message length
    msg = (struct.pack('>I', len(header) + len(byte_data)) +
           header + byte_data)
    # sock.sendall(msg)
    try:
        sock.sendall(msg)
    except socket.error as e:
        if e.errno != errno.EPIPE:
            # Not a broken pipe
            pass

def recv_msg(sock, N_byte_max=None):
    """
    Receive a packet from the network.

    Parameters
    ----------
    sock : :py:class:`~socket.socket`
    N_byte_max : int
        Maximum number of bytes to accept. (None = unlimited.)
        :py:class:`RuntimeError` raised if threshold exceeded.

    Returns
    -------
    header : bytes
        (4,) byte string
    data : :py:class:`~numpy.ndarray`
    """
    if (N_byte_max is not None):
        if not (N_byte_max > 0):
            raise TypeError('Parameter[N_byte_max] must be positive.')
    else:
        N_byte_max = np.inf

    # Extract message length
    N_msg_raw = recv_bytes(sock, 4)
    N_msg = struct.unpack('>I', N_msg_raw)[0]  # bytes

    msg = recv_bytes(sock, N_msg)
    header = msg[:4]
    with io.BytesIO(msg[4:]) as f:
        data = np.load(f)
    return header, data

def recv_bytes(sock, N_byte):
    """
    Receive bytes from the network.

    Parameters
    ----------
    sock : :py:class:`~socket.socket`
    N_byte : int
        Number of bytes to read.

    Returns
    -------
    byte_data : bytes
        (N_byte,)
    """
    packet_size = 2 ** 12

    packets, N_byte_read = [], 0
    while N_byte_read < N_byte:
        packet = sock.recv(min(packet_size, N_byte - N_byte_read))
        packets.append(packet)
        N_byte_read += len(packet)

    byte_data = b''.join(packets)
    return byte_data
