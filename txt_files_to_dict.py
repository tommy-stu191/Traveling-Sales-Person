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


# test_case = txt_files_to_dict("seven_cities_names.txt", "seven_cities_dist.txt")
# print(test_case)

# test_case_large = txt_files_to_dict("thirty_cities_names.txt", "thirty_cities_dist.txt")
# print(test_case_large)
