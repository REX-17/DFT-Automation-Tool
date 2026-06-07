module and_gate(
    input a,
    input b,
    output y
);

assign y = a & b;

endmodule


module structural(
    input a,
    input b,
    output y
);

and_gate U1(
    .a(a),
    .b(b),
    .y(y)
);

endmodule