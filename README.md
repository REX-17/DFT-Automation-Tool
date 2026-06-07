# DFT Automation Tool

## Overview

DFT Automation Tool is a Python and Streamlit based application developed to automate key Design-for-Testability (DFT) tasks for RTL and netlist designs.

The tool accepts Verilog, SystemVerilog and VHDL designs, performs structural analysis, identifies sequential elements, generates scan-chain information, estimates ATPG metrics, and provides AI-assisted DFT recommendations through an interactive dashboard.

The project was developed to demonstrate practical concepts used in ASIC and VLSI test engineering workflows.



## Features

### RTL and Netlist Parsing

* Supports Verilog (.v)
* Supports SystemVerilog (.sv)
* Supports VHDL (.vhd/.vhdl)
* Extracts design information automatically

### Flip-Flop Detection

* Identifies sequential elements
* Detects clock signals
* Detects reset signals
* Reports flip-flop statistics

### Scan Chain Generation

* Creates scan-chain connectivity
* Calculates scan-chain length
* Generates scan insertion plans

### ATPG Metrics

* Estimates scan coverage
* Estimates fault coverage
* Computes DFT readiness score
* Generates ATPG summary reports

### AI-Assisted Analysis

* Design quality assessment
* DFT readiness evaluation
* Automated recommendations
* Improvement suggestions

### Sample Demonstration Designs

The repository includes multiple sample designs such as:

* D Flip-Flop Register
* 4-bit Counter
* UART Transmitter
* Traffic Light FSM
* DFT-Ready Design



## Project Architecture

Input RTL / Netlist

↓

Parser

↓

Flip-Flop Detection

↓

Scan Chain Generation

↓

Scan Insertion Analysis

↓

ATPG Estimation

↓

AI-Based DFT Review

↓

Report Generation


## Technologies Used

* Python
* Streamlit
* Verilog HDL
* SystemVerilog
* VHDL
* ASIC DFT Concepts
* ATPG Estimation Techniques



## Repository Structure

```text
app.py                  Main Streamlit Application
parser.py               RTL Parser
ff_detector.py          Flip-Flop Detection Engine
scan_chain.py           Scan Chain Generator
scan_insertion.py       Scan Insertion Analysis
atpg.py                 ATPG Metric Generation
ai_analysis.py          AI-Assisted Design Review
test_designs/           Sample RTL Designs
```

## How to Run

Clone the repository:

```bash
git clone <repository-link>
cd DFT_Automation_Tool
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Launch the application:

```bash
streamlit run app.py
```



## Example Outputs

* Parser Reports
* Flip-Flop Analysis Reports
* Scan Chain Connectivity
* Scan Insertion Plans
* ATPG Metrics
* AI-Based Recommendations
* Downloadable Text Reports



## Applications

* VLSI Design Verification
* Design-for-Testability Education
* ASIC Test Flow Demonstration
* FPGA and RTL Analysis
* Academic Projects and Research

