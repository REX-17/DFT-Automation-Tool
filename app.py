import streamlit as st
import tempfile
import os

from parser import parse_file

from ff_detector import (
    detect_flip_flops
)

from ai_analysis import (
    generate_ai_analysis
)

from scan_chain import (
    create_scan_chain
)

from scan_insertion import (
    generate_scan_insertion_report
)

from atpg import (
    generate_atpg_report
)
# ------------------------------------------------
# PAGE CONFIG
# ------------------------------------------------

st.set_page_config(

    page_title=
    "DFT Automation Tool",

    layout="wide"

)

st.markdown(
    """
    <style>

    div[data-baseweb="select"] {
        min-height: 68px;
    }

    div[data-baseweb="select"] > div {
        min-height: 68px;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# ------------------------------------------------
# HEADER
# ------------------------------------------------

st.title(
    "DFT Automation Tool"
)

with st.expander(
    "How To Use"
):

    st.write(
        """
        1. Upload RTL, SystemVerilog, VHDL or Netlist files.

        2. Select one or more designs.

        3. Click Analyze Design.

        4. Review DFT metrics.

        5. Review ATPG results.

        6. Check AI recommendations.

        7. Download reports.
        """
    )

# ------------------------------------------------
# UPLOAD SECTION
# ------------------------------------------------

st.subheader(
    "Upload RTL / Netlist"
)

c1, c2 = st.columns([3, 2])

with c1:

    uploaded_files = st.file_uploader(

        "Choose Verilog, SystemVerilog or VHDL Files",

        type=[
            "v",
            "sv",
            "vhd",
            "vhdl"
        ],

        accept_multiple_files=True

    )

with c2:

  sample_design = st.selectbox(
    "Try Sample Test Files",
    [
        "None",

        "D Flip-Flop Register",
        "4-bit Counter",
        "UART Transmitter",
        "Traffic Light FSM",
        "DFT-Ready Design",

        
    ]
)
  
  sample_file_map = {
    "D Flip-Flop Register": "demos/dff_register.v",
    "4-bit Counter": "demos/counter_4bit.v",
    "UART Transmitter": "demos/uart_tx.v",
    "Traffic Light FSM": "demos/traffic_fsm.sv",
    "DFT-Ready Design": "demos/dft_ready_design.v",

    
}

# ----------------------------------------
# BUILD DESIGN LIST
# ----------------------------------------

all_designs = []

if uploaded_files:

    all_designs.extend(
        uploaded_files
    )

if sample_design != "None":
    all_designs.append(
        sample_file_map[sample_design]
    )

# ----------------------------------------
# DISPLAY DESIGNS
# ----------------------------------------

with st.expander(

    "Uploaded Designs",

    expanded=True

):

    if len(all_designs) == 0:

        st.info(
            "No designs selected yet."
        )

    else:

        for design in all_designs:

            if hasattr(
                design,
                "name"
            ):

                st.write(
                    f"📄 {design.name}"
                )

            else:

                st.write(
                    f"📄 {design}"
                )

# ----------------------------------------
# SELECTION SECTION
# ----------------------------------------

selected_files = []

if len(all_designs) > 1:

    st.subheader(
        "Select Designs to Analyze"
    )

    for design in all_designs:

        design_name = (

            design.name

            if hasattr(
                design,
                "name"
            )

            else design

        )

        if st.checkbox(

            design_name,

            key=f"select_{design_name}"

        ):

            selected_files.append(
                design
            )

elif len(all_designs) == 1:

    selected_files = all_designs

if selected_files:

    st.success(

        f"{len(selected_files)} design(s) selected"

    )

analyze = st.button(

    "Analyze Selected Designs"

)

# ------------------------------------------------
# MAIN ANALYSIS
# ------------------------------------------------

if selected_files and analyze:

    for selected_file in selected_files:

        # ----------------------------------------
        # SAMPLE TEST FILE
        # ----------------------------------------

        if isinstance(
            selected_file,
            str
        ):

            temp_path = os.path.join(

                "test_designs",

                selected_file

            )

            design_name = selected_file

        # ----------------------------------------
        # UPLOADED FILE
        # ----------------------------------------

        else:

            suffix = os.path.splitext(

                selected_file.name

            )[1]

            with tempfile.NamedTemporaryFile(

                delete=False,

                suffix=suffix

            ) as tmp_file:

                tmp_file.write(

                    selected_file.getbuffer()

                )

                temp_path = tmp_file.name

            design_name = selected_file.name

        # ----------------------------------------
        # RUN ANALYSIS
        # ----------------------------------------

        parser_data = parse_file(
            temp_path
        )

        ff_data = detect_flip_flops(
            temp_path
        )

        scan_chain = create_scan_chain(

            ff_data[
                "flip_flops"
            ]

        )

        scan_report = (

            generate_scan_insertion_report(
                temp_path
            )

        )

        atpg_report = (

            generate_atpg_report(
                temp_path
            )

        )

        ai_report = (

            generate_ai_analysis(
                temp_path
            )

        )

        # ----------------------------------------
        # HEADER
        # ----------------------------------------

        st.markdown("---")

        st.success(

            f"Selected Design: {design_name}"

        )

        # ----------------------------------------
        # DASHBOARD METRICS
        # ----------------------------------------

        c1, c2, c3, c4, c5, c6 = st.columns(6)

        with c1:

            st.metric(

                "Flip-Flops",

                ff_data[
                    "total_flip_flops"
                ]

            )

        with c2:

            st.metric(

                "Clock Domains",

                len(

                    ff_data[
                        "clocks"
                    ]

                )

            )

        with c3:

            st.metric(

                "Reset Domains",

                len(

                    ff_data[
                        "resets"
                    ]

                )

            )

        with c4:

            st.metric(

                "Scan Length",

                scan_report[
                    "scan_chain_length"
                ]

            )

        with c5:

            st.metric(

                "Fault Coverage",

                atpg_report[
                    "estimated_fault_coverage"
                ]

            )

        with c6:

            st.metric(

                "DFT Readiness",

                atpg_report[
                    "dft_readiness"
                ]

            )

        st.markdown("---")

                # ----------------------------------------
        # TABS
        # ----------------------------------------

        tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(
            [
                "Parser",
                "FF Analysis",
                "Scan Chain",
                "Scan Insertion",
                "ATPG",
                "AI Analysis"
            ]
        )

        # ----------------------------------------
        # PARSER TAB
        # ----------------------------------------

        with tab1:

            st.subheader(
                "Parser Results"
            )

            for key, value in parser_data.items():

                st.write(
                    f"**{key}**",
                    value
                )

        # ----------------------------------------
        # FF ANALYSIS TAB
        # ----------------------------------------

        with tab2:

            st.subheader(
                "Flip-Flop Analysis"
            )

            st.metric(
                "Total Flip-Flops",
                ff_data["total_flip_flops"]
            )

            st.write("Detected Flip-Flops")

            st.write(
                ff_data["flip_flops"]
            )

            st.write("Clock Signals")

            st.write(
                ff_data["clocks"]
            )

            st.write("Reset Signals")

            st.write(
                ff_data["resets"]
            )

            if ff_data["total_flip_flops"] == 0:

                st.warning(
                    "No sequential elements detected."
                )

            else:

                st.success(
                    f"{ff_data['total_flip_flops']} flip-flops detected."
                )

        # ----------------------------------------
        # SCAN CHAIN TAB
        # ----------------------------------------

        with tab3:

            st.subheader(
                "Generated Scan Chain"
            )

            if len(scan_chain) == 0:

                st.warning(
                    "No scan chain generated."
                )

            else:

                for src, dst in scan_chain:

                    st.write(
                        f"{src} → {dst}"
                    )

                st.success(
                    f"Total Connections: {len(scan_chain)}"
                )

        # ----------------------------------------
        # SCAN INSERTION TAB
        # ----------------------------------------

        with tab4:

            st.subheader(
                "Scan Insertion Report"
            )

            c1, c2, c3 = st.columns(3)

            with c1:

                st.metric(
                    "Scan Chain Length",
                    scan_report["scan_chain_length"]
                )

            with c2:

                st.metric(
                    "Total Flip-Flops",
                    scan_report["total_flip_flops"]
                )

            with c3:

                st.metric(
                    "Scan Signals",
                    len(scan_report["scan_signals"])
                )

            st.subheader(
                "DFT Signals"
            )

            st.write("Scan Signals")

            st.code(
                ", ".join(
                    scan_report["scan_signals"]
                )
            )

            st.write("Clock Signals")

            st.code(
                ", ".join(
                    scan_report["clocks"]
                )
            )

            st.write("Reset Signals")

            st.code(
                ", ".join(
                    scan_report["resets"]
                )
            )

            st.subheader(
                "Scan Chain Connectivity"
            )

            for src, dst in scan_report["scan_chain"]:

                st.write(
                    f"{src} ➜ {dst}"
                )

            st.subheader(
                "Scan Conversion Plan"
            )

            for item in scan_report["conversion_plan"]:

                with st.expander(
                    f"Register : {item['register']}"
                ):

                    st.write(
                        f"Scan Input : {item['scan_input']}"
                    )

                    st.write(
                        f"Scan Output : {item['scan_output']}"
                    )

                    st.write(
                        f"Requires Scan MUX : {item['requires_scan_mux']}"
                    )

        # ----------------------------------------
        # ATPG TAB
        # ----------------------------------------

        with tab5:

            st.subheader(
                "ATPG Report"
            )

            m1, m2, m3 = st.columns(3)

            with m1:

                st.metric(
                    "Scan Coverage (%)",
                    atpg_report["scan_coverage"]
                )

            with m2:

                st.metric(
                    "Fault Coverage (%)",
                    atpg_report["estimated_fault_coverage"]
                )

            with m3:

                st.metric(
                    "DFT Readiness",
                    atpg_report["dft_readiness"]
                )

        # ----------------------------------------
        # AI ANALYSIS TAB
        # ----------------------------------------

        with tab6:

            st.subheader(
                "AI Design Review"
            )

            c1, c2 = st.columns(2)

            with c1:

                st.metric(
                    "DFT Status",
                    ai_report["status"]
                )

            with c2:

                st.metric(
                    "Score",
                    ai_report["score"]
                )

            st.subheader(
                "Observations"
            )

            for item in ai_report["observations"]:

                st.info(item)

            st.subheader(
                "Recommendations"
            )

            for item in ai_report["recommendations"]:

                st.success(item)

            report_text = f"""
Design:
{design_name}

Flip-Flops:
{ff_data['total_flip_flops']}

Scan Coverage:
{atpg_report['scan_coverage']}

Fault Coverage:
{atpg_report['estimated_fault_coverage']}

DFT Readiness:
{atpg_report['dft_readiness']}

DFT Status:
{ai_report['status']}
"""

            st.download_button(
                label="Download TXT Report",
                data=report_text,
                file_name=f"{design_name}_report.txt",
                mime="text/plain"
            )
























       