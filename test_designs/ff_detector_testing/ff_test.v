module ff_test(

    input clk,
    input rst,
    input d,

    output reg q1,
    output reg q2,
    output reg q3

);

always @(posedge clk or negedge rst)
begin

    if(!rst)
    begin

        q1 <= 0;
        q2 <= 0;
        q3 <= 0;

    end

    else
    begin

        q1 <= d;
        q2 <= q1;
        q3 <= q2;

    end

end

endmodule