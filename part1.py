def get_heuristic_value(location):
    h_values = {
        'Starting point': 1,
        'Stormy ocean': 2,
        'Desert': 3,
        'Forest': 3,
        'Treasure': 0
    }
    return h_values.get(location, 0) #return heuristic value of certain location


def uniform_cost_search(start, goal, graph):
    visited = [] #keeps visited locations to look for new path if there is still unvisited locations
    parents = {} #keep parent previous location to achieve certain location. Updates if there is lesser cost parent
    costs = {} #total cost to arrive certain location

    # Make a priority queue with start location and its cost 0 by default
    pq = [(0, start)]
    costs[start] = 0
    print("Applying UCS:")

    # Continue until queue empty
    while pq:
        # Sort priority queue and pop location with lowest cost
        pq.sort()
        current_cost, current_location = pq.pop(0)

        # Visited new location
        if current_location not in visited:
            # Mark location as visited
            visited.append(current_location)
            for child, child_cost in graph[current_location]:
                # Calculate total cost by adding every child
                total_cost = current_cost + child_cost

                # If child(next) location is not visited and has less cost(discard previous path with higher cost)
                if child not in visited and (child not in costs or total_cost < costs[child]):
                    # Update cost and parent for next location
                    costs[child] = total_cost
                    parents[child] = current_location
                    # Add child location to queue
                    pq.append((total_cost, child))
                    # Display current path and cost
                    print(f"{current_location}–{child}: Cost is {total_cost}")

        # If we reach goal, recalcute path by iterating parents
        if current_location == goal:
            shortest_path = [current_location]
            while current_location in parents:
                current_location = parents[current_location]
                shortest_path.append(current_location)
            shortest_path.reverse()
            return current_cost, shortest_path

def uniform_cost_search_with_a_star(start, goal, graph):
    visited = []  # keeps visited locations to look for new path if there is still unvisited locations
    parents = {}  # keep parent previous location to achieve certain location. Updates if there is lesser cost parent
    costs = {}  # total cost to arrive certain location

    pq = [(get_heuristic_value(start), start)]  #this time add heuristic value for queue
    costs[start] = 0 #cost still 0 by default
    print("Applying A*:")

    while pq:
        pq.sort()
        current_cost, current_location = pq.pop(0)

        if current_location not in visited:
            visited.append(current_location)
            for child, child_cost in graph[current_location]:
                total_cost = current_cost + child_cost

                if child not in visited and (child not in costs or total_cost < costs[child]):
                    costs[child] = total_cost
                    parents[child] = current_location
                    # add heuristic value for total cost
                    pq.append((total_cost + get_heuristic_value(child), child))
                    print(f"{current_location}–{child}: Cost is {total_cost}")

        if current_location == goal:
            shortest_path = [current_location]
            while current_location in parents:
                current_location = parents[current_location]
                shortest_path.append(current_location)
            shortest_path.reverse()
            return costs[goal], shortest_path

if __name__ == '__main__':
    graph = dict()
    graph['Starting point'] = [['Stormy ocean', 4], ['Forest', 7]]
    graph['Stormy ocean'] = [['Desert', 4]]
    graph['Desert'] = [['Treasure', 10]]
    graph['Forest'] = [['Treasure', 4]]
    graph['Treasure'] = []

    cost, path = uniform_cost_search('Starting point', 'Treasure', graph)
    print(f"Solution Path: {'-'.join(path)} with total cost {cost}")
    print("------------------------")
    cost, path = uniform_cost_search_with_a_star('Starting point', 'Treasure', graph)
    print(f"Solution Path: {' '.join(path)} with total cost {cost}")
