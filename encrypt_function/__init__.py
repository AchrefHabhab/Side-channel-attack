
def capture_trace_oscill(oscope, target, plaintext: bytearray, key: Optional[bytearray] = None, ack: bool = True, poll_done: bool = False, as_int: bool = False, always_send_key: bool = False) -> Optional[Trace]:
    """
    Capture a trace using the Keysight oscilloscope.

    Args:
        oscope: Oscilloscope object (pyvisa resource).
        target: Target object (CW305 FPGA target).
        plaintext: Plaintext to send to the target.
        key: Key to send to the target.
        ack: Check for ack when reading response from target.
        poll_done: Poll the oscilloscope to find out when it's done capturing.
        as_int: If False, return trace as a float. Otherwise, return as an int.
        always_send_key: If True, always send key. Otherwise, only send if the key is different from the last one sent.

    Returns:
        Trace object or None if capture timed out.
    """
    import signal

    if key:
        target.set_key(key, ack=ack, always_send=always_send_key)

    # Arm the oscilloscope
    oscope.write(":TRIGger:SWEep NORMal")  # Set trigger mode to normal
    oscope.write(":DIGitize CHANnel1")  # Digitize the signal on channel 1

    if plaintext:
        target.simpleserial_write('p', plaintext)

    # Wait for the oscilloscope to capture the trace
    #time.sleep(0.1)  # Adjust this delay as needed

    # Check if the oscilloscope has finished capturing

    # Read the trace data from the oscilloscope
    oscope.query('*OPC?')
    oscope.write(":WAVeform:SOURce CHANnel1")
    oscope.write(":WAVeform:FORMat ASCii")
    trace_data = oscope.query(":WAVeform:DATA?")
    trace_data = trace_data.strip().split(',')
    trace_data = np.array([float(x) for x in trace_data])

    # Read the response from the target
    response = target.simpleserial_read('r', target.output_len, ack=ack)

    if len(trace_data) >= 1:
        return Trace(trace_data, plaintext, response, key)
    else:
        return None
    
import numpy as np
import time
from typing import Optional

def encrypt_1(scope, target, plaintext: bytearray, key: Optional[bytearray] = None, ack: bool = True):
    # Configure the oscilloscope for continuous (NORMAL) acquisition on Channel 1.
    scope.write(":WAVeform:SOURce CHANnel1")   # Select Channel 1
    scope.write(":WAVeform:FORMat BYTE")         # Use binary format for efficient data transfer
    scope.write(":WAVeform:MODE NORMal")         # Set waveform mode to NORMAL (continuous)
    scope.write(":WAVeform:POINts 2000")         # Set number of points (adjust as needed)
    
    # Set encryption key if provided.
    if key:
        target.set_key(key, ack=ack)
    
    # Check initial trigger status.
    print("Old trigger status is:", scope.query(":TRIGger:STATus?"))
    
    # Send plaintext for encryption.
    target.simpleserial_write('p', plaintext)
    
    # Start capturing waveform.
    scope.write(":DIGitize")
    
    # Wait until the target encryption operation is complete.
    i = 0
    while not target.is_done():
        time.sleep(0.05)  # Wait 50 ms between checks.
        i += 1
        if i > 100:  # Timeout after ~5 seconds.
            print("Warning: Target did not finish operation")
            return None
    
    # In NORMAL mode, the scope is continuously running and automatically decimates the data,
    # so we can directly query the waveform data without stopping the scope.
    raw_waveform = scope.query_binary_values(":WAVeform:DATA?", datatype='B', container=np.array)
    print("Captured waveform:", raw_waveform)
    
    # Read ciphertext from the target FPGA.
    ciphertext = target.simpleserial_read('r', target.output_len, ack=ack)
    
    return raw_waveform, ciphertext



