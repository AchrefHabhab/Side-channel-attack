import numpy as np
import time
from typing import Optional

def encrypt_ascii(scope, target, plaintext: bytearray, key: Optional[bytearray] = None, ack: bool = True):
    # Configure the oscilloscope for continuous (NORMAL) acquisition on Channel 1.
    scope.write(":WAVeform:SOURce CHANnel1")    # Select channel 1
    scope.write(":WAVeform:FORMat ASCii")          # Use ASCII format
    scope.write(":WAVeform:MODE NORMal")           # Set waveform mode to NORMAL (continuous)
    scope.write(":WAVeform:POINts 2000")           # Set number of points (adjust as needed)
    
    # Set encryption key if provided.
    if key:
        target.set_key(key, ack=ack)
    
    
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
    
    # Retrieve ASCII waveform data (which includes a header).
    ascii_data = scope.query(":WAVeform:DATA?")
    # Remove the SCPI header if present.
    if ascii_data.startswith('#'):
        # The character after '#' indicates how many digits describe the length.
        n = int(ascii_data[1])
        header_len = 2 + n  # '#' + digit + length field
        data_str = ascii_data[header_len:]
    else:
        data_str = ascii_data
    
    # Clean and split the data string.
    data_str = data_str.strip()
    # Assuming the data is comma separated.
    data_values_str = data_str.split(',')
    # Convert each value to float.
    waveform = np.array([float(x) for x in data_values_str if x.strip() != ''])



    
    # Read ciphertext from the target FPGA.
    ciphertext = target.simpleserial_read('r', target.output_len, ack=ack)
    
    # Return the converted voltage trace, raw waveform (as floats), and ciphertext.
    return  waveform, ciphertext
