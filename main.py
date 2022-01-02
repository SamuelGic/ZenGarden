import random
import copy
import time
from random import randint
from termcolor import colored


def create_matrix(state, matrix):
    new_matrix = copy.deepcopy(matrix)
    y = len(new_matrix)
    x = len(new_matrix[0])
    num_of_entries = 2 * (y + x)

    direction = ""
    stuck = False
    num = 0
    count = 0
    random_count = num_of_entries / 2

    for i in state:
        count += 1
        # last 5 indexes of state list are random decisions
        if count > num_of_entries:
            continue

        route_length = 0
        if stuck:
            break
        # starting at the top
        if i < x:
            # starting position will be in first line
            start_y = 0
            # ... and in i-column
            start_x = i
            direction = "down"
        # starting at the right side
        elif x <= i < (x + y):
            # starting position will be in (i - x)-line
            start_y = i - x
            # ... and in last column
            start_x = x - 1
            direction = "left"
        # starting at the bottom
        elif (x + y) <= i < ((2 * x) + y):
            # starting position will be in last line
            start_y = y - 1
            # ... and in [((2 * x + y) - 1) - i]-column
            start_x = ((2 * x + y) - 1) - i
            direction = "up"
        # starting at the left side
        else:
            # starting position will be in [(2 * (x + y) - 1) - i]-line
            start_y = (2 * (x + y) - 1) - i
            # ... and in first column
            start_x = 0
            direction = "right"

        # if there is either obstacle or already raked box
        if new_matrix[start_y][start_x] != 0:
            # we'll go to the next starting position
            continue
        # he can enter map
        else:
            # number of route
            num += 1
            # he will rake first box
            new_matrix[start_y][start_x] = num
            route_length += 1

        monk_y = start_y
        monk_x = start_x
        end = False

        while not end:
            old_y = monk_y
            old_x = monk_x
            # we will change his coordinates depending on the direction he is moving
            if direction == "up":
                monk_y -= 1
            elif direction == "down":
                monk_y += 1
            elif direction == "right":
                monk_x += 1
            elif direction == "left":
                monk_x -= 1

            # if he is out of matrix
            if monk_x >= x or monk_x < 0 or monk_y >= y or monk_y < 0:
                end = True
                break

            # if the box is not raked, monk will rake it
            if new_matrix[monk_y][monk_x] == 0:
                new_matrix[monk_y][monk_x] = num
                route_length += 1
            # if there is obstacle or already raked box
            elif new_matrix[monk_y][monk_x] != 0:
                # he will go one step back
                monk_y = old_y
                monk_x = old_x

                # we need to change direction he is going
                # if he is going up/down
                if direction == "up" or direction == "down":
                    # if he can move either to the left or to the right
                    if (monk_x - 1) >= 0 and (monk_x + 1) < x and new_matrix[monk_y][monk_x - 1] == 0 and \
                            new_matrix[monk_y][monk_x + 1] == 0:
                        # he will choose one side (randomly)
                        if random_count < len(state) / 2:
                            option = state[random_count]
                            random_count += 1
                        else:
                            random_count = int(num_of_entries / 2)
                            option = state[random_count]
                            random_count += 1

                        if option == 0:
                            # he will go left
                            monk_x -= 1
                            direction = "left"
                        elif option == 1:
                            # he wil go right
                            monk_x += 1
                            direction = "right"
                    # elif he can move only to the left
                    elif (monk_x - 1) >= 0 and new_matrix[monk_y][monk_x - 1] == 0:
                        monk_x -= 1
                        direction = "left"
                    # elif he can move only to the right
                    elif (monk_x + 1) < x and new_matrix[monk_y][monk_x + 1] == 0:
                        monk_x += 1
                        direction = "right"
                    # if he is on the edge of the map, he can leave the map
                    elif monk_x == 0 or monk_x == x - 1 or monk_y == 0 or monk_y == y - 1:
                        # if he entered map not on the corner and there is only one free box, he can not rake this box
                        # if it is corner box, he can rake it even if it is the only free box
                        if route_length == 1 and not (monk_y == 0 and monk_x == 0) and not (
                                monk_y == 0 and monk_x == x - 1) and not (monk_y == y - 1 and monk_x == 0) and not (
                                monk_y == y - 1 and monk_x == x - 1):
                            new_matrix[monk_y][monk_x] = 0
                            num -= 1
                        end = True
                        break
                    # he is stucked -> Game Over
                    else:
                        end = True
                        stuck = True
                        break
                # if he is going left/right
                elif direction == "left" or direction == "right":
                    # if he can move either up or down
                    if (monk_y - 1) >= 0 and (monk_y + 1) < y and new_matrix[monk_y - 1][monk_x] == 0 and \
                            new_matrix[monk_y + 1][monk_x] == 0:
                        # he will choose one side (randomly)
                        if random_count < len(state) / 2:
                            option = state[random_count]
                            random_count += 1
                        else:
                            random_count = int(num_of_entries / 2)
                            option = state[random_count]
                            random_count += 1

                        if option == 0:
                            # he will go up
                            monk_y -= 1
                            direction = "up"
                        elif option == 1:
                            # he wil go down
                            monk_y += 1
                            direction = "down"
                    # elif he can move only up
                    elif (monk_y - 1) >= 0 and new_matrix[monk_y - 1][monk_x] == 0:
                        monk_y -= 1
                        direction = "up"
                    # elif he can move only down
                    elif (monk_y + 1) < y and new_matrix[monk_y + 1][monk_x] == 0:
                        monk_y += 1
                        direction = "down"
                    # if he is on the edge of the map, he can leave the map
                    elif monk_x == 0 or monk_x == x - 1 or monk_y == 0 or monk_y == y - 1:
                        # if he entered map not on the corner and there is only one free box, he can not rake this box
                        # if it is corner box, he can rake it even if it is the only free box
                        if route_length == 1 and not (monk_y == 0 and monk_x == 0) and not (
                                monk_y == 0 and monk_x == x - 1) and not (monk_y == y - 1 and monk_x == 0) and not (
                                monk_y == y - 1 and monk_x == x - 1):
                            new_matrix[monk_y][monk_x] = 0
                            num -= 1
                        end = True
                        break
                    # he is stucked -> Game Over
                    else:
                        end = True
                        stuck = True
                        break

                # he will rake new box
                new_matrix[monk_y][monk_x] = num
                route_length += 1

    return new_matrix


def fitness(matrix):

    # number of boxes raked
    count = 0
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j] > 0:
                count += 1

    return count


def number_of_rocks(matrix):
    # it returns number of boxes to be raked (empty boxes)
    count = 0
    for y in range(len(matrix)):
        for x in range(len(matrix[y])):
            if matrix[y][x] == -1:
                count += 1
    return count


def print_matrix(matrix):
    # change elements of matrix to strings for the better printout
    for y in range(len(matrix)):
        for x in range(len(matrix[y])):
            if matrix[y][x] != -1 and matrix[y][x] < 10:
                matrix[y][x] = "0" + str(matrix[y][x])
            else:
                matrix[y][x] = str(matrix[y][x])

    # printing out new matrix
    print("-----------------------------------------------------------------------")
    for y in range(len(matrix)):
        print(colored(matrix[y], 'blue'))


def create_chromosome(number):

    gene = random.sample(range(1, number), int(number/2))
    for i in range(5):
        gene.append(randint(0, 1))

    return gene


def elitism(matrix):

    y = len(matrix)
    x = len(matrix[0])
    num_of_entries = 2 * (y + x)
    generation = 1
    found = False
    population = []
    rocks = number_of_rocks(matrix)
    number_of_population = 50

    for i in range(number_of_population):
        gnome = create_chromosome(num_of_entries)
        population.append(gnome)

    while not found:

        for l in range(number_of_population):
            sBest = population[l]
            bestMatrix = create_matrix(sBest, matrix)
            bestFitness = fitness(bestMatrix)
            population[l].append(bestFitness)
            if bestFitness == ((x * y) - rocks):
                found = True

        population = sorted(population, key=lambda k: k[len(population[0]) - 1], reverse=True)

        for k in range(number_of_population):
            population[k].pop(len(population[k]) - 1)

        # Otherwise generate new offsprings for new generation
        new_generation = []

        # Perform Elitism, that mean 10% of fittest population
        # goes to the next generation
        s = int((10 * number_of_population) / 100)
        new_generation.extend(population[:s])

        # From 50% of fittest population, Individuals
        # will mate to produce offspring
        s = int((90 * number_of_population) / 100)
        for _ in range(s):
            parent1 = random.choice(population[:50])
            parent2 = random.choice(population[:50])
            child = []
            point = randint(0, x + y - 3)

            for j in range(point):
                child.append(parent1[j])

            for j in range(point, len(population[0])):
                child.append(parent2[j])

            point = randint(2, x + y - 1)
            child[point] = randint(0, num_of_entries)
            new_generation.append(child)


        population = new_generation
        generation += 1
        
        if generation == 1000:
            break

    for l in range(number_of_population):
        sBest = population[l]
        bestMatrix = create_matrix(sBest, matrix)
        bestFitness = fitness(bestMatrix)
        population[l].append(bestFitness)

    population = sorted(population, key=lambda k: k[len(population[0]) - 1], reverse=True)
    bestMatrix = create_matrix(population[0], matrix)
    print("Počiatočná mapa:")
    print_matrix(matrix)
    print("Výsledná mapa:")
    print_matrix(bestMatrix)
    print("Generacia ", generation)
    print(population[0])


def tournament(matrix):
    y = len(matrix)
    x = len(matrix[0])
    num_of_entries = 2 * (y + x)
    generation = 1
    found = False
    population = []
    rocks = number_of_rocks(matrix)
    number_of_population = 50

    for i in range(number_of_population):
        gnome = create_chromosome(num_of_entries)
        population.append(gnome)

    while not found:

        for l in range(number_of_population):
            sBest = population[l]
            bestMatrix = create_matrix(sBest, matrix)
            bestFitness = fitness(bestMatrix)
            if bestFitness == ((x * y) - rocks):
                found = True

        new_generation = []

        for i in range(number_of_population):
            parent1 = population[randint(0, 49)]
            parent2 = population[randint(0, 49)]
            parent3 = population[randint(0, 49)]
            parent4 = population[randint(0, 49)]

            par_1_mat = create_matrix(parent1, matrix)
            par_2_mat = create_matrix(parent2, matrix)
            par_3_mat = create_matrix(parent3, matrix)
            par_4_mat = create_matrix(parent4, matrix)

            par_1_fit = fitness(par_1_mat)
            par_2_fit = fitness(par_2_mat)
            par_3_fit = fitness(par_3_mat)
            par_4_fit = fitness(par_4_mat)

            if par_1_fit > par_2_fit:
                final_parent1 = parent1

            else:
                final_parent1 = parent2

            if par_3_fit > par_4_fit:
                final_parent2 = parent3

            else:
                final_parent2 = parent4

            child = []
            point = randint(0, x + y - 3)

            for j in range(point):
                child.append(final_parent1[j])

            for j in range(point, len(population[0])):
                child.append(final_parent2[j])

            point = randint(2, x + y - 1)
            child[point] = randint(0, num_of_entries)
            new_generation.append(child)

        population = new_generation
        generation += 1

        if generation == 1000:
            break

    for l in range(number_of_population):
        sBest = population[l]
        bestMatrix = create_matrix(sBest, matrix)
        bestFitness = fitness(bestMatrix)
        population[l].append(bestFitness)

    population = sorted(population, key=lambda k: k[len(population[0]) - 1], reverse=True)
    mat = population[0]
    bestMatrix = create_matrix(mat, matrix)
    print("Počiatočná mapa:")
    print_matrix(matrix)
    print("Výsledná mapa:")
    print_matrix(bestMatrix)
    print("Generacia ", generation)
    print(mat)

if __name__ == '__main__':
    """
    1.test:
    
    garden = [
        [00, 00, 00, 00],
        [00, -1, 00, 00],
        [00, 00, 00, 00],
        [00, 00, 00, 00],
    ]
    
    2.test:
    """
    garden = [
        [00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00],
        [00, 00, 00, 00, 00, -1, 00, 00, 00, 00, 00, 00],
        [00, -1, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00],
        [00, 00, 00, 00, -1, 00, 00, 00, 00, 00, 00, 00],
        [00, 00, -1, 00, 00, 00, 00, 00, 00, 00, 00, 00],
        [00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00],
        [00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00],
        [00, 00, 00, 00, 00, 00, 00, 00, -1, -1, 00, 00],
        [00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00],
        [00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00],
        [00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00],
    ]
    """
    3.test:
    
    garden = [
        [00, -1, 00, 00, 00, 00, 00],
        [00, 00, 00, 00, 00, -1, 00],
        [00, 00, 00, 00, 00, 00, 00],
        [00, 00, -1, 00, 00, 00, 00],
        [00, 00, 00, 00, 00, 00, 00],
        [00, 00, 00, 00, 00, -1, 00],
        [00, 00, 00, 00, 00, 00, 00],
    ]
    
    4.test:
    
    garden = [
        [00, -1, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00],
        [00, 00, 00, 00, 00, -1, 00, 00, 00, 00, 00, 00],
        [00, -1, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00],
        [00, 00, 00, 00, -1, 00, 00, 00, 00, 00, 00, 00],
        [00, 00, -1, 00, 00, 00, 00, 00, 00, 00, 00, 00],
        [00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00],
        [00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00],
        [00, 00, 00, 00, 00, 00, 00, 00, -1, -1, 00, 00],
        [00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00],
        [00, 00, -1, 00, 00, 00, 00, 00, 00, 00, 00, 00],
        [00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00],
    ]
    
    5.test:
    
    garden = [
        [00, 00, 00, 00, 00, 00, 00],
        [00, 00, 00, 00, 00, -1, 00],
        [00, 00, 00, 00, 00, 00, 00],
        [00, 00, -1, 00, 00, 00, 00],
        [00, 00, 00, 00, 00, 00, 00],
        [00, 00, 00, 00, 00, -1, 00],
        [00, 00, 00, 00, 00, 00, 00],
    ]
    
    6.test:
    

    garden = [
        [00, 00, 00, -1],
        [00, -1, 00, 00],
        [00, 00, -1, 00],
        [00, 00, 00, 00],
    ]
    """

    start = time.time()
    elitism(garden)
    # turnaj(garden)
    end = time.time()
    print(end - start)