module multi_clock(

    input clk1,
    input clk2,

    input d1,
    input d2,

    output reg q1,
    output reg q2

);

always @(posedge clk1)
begin
    q1 <= d1;
end

always @(posedge clk2)
begin
    q2 <= d2;
end

endmodule