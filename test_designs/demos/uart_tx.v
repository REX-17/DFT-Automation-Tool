module uart_tx(
    input clk,
    input rst,
    input start,
    output reg tx
);

reg [3:0] state;

always @(posedge clk)
begin
    if(rst)
        state <= 0;
    else if(start)
        state <= state + 1;
end

endmodule