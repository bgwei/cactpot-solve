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

LIST OF POSSIBLE TO-DO ITEMS FOR THE FUTURE:
-Restructure code with a class structure. It would probably be a lot nicer to have
a bunch of getters and setters instead of having to toss a ton of arguments into each function
-Make GUI prettier
-Add a custom number_pool parameter to allow for scratchcard games whose numbers
include more numbers than just 1-9. Also add an error check to make sure the number_pool is
appropriately large to accommodate all the spaces in the scratchcard grid.
-Add numbers_repeat boolean parameter to initialize() to allow for scratchcards in which the
same number can occur more than once. This would mean changing scratchcard_solve() so that
revealed numbers are not removed from number_pool. Check_scratchcard() would also need to be
modified to not throw an error when there are duplicates while numbers_repeat = true.
- Make an error to catch if a line sum is not in payout_dict
- Add functionality to make sure diagonal lines don't apply if rows != columns, or modify it to
include all possible diagonals. 
- Modify code to account for multiple lines of equal value
