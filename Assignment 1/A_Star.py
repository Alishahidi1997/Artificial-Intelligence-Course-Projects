import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import copy
import time
import heapq


file_name = "test2"


class State:

  def __init__(self):
    self.counter = 0
    self.food = set({})
    self.food_p = []
    self.food_q = []
    self.food_pq = []
    self.num_of_food = 0
    self.p = (0, 0)
    self.q = (0, 0)
    self.hu_cost = 0

  def __gt__(self, other):
    return self.hu_cost > other.hu_cost

  def __eq__(self, other):
    return self.num_of_food == other.num_of_food and self.food == other.food and self.p == other.p and self.q == other.q

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
                state.food_p.append((i, j))
                state.food.add((i,j))
                state.num_of_food += 1
            elif map[i][j] == "2":
                state.food_q.append((i, j))
                state.food.add((i, j))
                state.num_of_food += 1
            elif map[i][j] == "3":
                state.food_pq.append((i, j))
                state.food.add((i, j))
                state.num_of_food += 1
            elif map[i][j] == "P":
                state.p = (i, j)
            elif map[i][j] == "Q":
                state.q = (i, j)
    print(" food states = ", state.food_pq, state.food_p, state.food_q)
    print(" number of  food = ", state.num_of_food)
    print(" position q = ", state.q)
    print(" position p = ", state.p)
    return state


def in_explores_state(states, map):
    if map_pos_to_state(map) in states:
        return True
    return False


def calculate_huristic(front, agent):
    min = 100000
    if agent == "P":
        for i in range(len(front.food_p)):
            dist = abs(front.p[0] - front.food_p[i][0]) + abs(front.p[1] - front.food_p[i][1])
            if min > dist:
                min = dist
    if agent == "Q":
        for i in range(len(front.food_q)):
            dist = abs(front.q[0] - front.food_q[i][0]) + abs(front.q[1] - front.food_q[i][1])
            if min > dist:
                min = dist
    for i in range(len(front.food_pq)):
        dist = abs(front.p[0] - front.food_pq[i][0]) + abs(front.p[1] - front.food_pq[i][1])
        distq = abs(front.q[0] - front.food_pq[i][0]) + abs(front.q[1] - front.food_pq[i][1])
        if dist > distq:
            dist = distq
        if min > dist:
            min = dist
    return min


def movements(new_map, frontier, explored_states):
    depth = 0
    repeat_depth = 0
    best_depth = 0
    start = time.time()
    finish = False
    while len(frontier)!=0:
        if finish == True:
            break
        fronts = heapq.heappop(frontier)
        for j in range(-1, 2):
            for i in range(-1, 2):
                if i == 0 or j == 0 and not (i == 0 and j == 0):
                    new_pos = new_map[fronts.p[0] - j][fronts.p[1] - i]
                    if new_pos != "%" and (new_pos != "2" or (
                            new_pos == "2" and (fronts.p[0] - j, fronts.p[1] - i) not in fronts.food)) \
                            and (fronts.p[0] - j, fronts.p[1] - i) != (fronts.q[0], fronts.q[1]):
                        front = copy.deepcopy(fronts)
                        front.p = (fronts.p[0] - j, fronts.p[1] - i)
                        front.counter += 1
                        repeat_depth += 1
                        if (front.p[0], front.p[1]) in fronts.food and (new_pos == "1" or new_pos == "3"):
                            front.num_of_food -= 1
                            front.food.remove((front.p[0], front.p[1]))
                            if new_pos == "1":
                                front.food_p.remove((front.p[0], front.p[1]))
                            elif new_pos == "3":
                                front.food_pq.remove((front.p[0], front.p[1]))
                        if front.num_of_food == 0:
                            best_depth = front.counter
                            finish = True
                            break
                        front.hu_cost = calculate_huristic(front, "P") + front.counter
                        if front not in explored_states:
                            explored_states.add(front)
                            depth += 1
                            heapq.heappush(frontier, front)

        for j in range(-1, 2):
            for i in range(-1, 2):
                if i == 0 or j == 0 and not (i == 0 and j == 0):
                    new_pos = new_map[fronts.q[0] - j][fronts.q[1] - i]
                    if new_pos != "%" and (new_pos != "1" or (
                            new_pos == "1" and (fronts.q[0] - j, fronts.q[1] - i) not in fronts.food)) \
                            and (fronts.q[0] - j, fronts.q[1] - i) != (fronts.p[0], fronts.p[1]):
                        front = copy.deepcopy(fronts)
                        front.q = (fronts.q[0] - j, fronts.q[1] - i)
                        front.counter += 1
                        repeat_depth += 1
                        if (front.q[0], front.q[1]) in fronts.food and (new_pos == "2" or new_pos == "3"):
                            front.num_of_food -= 1
                            front.food.remove((front.q[0], front.q[1]))
                            if new_pos == "2":
                                front.food_q.remove((front.q[0], front.q[1]))
                            elif new_pos == "3":
                                front.food_pq.remove((front.q[0], front.q[1]))
                        if front.num_of_food == 0:
                            best_depth = front.counter
                            finish = True
                            break
                        front.hu_cost = calculate_huristic(front, "Q") + front.counter
                        if front not in explored_states:
                            explored_states.add(front)
                            depth += 1
                            heapq.heappush(frontier, front)

    end = time.time()
    print("Depth = ", best_depth)
    print("All movement = ", depth)
    print("All + repeated movement = ", repeat_depth)
    print("Duration = ", end - start)
    return best_depth, end - start

def A(map, frontier, explored_states):
    new_map = copy.deepcopy(map)
    new_explored_states = copy.deepcopy(explored_states)
    return movements(new_map, frontier, new_explored_states)


def main():
    # time = []
    # depth = []
    # file_name = [ "test2", "test3", "test4", "test5"]
    # for i in range(len(file_name)):
        df = pd.read_csv(file_name)
        map = [[]]
        frontier = []
        read_map(df, map)
        initial_state = map_pos_to_state(map)
        heapq.heappush(frontier, initial_state)
        explored_states = set({})
        explored_states.add(initial_state)
        explored_states.add(initial_state)
        print_map(map)
        d,t = A(map, frontier, explored_states)
        # time.append(t)
        # depth.append(d)
    # print(depth)
    # plt.scatter(depth, time)
    # plt.title("A*")
    # plt.xlabel('depth')
    # plt.ylabel('time')
    # plt.show()

if __name__ == '__main__':
    main()