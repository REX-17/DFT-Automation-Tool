import re


def detect_flip_flops(filename):

    with open(filename, "r") as f:
        code = f.read()

    # Remove comments
    code = re.sub(r'//.*', '', code)
    code = re.sub(r'/\*.*?\*/', '', code, flags=re.DOTALL)

    flip_flops = set()
    clocks = set()
    resets = set()

    # ------------------------------------------------
    # Detect always_ff blocks (SystemVerilog)
    # ------------------------------------------------

    always_ff_blocks = re.finditer(
        r'always_ff\s*@\((.*?)\)(.*?)(?=always_ff|always_comb|endmodule|\Z)',
        code,
        re.DOTALL
    )

    for block in always_ff_blocks:

        sensitivity = block.group(1)
        body = block.group(2)

        edge_signals = re.findall(
            r'(posedge|negedge)\s+(\w+)',
            sensitivity
        )

        if edge_signals:

            # First edge signal is assumed to be clock
            clocks.add(edge_signals[0][1])

            # Remaining edge signals are resets
            for edge_type, signal in edge_signals[1:]:

                resets.add(signal)

        assignments = re.findall(
            r'(\w+)\s*<=',
            body
        )

        flip_flops.update(assignments)

    # ------------------------------------------------
    # Detect Verilog always blocks
    # ------------------------------------------------

    always_blocks = re.finditer(
        r'always\s*@\((.*?)\)(.*?)(?=always|endmodule|\Z)',
        code,
        re.DOTALL
    )

    for block in always_blocks:

        sensitivity = block.group(1)
        body = block.group(2)

        if "posedge" not in sensitivity and "negedge" not in sensitivity:
            continue

        edge_signals = re.findall(
            r'(posedge|negedge)\s+(\w+)',
            sensitivity
        )

        if edge_signals:

            # First edge signal is assumed to be clock
            clocks.add(edge_signals[0][1])

            # Remaining edge signals are resets
            for edge_type, signal in edge_signals[1:]:

                resets.add(signal)

        assignments = re.findall(
            r'(\w+)\s*<=',
            body
        )

        flip_flops.update(assignments)

    return {
        "flip_flops": sorted(list(flip_flops)),
        "total_flip_flops": len(flip_flops),
        "clocks": sorted(list(clocks)),
        "resets": sorted(list(resets))
    }


if __name__ == "__main__":

    result = detect_flip_flops(
        "test_designs/ff_detector_testing/sv_ff_test.sv"
    )

    print("\nDetected Flip-Flops:")
    for ff in result["flip_flops"]:
        print(ff)

    print("\nTotal Flip-Flops:")
    print(result["total_flip_flops"])

    print("\nClocks:")
    for clk in result["clocks"]:
        print(clk)

    print("\nResets:")
    for rst in result["resets"]:
        print(rst)