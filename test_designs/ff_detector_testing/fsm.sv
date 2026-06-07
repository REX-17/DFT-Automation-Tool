module fsm(

    input logic clk,
    input logic rst,
    input logic x,

    output logic y

);

typedef enum logic [1:0]
{
    S0,
    S1,
    S2,
    S3
} state_t;

state_t state;
state_t next_state;

always_ff @(posedge clk or negedge rst)
begin

    if(!rst)
        state <= S0;

    else
        state <= next_state;

end

always_comb
begin

    next_state = state;

    case(state)

        S0:
            if(x)
                next_state = S1;

        S1:
            if(x)
                next_state = S2;

        S2:
            if(x)
                next_state = S3;

        S3:
            next_state = S0;

    endcase

end

assign y = (state == S3);

endmodule