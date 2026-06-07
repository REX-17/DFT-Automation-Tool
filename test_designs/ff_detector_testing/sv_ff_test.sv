module sv_ff_test(

    input logic clk,
    input logic rst,

    input logic d1,
    input logic d2,

    output logic q1,
    output logic q2

);

always_ff @(posedge clk or negedge rst)
begin

    if(!rst)
    begin

        q1 <= 0;
        q2 <= 0;

    end

    else
    begin

        q1 <= d1;
        q2 <= d2;

    end

end

endmodule