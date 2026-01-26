import numpy as np
import pandas as pd
import time                    #Required library to calculate Computational Time

start_time = time.time()                 #Keeps the start time

np.random.seed(40)

dataset = pd.read_csv('dataset.csv')     #Imports the csv file containing the data

sites=np.array(dataset)

def calculate_distance(sites , solution):
    solution_for_distance_calculation = np.append(solution, [solution[0]], axis=0) #Appends the site index at the beginning of the solution array to the end of the array
    distance = 0
    next_city_index_founder=0 
    
    for i in solution_for_distance_calculation: #i will hold first site indexes
        next_city_index_founder += 1
        if next_city_index_founder < len(solution_for_distance_calculation):
            next_city_index=solution_for_distance_calculation[next_city_index_founder] #Find the second site indexes here
            distance += np.sqrt(((sites[next_city_index,0]-sites[i,0])**2)+((sites[next_city_index,1]-sites[i,1])**2)) #First site and second site indexes are used when calculating euclidean distance
            
    return distance        

def generate_solution(current_solution): #A new solution will be created by swapping two random sites in the current solution
    idx1 , idx2 = np.random.choice(len(current_solution),2)
    current_solution_copy = current_solution.copy()
    current_solution_copy[idx2], current_solution_copy[idx1] = current_solution_copy[idx1], current_solution_copy[idx2]  
    return current_solution_copy



def main(dataset, T, cooling_rate, T_lower_bound, tolerance):
    
    current_solution = np.random.permutation(range(len(dataset))) #A random initial solution is created using site indexes
    h=0 #Keeps the number of iterations
    
    while T>T_lower_bound: #We want the algorithm to run when the temperature is greater than T_lower_bound
        h+=1
        while True: #Local search will be done here; different solutions will be tried for the "same" temperature value, until new solutions give very close values ​​to the current solution (that is, until the difference in costs between the new potential solution and the current solution is less than the tolerance)
            potential_solution = generate_solution(current_solution) #The potential solution is created using the generate_solution function
            potential_distance = calculate_distance(sites , potential_solution) #The cost of the potential solution is calculated with the calculate_distance function
            current_distance = calculate_distance(sites , current_solution) #The cost of the current solution is calculated with the calculate_distance function
            
        
            if potential_distance < current_distance: #If the potential solution is better, the potential solution is accepted
                current_solution = potential_solution
                
        
            elif np.random.random() < np.exp(-(potential_distance - current_distance)/T): #Potential solution has a chance to be accepted based on a probability even if it is worse
                current_solution = potential_solution
                
            
            if np.abs(potential_distance-current_distance) < tolerance: #Local search will run until a potential solution gives a cost value very close to the current solution
                break
            
            
        T = T*cooling_rate #The temperature is updated depending on the cooling rate
        
        print("------------------------------")
        print("Current solution: ")
        print(np.append(current_solution, [current_solution[0]], axis=0))
        print("Current distance: ")
        print(current_distance)
    
    print("--------RESULTS---------")
    print("Best tour founded for salesman: ", np.append(current_solution, [current_solution[0]], axis=0))
    print("Distance of tour founded: ", current_distance)
    print("Iterations: ",h )
    comp_time = time.time() - start_time     #Keeps the difference between the end time and the start time
    print(f"-> Computational Time: {comp_time} seconds")     #Prints Computational Time
    
main(dataset,100,0.999, 0.01, 1)   #(Dataset including site coordinates, Starting temperature, Cooling rate, Lower bound of temperature, Tolerance of local search)