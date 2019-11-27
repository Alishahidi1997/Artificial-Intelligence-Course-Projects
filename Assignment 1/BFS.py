import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import copy
import time


file_name = "test2"


class State:

  def __init__(self):
    self.food = set({})
    self.num_of_food = 0
    self.p = (0, 0)
    self.q = (0, 0)
    self.counter = 0


  def __eq__(self, other):
    return (self.num_of_food == other.num_of_food and self.food == other.food and self.p == other.p and self.q == other.q)

  def __hash__(self):
      return hash(([sum(x) for x in zip(*self.food)][0], [sum(x) for x in zip(*self.food)][1], self.num_of_food, self.p, self.q))

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


def movements(new_map, frontier, explored_states):
    depth = 0
    repeat_depth = 0
    best_depth = 0
    start = time.time()
    finish = False
    while len(frontier) != 0:
        if finish == True:
            break
        for j in range(-1, 2):
            for i in range(-1, 2):
                if i == 0 or j == 0 and not (i == 0 and j == 0):
                    new_pos = new_map[frontier[0].p[0] - j][frontier[0].p[1] - i]
                    if new_pos != "%" and ( new_pos != "2" or (new_pos == "2" and(frontier[0].p[0] - j, frontier[0].p[1] - i) not in frontier[0].food))\
                            and (frontier[0].p[0] - j, frontier[0].p[1] - i) != (frontier[0].q[0], frontier[0].q[1]):
                        front = copy.deepcopy(frontier[0])
                        front.p = (frontier[0].p[0] - j, frontier[0].p[1] - i)
                        front.counter += 1
                        repeat_depth += 1
                        if (front.p[0], front.p[1]) in frontier[0].food and(new_pos == "1" or new_pos == "3"):
                            front.num_of_food -= 1
                            front.food.remove((frontier[0].p[0] - j, frontier[0].p[1] - i))
                            # print(front.num_of_food)
                        if front.num_of_food == 0:
                            best_depth = front.counter
                            finish = True
                            break
                        if front not in explored_states:
                            frontier.append(front)
                            explored_states.add(front)
                            depth += 1

        for j in range(-1, 2):
            for i in range(-1, 2):
                if i == 0 or j == 0 and not (i == 0 and j == 0):
                    new_pos = new_map[frontier[0].q[0] - j ][frontier[0].q[1] - i]
                    if new_map[frontier[0].q[0] - j ][frontier[0].q[1] - i] != "%" and (new_pos != "1"  or (new_pos == "1" and
                                                                                   (frontier[0].q[0] - j, frontier[0].q[1] - i) not in frontier[0].food))\
                            and (frontier[0].q[0] - j, frontier[0].q[1] - i) != (frontier[0].p[0], frontier[0].p[1]):
                        front = copy.deepcopy(frontier[0])
                        front.q = (frontier[0].q[0] - j, frontier[0].q[1] - i)
                        front.counter += 1
                        repeat_depth += 1
                        # print(front.p)
                        if (front.q[0], front.q[1]) in frontier[0].food and (new_pos == "2"  or new_pos == "3"):
                            front.num_of_food -= 1
                            front.food.remove((frontier[0].q[0] - j, frontier[0].q[1] - i))
                        if front.num_of_food == 0:
                            best_depth = front.counter
                            finish = True
                            break
                        if front not in explored_states:
                            frontier.append(front)
                            explored_states.add(front)
                            depth += 1
        frontier.pop(0)

    end = time.time()
    print("Depth = ", best_depth)
    print("All movement = ", depth)
    print("All + repeated movement = ", repeat_depth)
    print("Duration = ", end - start)
    return best_depth, end - start

def bfs(map, frontier, explored_states):
    new_map = copy.deepcopy(map)
    new_explored_states = copy.deepcopy(explored_states)
    return movements(new_map, frontier, new_explored_states)


def main():
    # time = []
    # depth = []
    # file_name = [ "test2", "test3", "test4", "test5"]
    # for i in range(len(file_name)):
        map = [[]]
        frontier = []
        df = pd.read_csv(file_name)
        read_map(df, map)
        print_map(map)
        initial_state = map_pos_to_state(map)
        frontier.append(initial_state)
        explored_states = set({})
        explored_states.add(initial_state)
        d, t= bfs(map, frontier, explored_states)
    #     time.append(t)
    #     depth.append(d)
    # print(depth)
    # plt.scatter(depth, time)
    # plt.title("BFS")
    # plt.xlabel('depth')
    # plt.ylabel('time')
    # plt.show()

if __name__ == '__main__':
    main()