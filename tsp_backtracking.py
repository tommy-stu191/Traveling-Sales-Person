def tsp_backtracking(names_file, distance_file):
    """

    :param names_file:
    :param distance_file:
    :return:
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

    :param partial_tour:
    :param remaining_cities:
    :return:
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


a = tsp_backtracking("thirty_cities_names.txt", "thirty_cities_dist.txt")
d = txt_files_to_dict("thirty_cities_names.txt", "thirty_cities_dist.txt")
print(count_distance(a, d), a)
