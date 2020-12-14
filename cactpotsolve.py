#The purpose of this tool is to determine the scratchcard line with the highest
#expected payout.
#The default parameters match the Mini Cactpot Scratchcard in Final Fantasy XIV, given an
#input of the four spaces the user has already scratched off.


import statistics
import math
import itertools
import tkinter

#TODO - visually show which line choice is best
#TODO - print errors to the GUI
#TODO - add reset button functionality
#TODO - compartmentalize functions more?
#TODO - custom number_pool in initialize() - error if number pool is too small for grid
#TODO - add numbers_repeat boolean to initialize(); would need to change number_pool to not
#       remove items and check_scratchcard() to not check duplicates
#TODO - error to catch if a possibility is not in payout dict given parameters?
#TODO - make sure diag doesn't apply if rows != columns?
#TODO - account for multiple lines of equal value?

#Create table of text input boxes representing scratchcard spaces
##Scratchcard Parameters
##rows = number of rows in scratchcard
##columns = number of columns in scratchcard
##number_to_scratch = number of spaces that can be scratched (revealed) before a line must be chosen
##payout_dict = a dictionary containing the payout for each score
def initialize(rows,columns,number_to_scratch,payout_dict):

    #Create table GUI
    master = tkinter.Tk()
    
    entry_boxes = [create_entry_box(master,box_number) for box_number in range(0,rows*columns)]

    for box_number in range(len(entry_boxes)):
        entry_boxes[box_number].grid(row=math.floor(box_number/columns),column=box_number%columns)
        
    correct_cells = []
    tkinter.Button(master, text="Go!",
                   command=lambda : scratchcard_solve(entry_boxes,rows,columns,
                                                      number_to_scratch,payout_dict)
                   ).grid(row=rows+1,column=columns-1)

    for cell in correct_cells:
        entry_boxes[cell].config({"background":"#00FF00"})
    
    master.mainloop()

#Creates an entry box
def create_entry_box(master,box_number):
    new_entry = tkinter.Entry(master)
    return new_entry

#Checks to make sure the values entered are valid. If they are, returns list of values for further
#processing. Otherwise, returns an error message string. Empty cells are returned as 0 within the list.
def check_scratchcard(entry_boxes,number_to_scratch):
    input_list = []
    scratch_count = 0
    for box in entry_boxes:
        if scratch_count > number_to_scratch:
            return ("Error! You cannot input more than "+str(number_to_scratch)+" scratched numbers!")
        if box.get() == '':
            input_list.append(0)
        elif box.get().isdigit() and 1 <= int(box.get()) <= 9:
            if int(box.get()) in input_list:
                return ("Error! You cannot scratch duplicates of the same number: "+box.get())
            else:
                input_list.append(int(box.get()))
                scratch_count += 1
        else:
            return ("Error! "+box.get()+" is an invalid input! Make sure you entered the correct numbers!")
        
    if scratch_count < number_to_scratch:
        return ("Error! "+str(scratch_count)+" numbers detected! You need all "+str(number_to_scratch)+"!")

    return(input_list)


#Solve scratchcard for optimal line choice based on average expected payout. Takes the input
#from the entry_boxes as an argument.    
def scratchcard_solve(entry_boxes,rows,columns,number_to_scratch,payout_dict):
    
    revealed_values = check_scratchcard(entry_boxes,number_to_scratch)
    
    #If revealed_values returned an error message, print the error and exit scratchcard_solve
    if isinstance(revealed_values,str):
        print(revealed_values)
        return
    #Figure out which numbers are still unscratched by removing ones already revealed
    number_pool = list(range(1,10))
    for num in revealed_values:
        if num in number_pool:
            number_pool.remove(num)
    #Split scratchcard into lines
    row_split = row_splitter(revealed_values,columns,rows)
    column_split = column_splitter(revealed_values,columns,rows)
    diagonal_split = diagonal_splitter(revealed_values,columns,rows)
    #Calculate payouts for those lines
    row_payouts = calc_line_payouts(row_split,number_pool,payout_dict)
    column_payouts = calc_line_payouts(column_split,number_pool,payout_dict)
    diagonal_payouts = calc_line_payouts(diagonal_split,number_pool,payout_dict)
    #Find max expected value
    all_max = max([max(row_payouts),max(column_payouts),max(diagonal_payouts)])
    #Identify the maximum expected value line and print it
    if all_max == max(row_payouts):
        print(row_split[row_payouts.index(max(row_payouts))])
##        print("Expected Payout: "+str(max(row_payouts)[0]))
##        print("Minimum Payout: "+str(max(row_payouts)[1]))
##        print("Maximum Payout: "+str(max(row_payouts)[2]))
    elif all_max == max(column_payouts):
        print(column_split[column_payouts.index(max(column_payouts))])
    elif all_max == max(diagonal_payouts):
        print(diagonal_split[diagonal_payouts.index(max(diagonal_payouts))])
    #Return the indexes of the numbers in the maximum value lines
    correct_cells = [1,2,3]
    return correct_cells
    

#Split scratchcard into a list of rows
def row_splitter(revealed_values,columns,rows):
    return [revealed_values[i*columns:(i+1)*columns] for i in range(rows)]

#Split scratchcard into a list of columns
def column_splitter(revealed_values,columns,rows):
    column_list = []
    
    for i in range(columns):
        column = []
        for j in range(rows):
            column.append(revealed_values[i+(j*columns)])
        column_list.append(column)
        
    return column_list

#Creates a list for each of the scratchcard diagonals
def diagonal_splitter(revealed_values,columns,rows):
    diag1 = []
    for i in range(rows):
        diag1.append(revealed_values[(columns+1)*i])
    diag2 = []
    for i in range(rows):
        diag2.append(revealed_values[(columns-1)*(i+1)])
    return [diag1,diag2]
    
#Given a list of lines, will calculate expected payouts for those lines of the scratchcard;
#returns a list whose elements are formatted: [Expected Payout,Minimum Payout,Maximum Payout]
def calc_line_payouts(lines,number_pool,payout_dict):
    line_payouts = []
    for line in lines:
        unrevealed_combinations = list(itertools.combinations(number_pool,line.count(0)))
        payouts = []
        for combination in unrevealed_combinations:
            payouts.append(payout_dict[sum(line)+sum(combination)])
        line_payouts.append(payouts)
    #Convert list of line_payouts into desired output format
    output = []
    for line in line_payouts:
        output.append([statistics.mean(line),min(line),max(line)])
    return output

initialize(3,3,4,{6:10000,7:36,8:720,9:360,10:80,11:252,12:108,13:72,
                 14:54,15:180,16:72,17:180,18:119,19:36,20:306,21:1080,
                 22:144,23:1800,24:3600})

