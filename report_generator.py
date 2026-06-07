from parser import parse_file

from ff_detector import detect_flip_flops

from scan_insertion import (
    generate_scan_insertion_report
)

from atpg import (
    generate_atpg_report
)


def generate_full_report(filename):

    parser_data = parse_file(
        filename
    )

    ff_data = detect_flip_flops(
        filename
    )

    scan_data = (
        generate_scan_insertion_report(
            filename
        )
    )

    atpg_data = generate_atpg_report(
        filename
    )

    report = {

        "filename":
            filename,

        "parser":
            parser_data,

        "ff_detector":
            ff_data,

        "scan":
            scan_data,

        "atpg":
            atpg_data

    }

    return report


def print_full_report(report):

    print("\n================================")
    print("DFT ANALYSIS REPORT")
    print("================================")

    print("\nFile:")
    print(report["filename"])

    print("\nModule:")
    print(
        report["parser"].get(
            "module",
            "Unknown"
        )
    )

    print("\nTotal Flip-Flops:")
    print(
        report["atpg"][
            "total_flip_flops"
        ]
    )

    print("\nScan Chain Length:")
    print(
        report["scan"][
            "scan_chain_length"
        ]
    )

    print("\nScan Coverage (%):")
    print(
        report["atpg"][
            "scan_coverage"
        ]
    )

    print("\nEstimated Fault Coverage (%):")
    print(
        report["atpg"][
            "estimated_fault_coverage"
        ]
    )

    print("\nDFT Readiness Score:")
    print(
        report["atpg"][
            "dft_readiness"
        ]
    )

    print("\nClocks:")

    for clk in report["scan"]["clocks"]:

        print(clk)

    print("\nResets:")

    for rst in report["scan"]["resets"]:

        print(rst)

    print("\nFlip-Flops:")

    for ff in report["scan"]["flip_flops"]:

        print(ff)


if __name__ == "__main__":

    report = generate_full_report(

        "test_designs/ff_detector_testing/flawed_file.v"

    )

    print_full_report(
        report
    )