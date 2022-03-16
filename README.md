# OFDM-System

This project was created to simulate a data transmission from a ofdm - transmitter over a awgn channel to a ofdm receiver.

For some example plots --> Documentation 
(not much yet) 


## Run Program
 make shure you installed Numpy and Matplotlib


```bash
> cd OFDM_Systems
> python OFDM_System.py
```

## Basic features:

- 16QAM IQ - Mapper,
- OFDM Modem 
- IQ Modulator that creates real bandpass signals (analytic low pass signal <-> bandpasssignal) 
- Spectrum - Analyser and Scope,
- Dynmaic spectrum and signal visualization 
- Simulation of CFO - distortions 
- guard interval options for intermodulation protection
- BER / BEP measuring.

## Future Features (in progress...)
   - Signal Processing:
        - PHY:
            - QPSK preamble
            - Scrambler
            - FEC
                - Interleaver
                - RS - Codec ?? 
            - adaptive modulation scheme based on the transmission channel properties 
    
   - Software features: 
        - use Python Dispatcher for an event - based solution (simulating interrupts)
        - Server/Client model
        - Server (Python): signal processing
        - Client:
           - Website with Flask or Dash 

## License
No Licence required

## Author: 

Paul Vielhauer (@paulvielhauer@outlook.de) 
