from parser import parse_file
from ff_detector import detect_flip_flops
from scan_insertion import generate_scan_insertion_report
from atpg import generate_atpg_report


def generate_ai_analysis(filename):

    parser_data = parse_file(filename)

    ff_data = detect_flip_flops(filename)

    scan_data = generate_scan_insertion_report(
        filename
    )

    atpg_data = generate_atpg_report(
        filename
    )

    observations = []
    recommendations = []

    score = 100

    # analysis code starts here

    # ------------------------------------
    # Flip-Flop Analysis
    # ------------------------------------

    ff_count = ff_data["total_flip_flops"]

    observations.append(
        f"{ff_count} flip-flops detected"
    )

    if ff_count == 0:

        recommendations.append(
            "Add sequential elements if scan-based testing is required."
        )

        recommendations.append(
            "Pure combinational logic may reduce ATPG effectiveness in larger designs."
        )

        score -= 40

    # ------------------------------------
    # Reset Analysis
    # ------------------------------------

    resets = ff_data["resets"]

    if len(resets) == 0:

        observations.append(
            "No reset signal detected"
        )

        recommendations.append(
            "Add a synchronous or asynchronous reset signal to ensure deterministic startup behavior."
        )

        recommendations.append(
            "Initialize all state-holding registers through reset logic."
        )

        score -= 10

    else:

        observations.append(
            "Reset signal detected"
        )

    # ------------------------------------
    # Clock Analysis
    # ------------------------------------

    clocks = ff_data["clocks"]

    observations.append(
        f"{len(clocks)} clock domain(s)"
    )

    if len(clocks) > 1:

        recommendations.append(
            "Separate scan chains should be considered for each clock domain."
        )

        recommendations.append(
            "Perform clock-domain-crossing (CDC) verification before scan insertion."
        )

        score -= 10

    # ------------------------------------
    # Scan Coverage Analysis
    # ------------------------------------

    coverage = atpg_data["scan_coverage"]

    observations.append(
        f"Scan coverage = {coverage}%"
    )

    if coverage < 100:

        recommendations.append(
            "Include uncovered flip-flops in the scan chain to improve controllability and observability."
        )

        recommendations.append(
            "Review scan stitching and scan chain connectivity."
        )

        score -= 15

    else:

        observations.append(
            "All detected flip-flops are included in the scan chain."
        )

    # ------------------------------------
    # Fault Coverage Analysis
    # ------------------------------------

    fault_cov = atpg_data[
        "estimated_fault_coverage"
    ]

    observations.append(
        f"Estimated fault coverage = {fault_cov}%"
    )

    if fault_cov < 90:

        recommendations.append(
            "Increase scan accessibility to improve ATPG effectiveness."
        )

        recommendations.append(
            "Consider adding observation or control points in difficult-to-test logic."
        )

        score -= 15

    elif fault_cov < 98:

        recommendations.append(
            "Fault coverage is acceptable but may be improved through additional test points."
        )

    # ------------------------------------
    # Positive Design Feedback
    # ------------------------------------

    if (
        len(resets) > 0
        and len(clocks) == 1
        and coverage == 100
        and fault_cov >= 95
    ):

        recommendations.append(
            "Design appears DFT-ready and suitable for scan-based ATPG."
        )

    # ------------------------------------
    # Final Rating
    # ------------------------------------

    if score >= 90:

        status = "EXCELLENT"

    elif score >= 75:

        status = "GOOD"

    elif score >= 60:

        status = "FAIR"

    else:

        status = "POOR"

    return {

        "status": status,

        "score": score,

        "observations": observations,

        "recommendations": recommendations

    }

def print_ai_analysis(report):

    print("\n========== AI ANALYSIS ==========")

    print("\nDFT Status:")
    print(report["status"])

    print("\nScore:")
    print(report["score"])

    print("\nObservations:")

    for item in report["observations"]:

        print("-", item)

    print("\nRecommendations:")

    for item in report["recommendations"]:

        print("-", item)


if __name__ == "__main__":

    report = generate_ai_analysis(

        "test_designs/ff_detector_testing/flawed_file.v"

    )

    print_ai_analysis(
        report
    )