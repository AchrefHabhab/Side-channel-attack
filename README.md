# 🔐 Side-Channel Attack on AES using ChipWhisperer CW305 & External Oscilloscopes

This project demonstrates a side-channel attack (SCA) on AES-128 encryption using the ChipWhisperer CW305 FPGA target. Instead of using the default capture board, we used external oscilloscopes to acquire traces, developed custom waveform acquisition functions, and performed a CPA attack to extract encryption key information.

---

## 📁 Project Structure

```
cw305-sidechannel-attack/
├── notebooks/             # Jupyter notebooks for trace capture and conversion
│   └── main.ipynb         # Main notebook for acquisition and .mat conversion
│
├── encrypt_function/      # Modified capture functions for ASCII and RAW formats
│   ├── encrypt_ascii.py
│   └── encrypt_RAW.py
│
├── matlab/                # MATLAB CPA script
│   └── simple_cpa.m
│
├── data/                  # Saved capture results and visualization
│   ├── attack_data_all_ascii.mat
│   └── raw_trace_plots/
│       └── capturedTracePlot.png
│
├── images/                # Images used for README or reports
│   └── oscilloscope_setup.png
│
├── README.md              # Project documentation
├── requirements.txt       # Python dependencies
└── .gitignore             # Files to ignore in version control
```
---

## 🎯 Project Objective

To apply side-channel techniques on an FPGA-based AES implementation using the CW305. Our goal was to extract power traces during encryption and analyze them to recover the secret key using Correlation Power Analysis (CPA).

---

## 🧰 Hardware Used

- 🧩 **ChipWhisperer CW305**: FPGA target with Artix-7 for AES execution.
- 📡 **RIGOL MSO5074**: Used for ASCII waveform acquisition via SCPI.
- 🧪 **Keysight MSOX3104T**: Used for RAW waveform acquisition.
- 🔌 USB connection to oscilloscope via SCPI (VISA).
- 💻 **Host PC** running Python and MATLAB.

---

## 🛠️ Software Used

- **ChipWhisperer Toolchain**: [GitHub](https://github.com/newaetech/chipwhisperer)
- **Python 3.10**
- **PyVISA** for SCPI commands
- **UltraSigma (Rigol)**: Required for scope detection: [Download](https://intsso.rigol.com/En/Index/listView/catid/28/tp/5/wd/)
- **MATLAB** for CPA analysis
- Required Python libraries in `requirements.txt`

---

## 🔧 Custom `encrypt` Functions

To capture power traces directly from an external oscilloscope, we created two custom `encrypt` functions:

- `encrypt_ascii`: Captures waveform in ASCII format from the oscilloscope.
- `encrypt_RAW`: Captures raw binary waveform data and converts it using preamble information.

These functions are placed inside the `encrypt_function/` directory of this repository for clarity and reusability.

### 📌 Integration with ChipWhisperer Toolchain

To use these functions within the ChipWhisperer Python environment, they must be **added manually** to the ChipWhisperer toolchain:

**Path:**

ChipWhisperer5_64\cw\home\portable\chipwhisperer\software\chipwhisperer_init_.py


At the bottom of the file or inside the relevant utility function section, you can copy the functions


⚠️ **Important:** After editing this file, make sure to restart your Python environment or Jupyter kernel to ensure the new functions are properly loaded and usable.

---

## 📈 Trace Capture Workflow

- Fixed AES key: `2b7e151628aed2a6abf7158809cf4f3c`
- 10,000 traces collected via `main.ipynb`
- Each trace linked with corresponding ciphertext
- All saved in `.mat` format for MATLAB use

---

## 🤖 MATLAB CPA Attack

The `simple_cpa.m` script:

- Loads traces and ciphertexts from `.mat` file
- Applies multiple leakage models (HW, MSB, LSB, etc.)
- Computes Pearson correlation per key guess
- Ranks candidates and visualizes the best correlations

---

## 📌 Why 10,000 Traces?

To overcome noise and limited sampling resolution in external scopes, a large number of traces was necessary to provide usable signal for analysis.

---

## ❗ Challenges Faced

- **⚙️ Trigger Configuration**: No trigger initially appeared on the oscilloscope. Required deep understanding of SCPI and waveform mode settings to synchronize scope with encryption.
- **🔧 Bitstream Debugging**: Building custom bitstream with routed trigger to T13 took extensive work in Vivado to enable TP1 as a trigger output.
- **📉 Weak Leakage Detection**: Several leakage models (`last_round_state_diff`, `mix_columns_output`) failed to recover key accurately. Correlation values remained low despite valid acquisition setup.
- **🧪 Extensive Experimentation**: Each configuration needed hundreds or thousands of traces; testing new hypotheses was time-consuming.

---

## 📌 Code Overview

- Configure FPGA and scope in `main.ipynb`
- Use `encrypt_ascii()` or `encrypt_RAW()` to acquire traces
- Save all traces and ciphertexts in MATLAB format
- Run `simple_cpa.m` to perform attack using HW or custom leakage model

---

## 🧠 For Future Students

This repo is a solid foundation for further exploration in hardware security. Even though the key recovery wasn’t successful due to signal leakage limits, this setup captures valid traces and models a full SCA pipeline. Future improvements could include:

- 🧬 Enhancing SNR via filtering or averaging
- 🧠 Exploring machine learning-based SCA
- 🔑 Testing better-aligned leakage models
- 🔁 Extending to other crypto algorithms (RSA, ECC, SHA)

---

## 🙏 Acknowledgements

- 📘 Professor Athanasios Papadimitriou — for his original CPA lab code and guidance.
- 🛠️ NewAE Technology — for the ChipWhisperer open-source platform.
- 🙌 All teammates — for the weeks of work debugging bitstreams, trigger alignment, and SCPI protocols.

---

## 📜 License

This project is licensed under the University of Passau License.  

---

## ❓ Questions?

For any questions, suggestions, or improvements, please feel free to open an issue or fork the repository.
