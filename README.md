# cactpot-solve
Simulates a grid-based scratchcard game. A limited amount of spaces can be revealed before a line must be chosen.
The "payout" for that line is based on the sum of the numbers in that line. Given inputs for the revealed spaces,
the tool determines which line has the highest expected payout based on the average of all possible payouts for
that line once the rest of the scratchcard is revealed.

The scratchcard can be customized with the following parameters:

rows = number of rows in scratchcard

columns = number of columns in scratchcard

number_to_scratch = number of spaces that can be scratched (revealed) before a line must be chosen

payout_dict = a dictionary containing the payout for each line sum

and highlights which row has the highest expected payout. The minimum and maximum possible payouts
will also be displayed.

The default settings simulate the Mini Cactpot from Final Fantasy XIV.
