import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import copy
import time
import collections

file_name = "test5"


class State:

  def __init__(self):
    self.food = set({})
    self.num_of_food = 0
    self.p = (0, 0)
    self.q = (0, 0)
    self.counter = 0

  def __eq__(self, other):
    return ( self.counter >= other.counter  and self.num_of_food == other.num_of_food and self.food == other.food and self.p == other.p and self.q == other.q)

  def __hash__(self):
      return hash(([sum(x) for x in zip(*self.food)][0], [sum(x) for x in zip(*self.food)][1], self.num_of_food, self.p, self.q, self.counter))


def split(word):
    return [char for char in word]


def read_map(df, map):
    list = df.values.tolist()
    map[0] = split(list[len(list)-1][len(list[0])-1])
    for i in range(len(list)):
        for j in range(len(list[i])):
            map.append(split(list[i][j]))


def print_map(map):
    for i in range(len(map)):
        for j in range(len(map[i])):
            print(map[i][j], end = '')
        print(" ")


def map_pos_to_state(map):
    state = State()
    for i in range(len(map)):
        for j in range(len(map[i])):
            if map[i][j] == "1":
                state.food.add((i, j))
                state.num_of_food += 1
            elif map[i][j] == "2":
                state.food.add((i, j))
                state.num_of_food += 1
            elif map[i][j] == "3":
                state.food.add((i, j))
                state.num_of_food += 1
            elif map[i][j] == "P":
                state.p = (i, j)
            elif map[i][j] == "Q":
                state.q = (i, j)
    print(" food states = ", state.food)
    print(" number of  food = ", state.num_of_food)
    print(" position q = ", state.q)
    print(" position p = ", state.p)
    return state


def in_explores_state(states, map):
    if map_pos_to_state(map) in states:
        return True
    return False



def movements(new_map, frontier, explored_states, initial_state):
    depth = 0
    repeat_state = 0
    finish = False
    current_depth = initial_state.num_of_food
    start = time.time()
    while finish != True:
        current_depth += 1
        # print(current_depth, "binnggg")
        explored_states = set({})
        explored_states.add(initial_state)
        frontier = collections.deque([State()])
        frontier[0] = copy.deepcopy(initial_state)
        while len(frontier) != 0:
            frontier_branch = []
            if frontier[0].counter < current_depth:
                    # if frontier[0].counter + 1 < current_depth:
                    #     for i in range(len(explored_states)):
                    #             if i == frontier[0].num_of_food:
                    #                 explored_states[i] = [x for x in explored_states[i] if x.counter < frontier[0].counter]
                    for j in range(-1, 2):
                        for i in range(-1, 2):
                            if i == 0 or j == 0 and not (i == 0 and j == 0):
                                new_pos = new_map[frontier[0].p[0] - j][frontier[0].p[1] - i]
                                if new_pos != "%" and (new_pos != "2" or(new_pos == "2" and (frontier[0].p[0] - j, frontier[0].p[1] - i) not in frontier[0].food )) \
                                        and (frontier[0].p[0] - j, frontier[0].p[1] - i) != (frontier[0].q[0], frontier[0].q[1]):
                                    front = copy.deepcopy(frontier[0])
                                    front.p = (frontier[0].p[0] - j, frontier[0].p[1] - i)
                                    front.counter += 1
                                    repeat_state += 1
                                    if (front.p[0], front.p[1]) in frontier[0].food and(new_pos == "1" or new_pos == "3"):
                                        front.num_of_food -= 1
                                        front.food.remove((frontier[0].p[0] - j, frontier[0].p[1] - i))
                                    if front.num_of_food == 0:
                                        finish = True
                                        break
                                    if front not in explored_states:
                                        depth += 1
                                        if front.counter < current_depth:
                                            frontier_branch.append(front)
                                            explored_states.add(front)

                    for j in range(-1, 2):
                        for i in range(-1, 2):
                            if i == 0 or j == 0 and not (i == 0 and j == 0):
                                new_pos = new_map[frontier[0].q[0] - j][frontier[0].q[1] - i]
                                if new_pos != "%" and (new_pos != "1" or(new_pos == "1" and (frontier[0].q[0] - j, frontier[0].q[1] - i) not in frontier[0].food)) \
                                        and (frontier[0].q[0] - j, frontier[0].q[1] - i) != (frontier[0].p[0], frontier[0].p[1]):
                                    front = copy.deepcopy(frontier[0])
                                    front.q = (frontier[0].q[0] - j, frontier[0].q[1] - i)
                                    front.counter += 1
                                    repeat_state += 1
                                    if (front.q[0], front.q[1]) in front.food and (new_pos == "2" or new_pos == "3"):
                                        front.num_of_food -= 1
                                        front.food.remove((frontier[0].q[0] - j, frontier[0].q[1] - i))
                                    if front.num_of_food == 0:
                                        finish = True
                                        break
                                    if front not in explored_states:
                                        depth += 1
                                        if front.counter < current_depth:
                                            frontier_branch.append(front)
                                            explored_states.add(front)

            del frontier[0]
            for i in range(len(frontier_branch)):
                frontier.insert(i, frontier_branch[i])
    end = time.time()

    print("Depth = ", current_depth)
    print("All movement = ", depth)
    print("All + repeated movement = ", repeat_state)
    print("Duration = ", end - start)
    return current_depth, end - start

def ids(map, frontier, explored_states, initial_state):
    new_map = copy.deepcopy(map)
    new_explored_states = copy.deepcopy(explored_states)
    return movements(new_map, frontier, new_explored_states, initial_state)


def main():
    # time = []
    # depth = []
    # file_name = [ "test2", "test3", "test4", "test5"]
    # for i in range(len(file_name)):
        map = [[]]
        frontier = collections.deque([])
        df = pd.read_csv(file_name)
        read_map(df, map)
        initial_state = map_pos_to_state(map)
        frontier.append(initial_state)
        explored_states = set({})
        explored_states.add(initial_state)
        print_map(map)
        d, t = ids(map, frontier, explored_states, initial_state)
    #     time.append(t)
    #     depth.append(d)
    # print(depth)
    # plt.scatter(depth, time)
    # plt.title("IDS")
    # plt.xlabel('depth')
    # plt.ylabel('time')
    # plt.show()


if __name__ == '__main__':
    main()