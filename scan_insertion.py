from ff_detector import detect_flip_flops
from scan_chain import create_scan_chain


def generate_scan_insertion_report(filename):

    ff_data = detect_flip_flops(filename)

    flip_flops = ff_data["flip_flops"]

    clocks = ff_data["clocks"]

    resets = ff_data["resets"]

    scan_chain = create_scan_chain(
        flip_flops
    )

    scan_signals = [
        "scan_in",
        "scan_out",
        "scan_en"
    ]

    conversion_plan = []

    for i, ff in enumerate(flip_flops):

        entry = {

            "register": ff,

            "scan_input":
            (
                "scan_in"
                if i == 0
                else flip_flops[i - 1]
            ),

            "scan_output":
            (
                "scan_out"
                if i == len(flip_flops) - 1
                else flip_flops[i + 1]
            ),

            "requires_scan_mux": True
        }

        conversion_plan.append(
            entry
        )

    report = {

        "design_file":
            filename,

        "total_flip_flops":
            len(flip_flops),

        "flip_flops":
            flip_flops,

        "clocks":
            clocks,

        "resets":
            resets,

        "scan_coverage":
             100,

        "scan_signals":
            scan_signals,

        "scan_chain":
            scan_chain,

        "scan_chain_length":
            len(flip_flops),

        "conversion_plan":
            conversion_plan

    }

    return report


def print_scan_insertion_report(report):

    print("\n====================================")
    print("SCAN INSERTION REPORT")
    print("====================================")

    print("\nDesign:")
    print(report["design_file"])

    print("\nTotal Flip-Flops:")
    print(report["total_flip_flops"])

    print("\nClocks:")

    for clk in report["clocks"]:
        print(clk)

    print("\nResets:")

    for rst in report["resets"]:
        print(rst)

    print("\nRequired Scan Signals:")

    for signal in report["scan_signals"]:
        print(signal)

    print("\nScan Chain:")

    for src, dst in report["scan_chain"]:
        print(f"{src} -> {dst}")

    print("\nScan Chain Length:")
    print(report["scan_chain_length"])

    print("\nDFT Conversion Plan:")

    for item in report["conversion_plan"]:

        print("\nRegister:",
              item["register"])

        print("Scan Input:",
              item["scan_input"])

        print("Scan Output:",
              item["scan_output"])

        print("Insert Scan Mux:",
              item["requires_scan_mux"])


if __name__ == "__main__":

    report = generate_scan_insertion_report(
        "test_designs/ff_detector_testing/sv_ff_test.sv"
    )

    print_scan_insertion_report(
        report
    )