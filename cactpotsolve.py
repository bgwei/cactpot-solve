#The purpose of this tool is to determine the scratchcard line with the highest
#expected payout.
#The default parameters match the Mini Cactpot Scratchcard in Final Fantasy XIV, given an
#input of the four spaces the user has already scratched off.


import statistics
import math
import itertools
import tkinter

#TODO - restructure code with classes?
#TODO - make GUI messages prettier?
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

    master = tkinter.Tk()
    #Create text message displays
    error_message = tkinter.StringVar()
    error_display = tkinter.Label(master, textvariable=error_message)
    error_display.grid(row=rows+2,column=0,columnspan=3)

    payout_message = tkinter.StringVar()
    payout_display = tkinter.Label(master, textvariable=payout_message)
    payout_display.grid(row=rows+3,column=0,rowspan=2,columnspan=2)

    #Create scratchcard grid
    entry_boxes = [create_entry_box(master,box_number) for box_number in range(0,rows*columns)]
    
    for box_number in range(len(entry_boxes)):
        entry_boxes[box_number].grid(row=math.floor(box_number/columns),column=box_number%columns)

    #Create buttons    
    tkinter.Button(master, text="Go!",
                   command=lambda : scratchcard_solve(payout_message,error_message,
                                                      entry_boxes,rows,columns,
                                                      number_to_scratch,payout_dict)
                   ).grid(row=rows+1,column=columns-1)

    tkinter.Button(master, text="Reset",
                   command=lambda : reset(entry_boxes,error_message,payout_message)
                   ).grid(row=rows+1,column=columns-2)

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
def scratchcard_solve(payout_message,error_message,entry_boxes,rows,columns,number_to_scratch,payout_dict):
    
    revealed_values = check_scratchcard(entry_boxes,number_to_scratch)
    
    #If revealed_values returned an error message, print the error and exit scratchcard_solve
    if isinstance(revealed_values,str):
        clear_all(entry_boxes,error_message,payout_message)
        error_message.set(revealed_values)
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
    #Identify the maximum expected value line call correct_boxes to highlight
    #it green; Display expected, min, max payout
    if all_max == max(row_payouts):
        correct_boxes("row",row_payouts.index(max(row_payouts)),
                      rows,columns,entry_boxes,error_message,payout_message)
        payout_message.set("Expected Payout: "+str(max(row_payouts)[0])+
        "\nMinimum Payout: "+str(max(row_payouts)[1])+
        "\nMaximum Payout: "+str(max(row_payouts)[2]))
    elif all_max == max(column_payouts):
        correct_boxes("column",column_payouts.index(max(column_payouts)),
                      rows,columns,entry_boxes,error_message,payout_message)
    elif all_max == max(diagonal_payouts):
        correct_boxes("diagonal",diagonal_payouts.index(max(diagonal_payouts)),
                      rows,columns,entry_boxes,error_message,payout_message)
    #Return the indexes of the numbers in the maximum value lines
    

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

#Given the line type (row, column, diagonal) and the index corresponding
#to the maximum payout calculated for that line type, will highlight the
#of the entry boxes corresponding to that line
def correct_boxes(line_type, payout_index, rows, columns, entry_boxes,error_message,payout_message):
    #Reset box backgrounds to white
    clear_all(entry_boxes,error_message,payout_message)
    #Highlight correct line green
    if line_type == "row":
        for i in range(payout_index*columns,(payout_index+1)*columns):
            entry_boxes[i].config({"background":"#00FF00"})
    elif line_type == "column":
        for i in range(rows):
            entry_boxes[payout_index+i*columns].config({"background":"#00FF00"})
    elif line_type == "diagonal":
        if payout_index == 0:
            for i in range(rows):
                entry_boxes[i*(columns+1)].config({"background":"#00FF00"})
        elif payout_index == 1:
            for i in range(rows):
                entry_boxes[(i+1)*(columns-1)].config({"background":"#00FF00"})

#Resets to initial state
def reset(entry_boxes,error_message,payout_message):
    clear_all(entry_boxes,error_message,payout_message)
    #Deletes text in all entry boxes
    for box in entry_boxes:
        box.delete(0,"end")

#Clears all messages and entry box colors
def clear_all(entry_boxes,error_message,payout_message):
    #Make entry box backgrounds white again
    for box in entry_boxes:
        box.config({"background":"#FFFFFF"})
    #Reset messages    
    error_message.set('')
    payout_message.set('')
    

initialize(3,3,4,{6:10000,7:36,8:720,9:360,10:80,11:252,12:108,13:72,
                 14:54,15:180,16:72,17:180,18:119,19:36,20:306,21:1080,
                 22:144,23:1800,24:3600})

