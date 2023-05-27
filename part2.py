def manhattan_distance(x, y):
    return abs(x[0] - y[0]) + abs(x[1] - y[1])
def get_neighbors(maze, position):
    x, y = position
    neighbors = []

    #check right
    new_x, new_y = x + 1, y
    if 0 <= new_x < len(maze) and 0 <= new_y < len(maze[0]) and maze[new_x][new_y] != '#': #,it is neighboor if it isn't wall or map boundary
        neighbors.append((new_x, new_y))

    #check left
    new_x, new_y = x - 1, y
    if 0 <= new_x < len(maze) and 0 <= new_y < len(maze[0]) and maze[new_x][new_y] != '#':
        neighbors.append((new_x, new_y))

    #check down
    new_x, new_y = x, y + 1
    if 0 <= new_x < len(maze) and 0 <= new_y < len(maze[0]) and maze[new_x][new_y] != '#':
        neighbors.append((new_x, new_y))

    #check up
    new_x, new_y = x, y - 1
    if 0 <= new_x < len(maze) and 0 <= new_y < len(maze[0]) and maze[new_x][new_y] != '#':
        neighbors.append((new_x, new_y))

    return neighbors


def get_cost(queue):
    return queue[0]  #return the cost from the first element


def uniform_cost_search(maze, start, goal):  #consider cost during queue priorty
    visited = []  #keeps visited locations
    queue = [(0, start, [])]  #create queue wit cost, current position, and path

    while queue:
        # sort queue by first element(cost)
        queue.sort(key=get_cost)

        # pop first item in the queue
        cost, current, path = queue.pop(0)

        #if the current position visited then skip
        if current in visited:
            continue
        visited.append(current)  #add the current position to visited

        if current == goal:
            return path + [current]  #return the path if goal has arrived

        #get list of neighbors of the current position
        neighbors = get_neighbors(maze, current)

        # add them to the queue with an updated cost and path
        for neighbor in neighbors:
            new_cost = cost + 1
            new_path = path + [current]
            queue.append((new_cost, neighbor, new_path))

    return None  #return none if can not find solution
def breadth_first_search(maze, start, goal): # Doesn't care cost just starts from left most element
    visited = []  # keeps visited locations
    queue = [(start, [])]  # create queue with current position and path

    while queue:
        # pop first item in the queue
        current, path = queue.pop(0)  #dont consider cost just select from left most element

        # if the current position is visited, then skip
        if current in visited:
            continue
        visited.append(current)  # add the current position to visited

        if current == goal:
            return path + [current]  # return the path if goal has arrived

        # get the list of neighbors of the current position
        neighbors = get_neighbors(maze, current)

        # add them to the queue with an updated cost and path
        for neighbor in neighbors:
            queue.append((neighbor, path + [current]))

    return None  # return None if cannot find a solution


def a_star_search(maze, start, goal): #combination of UCS and manhattan distance
    visited = []
    queue = [(manhattan_distance(start, goal), start, [])]

    while queue:
        queue.sort(key=get_cost)
        cost, current, path = queue.pop(0)

        if current in visited:
            continue
        visited.append(current)

        if current == goal:
            return path + [current]

        neighbors = get_neighbors(maze, current)
        for neighbor in neighbors: #calculate cost of g value h value then sum up to f value
            g_cost = len(path) + 1
            h_cost = manhattan_distance(neighbor, goal)
            new_cost = g_cost + h_cost
            new_path = path + [current]
            queue.append((new_cost, neighbor, new_path))

    return None

def find_start_and_treasure_positions(maze): #returns position of treasure and start point
    start_position = None
    goal_position = None

    for row in range(len(maze)):
        for col in range(len(maze[row])):
            cell = maze[row][col]

            if cell == 'S':  # If the cell contains the start symbol
                start_position = (row, col)
            elif cell == 'T':  # If the cell contains the goal symbol
                goal_position = (row, col)

            # If both start and goal positions are found, no need to continue searching
            if start_position is not None and goal_position is not None:
                return start_position, goal_position

    return start_position, goal_position


def read_maze(filename):
    with open(filename, "r") as file:
        maze = [list(line.strip()) for line in file]  #read the maze file
    return maze

def print_solution(maze, solution):
    if solution is None:
        print("No path found")
    else:
        # fill path with stars to track solution
        for step in solution:
            x, y = step
            if maze[x][y] not in ('S', 'T'):  # fill stars excluding start point and treasure
                maze[x][y] = '*'
        # print solution in the maze
        for row in maze:
            print(''.join(row))
    print("\n")
if __name__ == "__main__":

    mazefilename= "maze.txt"
    # read maze.txt
    maze = read_maze(mazefilename)
    # get start and goal positions
    start_position, treasure_position = find_start_and_treasure_positions(maze)

    # Uniform Cost Search
    print("Applying Uniform Cost Search:")
    solution = uniform_cost_search(maze, start_position, treasure_position)
    print_solution(maze, solution)

    # reset the maze
    maze = read_maze(mazefilename)

    # Breadth-First Search
    print("Applying Breadth-First Search:")
    solution = breadth_first_search(maze, start_position, treasure_position)
    print_solution(maze, solution)

    # reset the maze
    maze = read_maze(mazefilename)

    # A* Search
    print("Applying A* Search:")
    solution = a_star_search(maze, start_position, treasure_position)
    print_solution(maze, solution)