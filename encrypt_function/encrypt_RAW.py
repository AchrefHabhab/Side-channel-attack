import numpy as np
import time
from typing import Optional

def encrypt_2(scope, target, plaintext: bytearray, key: Optional[bytearray] = None, ack: bool = True):
    # --- Configure the oscilloscope channel for small signals around 0 V ---
    # AC coupling removes large DC offsets automatically.
    scope.write(":CHANnel1:COUPling AC")  
    # Ensure no additional offset is applied.
    scope.write(":CHANnel1:OFFSet 0")     
    # Set a low vertical scale (e.g., 10 mV/div). Adjust as needed.
    scope.write(":CHANnel1:SCALe 0.01")   
    # Use NORMAL mode for continuous acquisition on Channel 1.
    scope.write(":WAVeform:SOURce CHANnel1")   
    scope.write(":WAVeform:FORMat BYTE")         
    scope.write(":WAVeform:MODE NORMal")         
    # Adjust the memory points as needed.
    scope.write(":WAVeform:POINts 2000")         

    # If a new encryption key is provided, set it on the target.
    if key:
        target.set_key(key, ack=ack)
    
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
    
    # Retrieve binary waveform data (raw ADC counts).
    raw_waveform = scope.query_binary_values(":WAVeform:DATA?", datatype='B', container=np.array)
    print("Raw waveform (ADC counts):", raw_waveform)
    
    # Retrieve the preamble for conversion parameters.
    preamble_str = scope.query(":WAVeform:PREamble?")
    # The preamble is typically: format, type, points, count, xincrement, xorigin,
    # xreference, yincrement, yorigin, yreference
    print("Preamble:", preamble_str)
    params = preamble_str.split(',')
    if len(params) < 10:
        print("Error: Unexpected preamble format")
        return None
    
    # Parse the Y conversion parameters
    _, _, _, _, _, _, _, yincrement, yorigin, yreference = params
    yincrement = float(yincrement)
    yorigin    = float(yorigin)
    yreference = float(yreference)
    
    # Convert raw ADC counts to volts
    voltage_trace_volts = (raw_waveform - yreference) * yincrement + yorigin
    
    # Convert volts to millivolts
    voltage_trace_mV = voltage_trace_volts * 1e3
    print("Converted voltage trace (mV):", voltage_trace_mV)
    
    # Read ciphertext from the target FPGA.
    ciphertext = target.simpleserial_read('r', target.output_len, ack=ack)
    
    # Return the converted voltage trace (mV), raw waveform, and ciphertext.
    return voltage_trace_mV, raw_waveform, ciphertext