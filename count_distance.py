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


example_city_dictionary = {'Alpha': [0.0, 27.0, 12.1, 17.7, 11.0, 29.2, 22.4], 'Beta': [27.0, 0.0, 16.8, 11.2, 29.2, 11.0, 31.8], 'Gamma': [12.1, 16.8, 0.0, 6.0, 12.5, 17.1, 27.9], 'Delta': [17.7, 11.2, 6.0, 0.0, 18.0, 11.7, 30.0], 'Epsilon': [11.0, 29.2, 12.5, 18.0, 0.0, 27.0, 33.2], 'Zeta': [29.2, 11.0, 17.1, 11.7, 27.0, 0.0, 40.2], 'Eta': [22.4, 31.8, 27.9, 30.0, 33.2, 40.2, 0.0]}
# Question: This is how i envisioned us storing and keeping track of our tour, with the following tour_list.
# I think this would make it easier to manipulate the tour in our algorithms. 
example_tour_list = ['Beta', 'Gamma', 'Delta', 'Epsilon', 'Zeta', 'Eta', 'Alpha']

print(count_distance(example_tour_list, example_city_dictionary))
