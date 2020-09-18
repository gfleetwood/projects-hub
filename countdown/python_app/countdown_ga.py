import numpy as np
import random

def setup():
	target = np.random.randint(100, 999)
	num_big_nums = np.random.randint(1, 4)
	nums = list(np.random.choice(range(10, 100), size = num_big_nums, replace = False)) + \
	list(np.random.choice(range(1, 10), size = 6-num_big_nums, replace = False))
	ops = ['+', '-', '/', '*']
	return target, nums, ops

def create_individual(nums, ops):
    pop_member = [1 for i in range(11)]
    pop_member[::2] = [str(num) for num in np.random.choice(nums, size = 6, replace = False)]
    pop_member[1::2] = [random.sample(ops, 1)[0] for i in range(5)]
    return pop_member

def create_population(nums, ops, size = 10):
    return [create_individual(nums, ops) for i in range(size)]

def result(individual):
    return eval(''.join([str(i) for i in individual]))

def fitness_individual(individual, target):
    target_produced = result(individual)
    digits = [int(i) for i in individual if i.isdigit()]
    
    #A decimal or negative number gets a fitness score of 10**6 
    if (np.abs(target_produced - int(target_produced)) > 0) or (target_produced) < 0:
        return 10**6  
    #So does an individual with repeated digits
    elif len(set(digits)) < len(digits):
        return 10**6            
    else:
        return np.abs(int(target_produced) - target)  
    
def fitness_population(pop, target):
    return np.mean([fitness_individual(ind, target) for ind in pop])

def evolution(pop, nums, ops, target, retain = 0.5, random_select = 0.05, mutate = 0.01):
    grades = [(fitness_individual(ind, target), ind) for ind in pop]
    grades = [x[1] for x in sorted(grades, reverse = False, key = lambda x: x[0])]
    parents = grades[:int(len(grades)*retain)]
    best_individual = grades[0]
    
    for ind in grades[int(len(grades)*retain):]:
        if random_select > random.random():
            parents.append(ind)
            
    for individual in parents:
        if mutate > random.random():
            pos_to_mutate = np.random.randint(0, 11)
            if pos_to_mutate%2==1:
                individual[pos_to_mutate] = random.sample(ops, 1)[0]

    parents_length = len(parents)
    desired_length = len(pop) - parents_length
    children = []
    while len(children) < desired_length:
        male, female = np.random.choice(range(parents_length), size = 2, replace = False)
        parent_1 = parents[male]
        parent_2 = parents[female]
        child = parent_1[:6] + parent_2[6:]
        children.append(child)
    parents.extend(children)
    return parents, (best_individual, result(best_individual))

def run_count_down(nums, ops, target, times = 5):
    pop = create_population(nums, ops)
    fitness_history = [fitness_population(pop, target)]
    for i in range(times):
        pop, best_individual = evolution(pop, nums, ops, target)
        fitness_history.append(fitness_population(pop, target))
    return fitness_history, best_individual

if __name__ == "__main__":
	target, nums, ops = setup()
	trial_history, best_individual = run_count_down(nums, ops, target, times = 10500)
	print('Best Population Fitness: {}'.format(min(trial_history)))
	print('1st Trial In Which It Occured: {}'.format(trial_history.index(min(trial_history))+1))
	print('Best Individual: {0}\nResult: {1}\nTarget: {2}'.format(best_individual[0], best_individual[1], target))