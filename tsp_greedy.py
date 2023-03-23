
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
    :return: A dictionary
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
            # Converting the key to a string rather than a string contained in a list
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

    :param tour_list: The list containing the order of cities traveled.
    :param cities_dictionary: The dictionary containing all cities and their distances to each other.
    :return: The sum of distance traveled.
    """
    total_distance = 0

    for city in tour_list:
        # Finding the index of the city so we do not have to work with the string
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
    Checks if the shortest_distance index is apart of a previously used city in a tour.
    
    :param cities: City/Distance dictionary
    :param tour: Current tour
    :param city_idx: index of potential next city in dictionary value list
    :return:
    """
    current_city = list(cities.items())[city_idx][0]
    if current_city in tour:
        return True
    return False


def tsp_greedy(name_file, distance_file):
    # Convert files to usable data
    # --> txt_files_to_dict()
    cities = txt_files_to_dict(name_file, distance_file)
    # Initializing tour with starting city
    tour = list()
    tour.append(list(cities.keys())[0])

    while len(tour) < len(cities):
        print(f'Tour contains: {tour}')
        shortest_path = 130000
        current_city = tour[-1]
        for distance in cities.get(current_city):

            # potential methods of determining if smallest dist found is not in tour list yet
            # A) Keep track of used index values >> pass over used idxs when
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


    # Determines the key/name of lowest distance to next city available
    # least_dist_idx = cities.get(current_city).index(shortest_path)
    # print(list(cities.items())[least_dist_idx][0])

    # If distance in tour list -> do none
    # if distance not in tour list -> add next city
    return tour


#tsp_greedy("seven_cities_names.txt", "seven_cities_dist.txt")

tour_complete = tsp_greedy("thirty_cities_names.txt", "thirty_cities_dist.txt")
print(f'Tour\n{tour_complete}\n'
      f'Total dist: {count_distance(tour_complete, txt_files_to_dict("thirty_cities_names.txt", "thirty_cities_dist.txt"))}'
      )


