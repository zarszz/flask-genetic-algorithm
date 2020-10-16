import random
import math
import struct

num_of_population = 100
bound_min = -1
bound_max_x1 = 2
bound_max_x2 = 1
crossover_index = 3
probability_mutated = 0.05
a = 0.00005

"""
    populations data structure

    populations = [
        {
            "float": {
                "x1": float,
                "x2": float,
            },
            "binary": {
                "x1": binary,
                "x2": binary
            },
            "fitness": float,
            "probability": float,
        }
    ]
"""


def generate_population():
    populations = []
    for _ in range(num_of_population):
        populations.append({
            'float': {
                'x1': random.uniform(bound_min, bound_max_x1),
                'x2': random.uniform(bound_min, bound_max_x2),
            },
            'binary': 0,
            'fitness': 0,
            'probability': 0
        })
    return populations


def decode_chromosome(populations):
    binary_populations = []
    for data in populations:
        data['binary'] = {
            'x1': float_to_binary(data['float']['x1']),
            'x2': float_to_binary(data['float']['x2']),
        }
        binary_populations.append(binary_populations)
    return binary_populations


def float_to_binary(num):
    return ''.join(bin(c).replace('0b', '').rjust(8, '0') for c in struct.pack('!f', num))


def bin_to_float(binary):
    return struct.unpack('!f', struct.pack('!I', int(binary, 2)))[0]


def fitness_function(x1, x2):
    h = math.cos(x1) * math.sin(x2) - (x1 / (x2 ** 2 + 1))
    return 1 / (h + a)


def perform_fitness_calculation(populations):
    data_after_fitness = []
    for data in populations:
        fitness_value = fitness_function(data['float']['x1'], data['float']['x2'])
        data['fitness'] = fitness_value
        data_after_fitness.append(data)
    return data_after_fitness


def generate_individual_probability(populations):
    fitness = [population['fitness'] for population in populations]
    total_fit = float(sum(fitness))
    relative_fitness = [f / total_fit for f in fitness]
    for i in range(len(relative_fitness)):
        populations[i]['probability'] = sum(relative_fitness[:i + 1])
    return populations


def perform_roulette_select(populations):
    selected = []
    for individual in populations:
        rand_value = random.uniform(0, 1)
        if rand_value <= individual['probability']:
            selected.append(individual)
    return selected


def perform_single_point_crossover(selected_populations):
    crossed_data = []
    for individual in selected_populations:
        tmp = individual
        x1_string = individual['binary']['x1']
        x2_string = individual['binary']['x2']
        tmp['x1'] = str(x1_string[:crossover_index] + x2_string[crossover_index:]).encode('ascii')
        tmp['x2'] = str(x2_string[:crossover_index] + x1_string[crossover_index:]).encode('ascii')
        crossed_data.append(tmp)
    return crossed_data


def perform_binary_mutation(crossed_populations_data):
    mutated_data = []
    for individual in crossed_populations_data:
        tmp = individual
        rand_value = random.uniform(0, 1)
        if rand_value <= probability_mutated:
            x1_string = individual['binary']['x1']
            x2_string = individual['binary']['x2']
            x1_random_index, x2_random_index = random.randint(0, len(x1_string)), random.randint(0, len(x2_string))
            if x1_random_index == len(x1_string):
                x1_random_index = x1_random_index - 1
            if x2_random_index == len(x2_string):
                x2_random_index = x2_random_index - 1
            tmp['x1'] = swap_mutated_gene(x1_string, x1_random_index)
            tmp['x2'] = swap_mutated_gene(x2_string, x2_random_index)
        mutated_data.append(tmp)
    return mutated_data


def swap_mutated_gene(gene, gene_index):
    if gene[gene_index] == '0':
        return gene[:gene_index - 1] + '1' + gene[gene_index - 1:]
    elif gene[gene_index] == '1':
        return gene[:gene_index - 1] + '0' + gene[gene_index - 1:]
    else:
        return ''


def perform_steady_state(populations):
    result = []
    i = 0
    while i <= num_of_population:
        parent1 = perform_roulette_select(populations)
        parent2 = perform_roulette_select(populations)
        child1, child2 = perform_single_point_crossover(parent1), perform_single_point_crossover(parent2)
        child1 = perform_binary_mutation(child1)
        child2 = perform_binary_mutation(child2)
        best_population = select_best_fitness(child1=child1, parent1=parent1, child2=child2, parent2=parent2)
        best1, best2 = best_population[0], best_population[1]
        parent1 = best1
        parent2 = best2
        i += 1
        if i == num_of_population:
            result.append(parent1)
            result.append(parent2)
    return result


def select_best_fitness(child1, parent1, child2, parent2):
    best_fitness = []
    sorted_population = list(
        sorted(child1 + child2 + parent1 + parent2, key=lambda population: population['fitness'], reverse=True))
    best_fitness.append(
        {
            "fitness_value": sorted_population[0]['fitness'],
            "index": 0,
            "individual_data": sorted_population[0]
        })
    best_fitness.append({
        "fitness_value": sorted_population[1]['fitness'],
        "index": 1,
        "individual_data": sorted_population[1]
    })
    return best_fitness


def execute_steady_state():
    populations = generate_population()
    decode_chromosome(populations)
    perform_fitness_calculation(populations)
    generate_individual_probability(populations)
    result = perform_steady_state(populations)
    print("individu terbaik\n")
    print("x1 = " + result[0]["individual_data"]['binary']['x1'])
    print("x2 = " + result[0]["individual_data"]['binary']['x2'])
    print("nilai fitness = " + str(result[0]["fitness_value"]))
    return result
