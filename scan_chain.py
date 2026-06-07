def create_scan_chain(ff_list):

    scan_connections = []

    if len(ff_list) == 0:

        return scan_connections

    scan_connections.append(
        ("Scan_In", ff_list[0])
    )

    for i in range(len(ff_list)-1):

        scan_connections.append(
            (
                ff_list[i],
                ff_list[i+1]
            )
        )

    scan_connections.append(
        (
            ff_list[-1],
            "Scan_Out"
        )
    )

    return scan_connections


def print_scan_chain(scan_connections):

    print("\nScan Chain:\n")

    for src, dst in scan_connections:

        print(f"{src} -> {dst}")

    print(
        f"\nTotal Connections: "
        f"{len(scan_connections)}"
    )


if __name__ == "__main__":

    from ff_detector import detect_flip_flops

    result = detect_flip_flops(

    "test_designs/ff_detector_testing/ff_test.v"
)

    flip_flops = result["flip_flops"]
    scan_chain = create_scan_chain(
        flip_flops
    )

    print_scan_chain(
        scan_chain
    )


