---
marp: true
theme: default
paginate: true
title: Systematic Diagnosis of Noise in Superconducting Qubits
author: Your Name
style: |
  section {
    font-size: 2em;
  }
---

# Systematic Diagnosis of Noise in SC Qubits

**Focus:** Prioritized noise categories & diagnostic methodologies  
*(Single- and Two-Qubit Systems)*

---

# Noise Categories & Prioritization

1. **SPAM Errors**  
   - State prep & readout errors  
2. **Intrinsic Decoherence**  
   - T₁ (energy relaxation)  
   - T₂ (dephasing via 1/f, etc.)
3. **Control & Gate Errors**  
   - Pulse calibration imperfections (single- and two-qubit)  
4. **Leakage Errors**  
   - Transitions out of the computational subspace  
5. **Crosstalk & Correlated Noise**  
   - Inter-qubit interference & common-mode noise

---

# SPAM Errors (Highest Priority)

- **Objective:** Ensure accurate initialization & measurement.
- **Diagnosis:**
  - Build confusion matrices from repeated |0⟩/|1⟩ preparations.
  - Use active reset / heralding techniques.
- **Key Methods:**  
  - Fast, non-destructive readout  
  - Measurement-based reset

*References: Krantz et al. (2019); Ristè et al. (2012)*

---

# Intrinsic Decoherence

### T₁ and T₂ Measurements

- **T₁ (Relaxation):**  
  - Inversion Recovery experiments.
- **T₂ (Dephasing):**  
  - Ramsey & Echo sequences.

### Noise Spectroscopy

- **Technique:**  
  - Use CPMG / decoupling sequences to extract noise PSD.

*References: Krantz et al. (2019); Müller et al. (2019)*

---

# Control & Gate Errors

### Single-Qubit Gates

- **Diagnostics:**
  - Rabi, Ramsey experiments for pulse calibration.
  - DRAG pulse shaping to cancel leakage & AC Stark shifts.
- **Benchmarking:**
  - Randomized Benchmarking (RB) / Gate Set Tomography (GST).

### Two-Qubit Gates

- **Spectroscopy:**
  - Chevron plots to extract coupling strengths.
- **Diagnostics & Benchmarking:**  
  - Interleaved RB, GST, conditional readout analysis.

*References: Motzoi et al. (2009); Rol et al. (2019); Poletto et al. (2012)*

---

# Leakage Errors

- **Issue:**  
  - Undesired excitations to $|2\rangle$ or higher.
- **Diagnosis:**
  - Modified readout to distinguish $|2\rangle$.
  - Leakage randomized benchmarking.
- **Mitigation:**  
  - Pulse shaping (DRAG, adiabatic pulses).  
  - Optional active reset of leaked states.

*References: Chen et al. (2016); Motzoi et al. (2009)*

---

# Crosstalk & Correlated Noise

- **Key Sources:**  
  - Control line interference, residual ZZ coupling.  
  - Global environmental events (e.g., cosmic rays).
- **Diagnosis:**  
  - Measure crosstalk matrix (single-qubit pulses vs. neighbors).  
  - Simultaneous RB & GST on multi-qubit systems.  
  - Cross-correlation analysis over time.
- **Mitigation:**  
  - Active compensation via pre-distortion.  
  - Architectural isolation & tailored decoupling (e.g., CA-DD).

*References: Suppressing Correlated Noise via Context-Aware Dynamical Decoupling (2024); Two-Qubit Spectroscopy (2019)*

---

# Prioritized Workflow Summary

1. **SPAM Calibration:**  
   - Build confusion matrices; implement active reset.
2. **Intrinsic Decoherence:**  
   - Measure T₁ and T₂; perform noise spectroscopy.
3. **Gate Error Diagnostics:**  
   - Calibrate pulses (Rabi, Ramsey, DRAG); benchmark via RB/GST.
4. **Leakage Detection:**  
   - Use modified readout/tomography; optimize pulse shaping.
5. **Crosstalk Analysis:**  
   - Characterize with simultaneous RB & cross-correlation studies.

*Goal:* Confirm the basic noise budget before further compensation.

---

# Conclusion

- Prioritize SPAM & intrinsic decoherence measurements to establish a baseline.
- Use a combination of spectroscopic, benchmarking, and tomography techniques to diagnose control errors and leakage.
- Characterize crosstalk using simultaneous multi-qubit measurements.
- Iteratively apply context-aware mitigation (CA-DD/CA-EC) based on these diagnostics.

---

# References

1. Krantz, P. et al. (2019). *A Quantum Engineer’s Guide to Superconducting Qubits*. DOI: [10.1063/1.5091792](https://doi.org/10.1063/1.5091792)
2. Motzoi, F. et al. (2009). *Simple Pulses for Elimination of Leakage in Weakly Nonlinear Qubits*. [10.1103/PhysRevLett.103.110501](https://doi.org/10.1103/PhysRevLett.103.110501)
3. Rol, M. et al. (2019). [10.1038/s41534-019-0132-2](https://doi.org/10.1038/s41534-019-0132-2)
4. Poletto, S. et al. (2012). [10.1103/PhysRevLett.109.240505](https://doi.org/10.1103/PhysRevLett.109.240505)
5. Chen, Z. et al. (2016). [10.1103/PhysRevLett.116.020501](https://doi.org/10.1103/PhysRevLett.116.020501)
6. Suppressing Correlated Noise via Context-Aware Dynamical Decoupling, (2024). [arXiv:2403.06852](https://arxiv.org/abs/2403.06852)
7. Two-Qubit Spectroscopy of Spatiotemporally Correlated Quantum Noise, (2019). [arXiv:1912.04982](https://arxiv.org/abs/1912.04982)