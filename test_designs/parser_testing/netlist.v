module netlist(
    input clk,
    input d,
    output q
);

DFFRX1 U1(
    .D(d),
    .CK(clk),
    .Q(q)
);

endmodule