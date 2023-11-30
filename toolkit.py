from copy import deepcopy
import random
import time
from datetime import datetime

import numpy as np
import numpy.random as rand


startTime = time.time()

rng = rand.default_rng()

problem = {
    "compatibility": {
        "C1": ["S1", "S3"],
        "C2": ["S3", "S4"],
        "C3": ["S2", "S4"],
        "C4": ["S1", "S4"],
        "courtyard": ["S1", "S2", "S3"],
    },
    "capacity": {"C1": 3, "C2": 4, "C3": 4, "C4":6, "courtyard": 1000},
    "arrest": {
        "S1": 5,
        "S2": 8,
        "S3": 6,
        "S4": 6
    },
    "squads": ["S1", "S2", "S3", "S4"],
    "cells": ["C1", "C2", "C3", "C4", "courtyard"],
}

class matIndividual:
    def __init__(self, problem):
        # loading all problems elements
        self.compatibility = deepcopy(problem["compatibility"])
        self.capacity = deepcopy(problem["capacity"])
        self.toimprison = deepcopy(problem["arrest"])
        arrested = 0 
        for key in problem["arrest"].keys():
            arrested+=problem["arrest"][key]
        self.arrested = arrested
        self.squads = deepcopy(problem["squads"])
        self.squad2indice = {squad: i for i, squad in enumerate(self.squads)}
        self.cell_list = problem["cells"]
        self.cell2indice = {cell: i for i, cell in enumerate(self.cell_list)}
        self.cell2choice = {cell: None for cell in self.cell_list}
        del self.cell2choice["courtyard"]
        # reverse compatibility between cells and squads
        self.rev_compatibility = self.make_revcompatibility(self.compatibility)

        self.state = np.zeros((len(self.cell_list), len(self.squads)))
        rand_cell_list = deepcopy(list(self.cell_list[:-1]))
        rand.shuffle(rand_cell_list)
        # initialize the cells with a random value
        for cell in rand_cell_list:
            # fix squad
            squad = random.choice(problem["compatibility"][cell])
            self.cell2choice[cell] = squad
            cell_line = np.zeros( (1, len(self.squads)))
            # define max quantity for cell as min of his own capacity and remaining arrested number in the squad
            max_qty = min(self.toimprison[squad], self.capacity[cell])
            qty = random.randint(0, max_qty)
            #print(f"cell {cell} holds squad {squad}, {qty}/{max_qty} units.")
            cell_line[0][self.squad2indice[squad]] = qty

            self.state[self.cell2indice[cell]] = cell_line
            self.toimprison[squad] -= qty
        # compensate with courtyard for possible remaining squads members 
        courtyard_line = np.zeros( (1, len(self.squads)))
        for squad in self.squads:
            courtyard_line[0][self.squad2indice[squad]] = self.toimprison[squad]
        self.state[self.cell2indice["courtyard"]] = courtyard_line
    def mutate(self, rate_amount, rate_prop):
        # move out or move in some prisoners with courtyard
        # rate_amout change the amout of prisoners than can be exchanged
        # rate prop is the amount of cells that are choosen randomely for modification
        rand_cell_list = deepcopy(list(self.cell_list[:-1]))
        rand.shuffle(rand_cell_list)
        logs = []
        for i in range(int(len(rand_cell_list) * rate_prop)):
            cell = rand_cell_list[i]
            squad = self.cell2choice[cell]
            amount_in_cell = self.state[self.cell2indice[cell]][self.squad2indice[squad]]
            #amount_in_courtyard = self.state[self.cell2indice["courtyard"]][self.squad2indice[squad]]
    
            choices = ["in", "out", "reset_choice"]
    
            if random.choice(["in", "out"]) == "out":
                #print(f"move out from cell {cell}, squad {squad}, amount {amout_in_cell}/{self.capacity[cell]}, courtyard {amount_in_courtyard}")
                # move out matter from cell to courtyard
                left_courtyard_capa = (
                    int(self.capacity["courtyard"])
                    - int(self.state[self.cell2indice["courtyard"]].sum())
                )
                max_amount = min(amount_in_cell, left_courtyard_capa)
                min_amount = 0
                qty_to_move_out = random.randint(min_amount, int(max_amount * rate_amount))
                self.state[self.cell2indice[cell]][
                    self.squad2indice[squad]
                ] -= qty_to_move_out
                self.state[self.cell2indice["courtyard"]][
                    self.squad2indice[squad]
                ] += qty_to_move_out
                # print(f"Quantity to move {qty_to_move}")
                logs.append(
                    f"Moving out {qty_to_move_out} of squad {squad} from cell {cell} to courtyard"
                )
            else:
                # move in matter from courtyard to cell
                left_cell_capa = (
                    self.capacity[cell] - self.state[self.cell2indice[cell]].sum()
                )
                amount_in_courtyard = self.state[self.cell2indice["courtyard"]][
                    self.squad2indice[squad]
                ]
                max_amount = min(amount_in_courtyard, left_cell_capa)
                min_amount = 0
                qty_to_move_in = random.randint(min_amount, int(max_amount * rate_amount))
                self.state[self.cell2indice["courtyard"]][
                    self.squad2indice[squad]
                ] -= qty_to_move_in
                self.state[self.cell2indice[cell]][
                    self.squad2indice[squad]
                ] += qty_to_move_in
                logs.append(
                    f"Moving in {qty_to_move_in} of squad {squad} from courtyard to cell {cell}"
                )
        return logs
                
    def crossover(self, mixinInd, rate_prop):
        # to crossover features between cells, take randomely a cell 
        # from one individual and the other cell from mix in individual
        rand_cell_list = deepcopy(list(self.cell_list[:-1]))
        rand.shuffle(rand_cell_list)
        logs = []
        for i in range(int(len(rand_cell_list) * rate_prop)):
            cell = rand_cell_list[i]
            choice = random.choice(["self", "other"])
            if choice == "other":
                logs.append(
                    f"Crossover {cell} - {choice}"
                )
                old_cell = self.state[self.cell2indice[cell]]
                new_cell = mixinInd.state[mixinInd.cell2indice[cell]]
                diff_quantities = old_cell - new_cell
                projected_courtyard = (
                    self.state[self.cell2indice["courtyard"]] + diff_quantities
                )
                logs.append(
                    f"New {new_cell} - Old {old_cell} - Diff {diff_quantities} - CW {projected_courtyard}"
                )
                # courtyard must always be above zero, constraint
                test_above_zero = projected_courtyard >= np.zeros(
                    (1, len(projected_courtyard))
                )
                test_below_capa = projected_courtyard.sum() < self.capacity["courtyard"]
                if test_above_zero.all() and test_below_capa:
                    self.state[self.cell2indice[cell]] = new_cell
                    self.state[self.cell2indice["courtyard"]] = projected_courtyard
        return logs


    
    def evaluate(self):
        # The objective function is the cell number of prisonners
        self.fitness = 0
        sum = self.state[self.cell2indice["courtyard"]].sum()

        self.fitness = self.arrested - sum

    def make_revcompatibility(self, compatibility):
        """
        Creates the reverse compatibility of Squad --> Cell
        from Cell --> Squad
        """
        rev_compat = {}
        for squad in self.toimprison.keys():
            rev_compat[squad] = []
            for cell, squads_list in compatibility.items():
                if squad in squads_list:
                    rev_compat[squad].append(cell)
        return rev_compat


class matPopulation:
    def __init__(self, problem, size=100, rate_prop=0.5, rate_amount=1, tournament_size=3):
        # Create individuals
        self.individuals = []
        for i in range(size):
            self.individuals.append(matIndividual(problem=problem))
            #print(f"created {i} individuals")
            #print(f"generated in individual {i}")
        self.individuals = [matIndividual(problem=problem) for _ in range(size)]
        # Store the best individuals
        best = matIndividual(problem)
        best.evaluate()
        self.best = [best]
        # Mutation rate
        # self.base_rate = rate
        self.rate_prop = rate_prop
        self.rate_amount = rate_amount
        

    def sort(self):
        self.individuals = sorted(self.individuals, key=lambda indi: indi.fitness, reverse=True)

    def enhance(self):
        parents = []

        # add the 3 best
        for ind in self.individuals[:3]:
            parents.append(ind)
        
        # roulette selection
        while len(parents) < 10:
            max = sum([i.fitness for i in self.individuals])
            selection_probs = [i.fitness/max for i in self.individuals]
            parents.append(self.individuals[rand.choice(len(self.individuals), p=selection_probs)])
        
        # Create new childs individuals from parents
        newIndividuals = []
        # Go through top 10 individuals - mutate
        for individual in parents:
            # Create 1 exact copy of each top 10 individuals
            newIndividuals.append(deepcopy(individual))
            # Create 4 mutated individuals
            for _ in range(4):
                newIndividual = deepcopy(individual)
                newIndividual.mutate(
                    rate_amount=self.rate_amount,
                    rate_prop=self.rate_prop
                )
                newIndividuals.append(newIndividual)
        # create 10 pairs of individuals - crossover
        pairs = [(random.choice(parents), random.choice(parents)) for _ in range(10)]
        for pair in pairs:
            parent1, parent2 = pair
            newIndividual_parent1 = deepcopy(parent1)
            newIndividual_parent2 = deepcopy(parent2)

            newIndividual_parent1.crossover(
                mixinInd=newIndividual_parent2,
                rate_prop=self.rate_prop
            )
            newIndividuals.append(newIndividual_parent1)
        
        # Replace the old population with the new population of offsprings
        self.individuals = newIndividuals
        self.evaluate()
        self.sort()
        # Store the new best individual
        self.best.append(self.individuals[0])
        # Increment the mutation rate if the population didn't change
        # if self.best[-1].fitness == self.best[-2].fitness:
            # self.rate += self.base_rate * 0.1
        # else:
            # self.rate = self.base_rate

    def evaluate(self):
        for indi in self.individuals:
            indi.evaluate()

def prettydf(x):
    if x == 0:
        return ""
    else:
        return f"{x} 👤"


def state_generator(session_state):
    for tracker in [
    'clicked_generation',
    'clicked_mutation',
    'clicked_sorted',
    'clicked_featurecross',
    'clicked_generation_evolution',
    'mutated',
    'featurecrossed',
    'generated',
    'generated_mutation',
    'generated_featurecross',
    'generated_evolution',
    'sorted',
    'evolved'
]:
        session_state[tracker] = False

    session_state.generated = False
    session_state.individuals = []

    if tracker not in session_state:
        session_state[tracker] = False
    match tracker:
        case 'generated_mutation':
            session_state.individual = None
        case 'generated_featurecross':
            session_state.individual_1 = None
            session_state.individual_2 = None
        case 'mutated':
            session_state.individual_mutated = None
            
    session_state.loaded = True
