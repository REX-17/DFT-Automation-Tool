library IEEE;
use IEEE.STD_LOGIC_1164.ALL;

entity counter is
    Port (
        clk : in STD_LOGIC;
        rst : in STD_LOGIC;
        q   : out STD_LOGIC
    );
end counter;

architecture Behavioral of counter is

signal temp : STD_LOGIC;

begin

process(clk)

begin

    if rising_edge(clk) then

        temp <= not temp;

    end if;

end process;

q <= temp;

end Behavioral;