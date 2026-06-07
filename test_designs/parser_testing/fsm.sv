module fsm(

    input logic clk,
    input logic rst,
    input logic x,

    output logic y

);

typedef enum logic [1:0] {

    S0,
    S1,
    S2,
    S3

} state_t;

state_t state;

always_ff @(posedge clk)
begin

    state <= S1;

end

always_comb
begin

    y = (state == S3);

end

endmodule