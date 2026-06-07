module dft_ready_design(
    input clk,
    input rst,
    input scan_en,
    input scan_in,
    output scan_out
);

reg q1;
reg q2;

always @(posedge clk)
begin
    if(rst)
    begin
        q1 <= 0;
        q2 <= 0;
    end
    else
    begin
        q1 <= scan_en ? scan_in : q1;
        q2 <= scan_en ? q1 : q2;
    end
end

assign scan_out = q2;

endmodule