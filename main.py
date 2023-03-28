import random


def txt_files_to_dict(names_txt_file, dist_txt_file):
    """
    Helper Function
    This function takes two '.txt' files as input. First, the function will attempt to open to files and will prompt an
    error message if one of the files is not found. If both files are found in the directory, then File Handling will
    be used to create a dictionary containing key-values pairs in the format:
    (key, value) = (city_name, list_of_distances)
    This will allow us to easily manage and work with our data in future functions.
    :param names_txt_file: The txt file containing the names of the cities.
    :param dist_txt_file: The txt file containing a list of distances from the selected city to any other city.
    :return: A dictionary containing the city names and distances.
    """
    # Error Handling
    # Looping to test each file input
    for file in [names_txt_file, dist_txt_file]:
        # Will attempt to open the file
        try:
            open(file, "r")
        # If the file fails to open, an exception and an error message is passed to the user.
        except FileNotFoundError:
            print(f"File {file} does not exist.")

    # Initializing an empty dictionary
    dictionary = {}

    # Opening both files in 'Read' mode
    with open(names_txt_file, "r") as names_txt, open(dist_txt_file, "r") as dist_txt:
        # 'zip' allows us to iterate over both files at once
        # Note: zip is not the same as a nested for loop, it will iterate over the first line of each file, then the
        # second line of each file, etc.
        for line1, line2 in zip(names_txt, dist_txt):
            # Extracting the city name from the names file to be used as the dictionary key.
            # By default, the key will be in a list.
            key_list = line1.strip().split("\n")
            # Converting the key to a string.
            key = key_list[0]

            # Extracting the string of values from the dist file to be used as the dictionary values
            value_string = line2.strip().split("\n")
            # Splitting the single value_string into separate strings for each distance present
            value_string_parts = value_string[0].split()
            # Converting the distance strings into floats, so we can perform mathematical operations on them later
            value_ints = [float(value) for value in value_string_parts]

            # Creating an entry in the dictionary
            dictionary[key] = value_ints

    return dictionary


def count_distance(tour_list, cities_dictionary):
    """
    Helper Function
    This function takes a list of strings and the main dictionary as input. Using some clever indexing, the distance
    between each consecutive city is recorded and summed. The distance between the first and last city is also counted
    so the entire tour completes a loop.
    :param tour_list: The list containing the order of cities traveled.
    :param cities_dictionary: The dictionary containing all cities and their distances to each other.
    :return: The sum of distance traveled.
    """
    total_distance = 0

    for city in tour_list:
        # Finding the index of the city, so we do not have to work with the string
        city_tour_index = tour_list.index(city)
        # True when the last city in the tour_list is selected
        if city_tour_index == len(tour_list)-1:
            # Defining the next_city as the first city of tour_list to complete the route loop
            next_city = tour_list[0]
        # When any city besides the last is selected
        else:
            # Finding the next city tour index and using that to extract the next_city from the tour_list
            next_city_tour_index = city_tour_index + 1
            next_city = tour_list[next_city_tour_index]
        # To find the dictionary index of the next city, we need to index the list of (ordered) dictionary keys.
        # Note: The index location in the main dictionary of a particular city is the same as that cities index
        # all distance lists
        next_city_dict_index = list(cities_dictionary.keys()).index(next_city)
        # A single distance is calculated by finding the distance associated with the next_cities index
        single_distance = cities_dictionary[city][next_city_dict_index]
        total_distance += single_distance

    return total_distance


def is_in_tour_list(cities, tour, city_idx):
    """
    Helper Function
    Checks if the shortest_distance index is a part of a previously used city in a tour.
    :param cities: City/Distance dictionary
    :param tour: Current tour
    :param city_idx: index of potential next city in dictionary value list
    :return: Boolean value
    """
    # Creating a list of main dictionary keys and using indexing to select the "current city"
    current_city = list(cities.items())[city_idx][0]
    # If the current city is already in the tour, return true
    if current_city in tour:
        return True
    return False


def mutate(tour):
    """
    Helper Function
    This function takes a tour list as input and randomly selects and swaps two elements of the list.
    :param tour: Tour list to be mutated
    :return: A tour with two elements swapped
    """
    # Using the random package to randomly select an index of the tour.
    first = random.randint(0, len(tour)-1)
    second = random.randint(0, len(tour)-1)
    # Using tuple swapping to switch the values located at the indices
    (tour[first], tour[second]) = (tour[second], tour[first])

    return tour


def tsp_greedy(name_file, distance_file):
    """
    Main Function
    This function uses the Greedy Algorithm to find a solution to the Traveling Salesman Problem.
    :param name_file: The *.txt file containing the city names in order.
    :param distance_file: The *.txt file containing the distances from one city to another, in order.
    :return: A list of city names (strings) that has the shortest distance.
    """
    # Convert files to usable data
    # --> txt_files_to_dict()
    cities = txt_files_to_dict(name_file, distance_file)
    # Initializing tour with starting city
    tour = list()
    # Forcing the FIRST city to the tour
    tour.append(list(cities.keys())[0])

    # Will loop until tour has used all available cities
    while len(tour) < len(cities):
        # Initializing the shortest path and selecting the current city as the last city in the tour list
        shortest_path = 130000
        current_city = tour[-1]
        # Looping over each distance related to the current city
        for distance in cities.get(current_city):

            # potential methods of determining if smallest dist found is not in tour list yet
            # A) Keep track of used index values >> pass over used indices when
            # finding next shortest distance(starting with idx 0 for alpha)
            #

            if distance < shortest_path and distance != 0:
                if not is_in_tour_list(
                        cities,
                        tour,
                        cities.get(current_city).index(distance)
                ):
                    shortest_path = distance

        shortest_path_idx = cities.get(current_city).index(shortest_path)
        shortest_path_city = list(cities.items())[shortest_path_idx][0]
        tour.append(shortest_path_city)

    # Determines the key/name of the lowest distance to next city available
    # least_dist_idx = cities.get(current_city).index(shortest_path)
    # print(list(cities.items())[least_dist_idx][0])

    # If distance in tour list -> do none
    # if distance not in tour list -> add next city
    return tour


def tsp_mutation(name_file, distance_file):
    """
    Main Function
    This function uses a Mutation Algorithm to find a solution to the Traveling Salesman Problem. The function 
    stagnates when two consecutive iterations give the same best child. The best child is then mutated three times
    and is saved in a list. Once the function stagnates five times, the shortest route from the list is returned.
    :param name_file: text file with names of city formatted in desired way
    :param distance_file: text file with distances between cities as they appear on name file
    :return: a tour of the cities with the smallest distance found via mutation algorithm
    """
    # Convert text files to usable dictionary for our purposes
    cities = txt_files_to_dict(name_file, distance_file)
    # Initialize a tour for mutating
    tour = list()
    # List of potential solutions that we will compare at the end
    potential_solutions = list()
    best_solution = list(cities.keys())
    
    # Creating an initial tour
    for city in cities:
        tour.append(city)
        
    # Begin mutation process
    # This is our termination criteria
    while len(potential_solutions) < 5:
        # Copy for stagnation comparison
        original_tour_copy = tour.copy()
        for x in range(0, 100):
            # This function performs the desired mutation
            child = mutate(tour.copy())
            # Check to see if mutation is better than original
            if count_distance(child, cities) < count_distance(tour, cities):
                # Update original
                tour = child
        # Check for stagnation after a generation
        if count_distance(tour, cities) == count_distance(original_tour_copy, cities):
            copy_of_tour = tour.copy()
            potential_solutions.append(copy_of_tour)
            # Perform 3 mutations and continue with while loop
            tour = mutate(mutate(mutate(tour)))
            
    # Finding the best solution in potential solutions
    for item in potential_solutions:
        if count_distance(item, cities) < count_distance(best_solution, cities):
            best_solution = item
            distance = count_distance(best_solution, cities)

    return best_solution, distance


def tsp_backtracking(names_file, distance_file):
    """
    This function uses a Backtracking Algorithm to give the best solution to the Traveling Salesman Problem. 
    A secondary function is used for the recursion. This function simply reads and formats the data, and calls the 
    recursion function.
    :param names_file: The *.txt file containing the city names in order.
    :param distance_file: The *.txt file containing the distances from one city to another, in order.
    :return: The list of city names with the shortest route.
    """
    # Globalizing and initializing variables
    global main_dictionary
    global dict_keys
    global best_tour

    # Loading in the dictionary and making a list of keys (city names)
    main_dictionary = txt_files_to_dict(names_file, distance_file)
    dict_keys = list(main_dictionary.keys())

    # Setting the best_tour equal to the trivial route
    best_tour = list(main_dictionary.keys())
    # Forcing the partial tour to start at the first city
    partial_tour = [dict_keys[0]]

    # Creating a list containing all cities other than the first city
    remaining_cities = []
    for city in dict_keys:
        if city not in partial_tour:
            remaining_cities.append(city)

    # Recursion Call
    tsp_recursion(partial_tour, remaining_cities)

    return best_tour


def tsp_recursion(partial_tour, remaining_cities):
    """
    Main Function
    This function performs the recursion for the Backtracking algorithm. The function prevents testing duplicate 
    routes by two ways. 
        1. Forcing the starting city to be the first city, and 
        2. ensures the last city has a greater index in the main dictionary than the second city.
    :param partial_tour: The partial tour list.
    :param remaining_cities: A list of cities that are not currently in the tour list.
    :return: Nothing
    """
    # Initializing and globalizing variables
    global best_tour
    possible_ordered_pairs = list()

    # If there are no more remaining cities
    if len(remaining_cities) == 0:
        if count_distance(partial_tour, main_dictionary) < count_distance(best_tour, main_dictionary):
            best_tour = partial_tour

    # Else, if there is only one city remaining
    elif len(partial_tour) == 1:
        # Creating the ordered pairs
        for city1 in main_dictionary.keys():
            for city2 in main_dictionary.keys():
                # This if block ensures there are no reverse pairs and the first city is not included
                if dict_keys.index(city1) < dict_keys.index(city2) and city1 != dict_keys[0]:
                    possible_ordered_pairs.append((city1, city2))

        # Looping over each ordered pair and adding the elements to a partial tour
        for ordered_pair in possible_ordered_pairs:
            # Creating copies so we do not change original values
            partial_tour_copy = partial_tour.copy()
            remaining_cities_copy = remaining_cities.copy()
            # Appending each part of the ordered pair to the partial_tour, in order
            partial_tour_copy.append(ordered_pair[0])
            partial_tour_copy.append(ordered_pair[1])
            # Removing those added cities from the remaining cities list
            remaining_cities_copy.remove(ordered_pair[0])
            remaining_cities_copy.remove(ordered_pair[1])

            tsp_recursion(partial_tour_copy, remaining_cities_copy)

    # else, there must be more than one city remaining
    else:
        for city in remaining_cities:
            # Creating copies so we do not change original values
            partial_tour_copy = partial_tour.copy()
            remaining_cities_copy = remaining_cities.copy()
            # Inserting cities to partial tour and removing them from the remaining cities list
            partial_tour_copy.insert(-1, city)
            remaining_cities_copy.remove(city)

            tsp_recursion(partial_tour_copy, remaining_cities_copy)


tour_greedy = tsp_greedy("thirty_cities_names.txt", "thirty_cities_dist.txt")
tour_mutate, dist_mutate = tsp_mutation('thirty_cities_names.txt', 'thirty_cities_dist.txt')
tour_backtrack = tsp_backtracking('seven_cities_names.txt', 'seven_cities_dist.txt')
print(f'Greedy Tour:\n {tour_greedy}\n'
      f'Greedy Dist: {count_distance(tour_greedy, txt_files_to_dict("thirty_cities_names.txt", "thirty_cities_dist.txt"))}\n'
      )
print(f'Mutation Tour:\n {tour_mutate}\n'
      f'Mutation Dist: {dist_mutate}\n'
      )
print(f'Backtracking Tour:\n {tour_backtrack}\n'
      f'Backtracking Dist: {count_distance(tour_backtrack, txt_files_to_dict("seven_cities_names.txt", "seven_cities_dist.txt"))}'
      )
