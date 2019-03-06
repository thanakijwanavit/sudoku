import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime as time
import functions as f


def calculate_and_solve(framework):
	
	### calculate each position array###
	v_poss=f.list_verticle_framework(framework)
	h_poss=f.list_horizontal_framework(framework)
	b_poss=f.list_box_framework(framework)
	framework_with_positional_element = f.generate_positional_array(framework)
	### solve ####
	status,remain_possible=f.solve(framework_with_positional_element,framework,1,v_poss,h_poss,b_poss)
	return [framework,status,remain_possible]

def solve_multiple_times(new_sudoku,times):
	### convert into 3,3,3,3 dimension###
	sudoku=f.create_framework(new_sudoku)
	for i in range(times):
		sudoku,status,remain_possible=calculate_and_solve(sudoku)
		if status == 0 : return {'sudoku':sudoku,"loops":i,"status":status,"remaining":remain_possible}
	return {'sudoku':sudoku,"loops":i,"status":status,"remaining":remain_possible}

## specify variables
difficulty=0.6
times=10

### generate sudoku ####
new_sudoku=f.generate_sudoku(difficulty)
t0=time.now()
#### calculate and solve###
final_sudoku=solve_multiple_times(new_sudoku,times)

print(f"sudoku is {'solved' if final_sudoku['status'] == 0 else 'not solved'} after {final_sudoku['loops']} loops.\n time taken is {(time.now()-t0).total_seconds()*1000} ms \n with {final_sudoku['remaining']} still possible")

#### save to file ####
np.save("solved", final_sudoku['sudoku'])