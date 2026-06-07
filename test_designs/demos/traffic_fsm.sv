module traffic_fsm(
    input logic clk,
    input logic rst,
    output logic [1:0] light
);

typedef enum logic [1:0]
{
    RED,
    GREEN,
    YELLOW
} state_t;

state_t state;

always_ff @(posedge clk or posedge rst)
begin
    if(rst)
        state <= RED;
    else
        case(state)
            RED: state <= GREEN;
            GREEN: state <= YELLOW;
            YELLOW: state <= RED;
        endcase
end

assign light = state;

endmodule