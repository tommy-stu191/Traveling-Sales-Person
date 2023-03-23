def backtracking_testing(names_file, distance_file):

    tour_list = list()
    possible_ordered_pairs = list()
    main_dictionary = txt_files_to_dict("seven_cities_names.txt", "seven_cities_dist.txt")
    dict_keys = list(main_dictionary.keys())

    tour_list.append(dict_keys[0])

    for city1 in main_dictionary.keys():
        for city2 in main_dictionary.keys():
            if dict_keys.index(city1) < dict_keys.index(city2) and city1 != tour_list[0]:
                possible_ordered_pairs.append((city1, city2))

    for ordered_pair in possible_ordered_pairs:
        partial_tour = tour_list.copy()
        partial_tour.append(ordered_pair[0])
        partial_tour.append(ordered_pair[1])
        print(partial_tour)

    print(possible_ordered_pairs)


backtracking_testing("seven_cities_names.txt", "seven_cities_dist.txt")
