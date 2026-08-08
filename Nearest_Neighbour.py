# Ask the user for a valid integer
def get_integer_input(message, minimum, maximum=None):
    while True:
        try:
            number = int(input(message))

            if number < minimum: 
                print("Please enter a number between", minimum, "and", maximum)
            else:
                return number

        except ValueError:
            print("Please enter a valid whole number.")

# Ask the user for a positive distance value
def get_distance_input(message):
    while True:
        try:
            distance = float(input(message)) # Attempts to convert the user input into float values

            if distance > 0: # Checks if distance provided is rgeater than 0
                return distance

            print("The distance must be greater than 0.")

        except ValueError:
            print("Please enter a valid number.")

# Collect unique city names
def get_city_names(number_of_cities):
    cities = []

    for city_number in range(1, number_of_cities + 1):
        while True:
            city_name = input("Enter the name of city " + str(city_number) + ": ").strip()

            if city_name == "":
                print("The city name cannot be empty.")
            elif city_name in cities:
                print("This city has already been entered.")
            else:
                cities.append(city_name)
                break

    return cities

# Create the distance matrix
def get_distance_matrix(cities):
    number_of_cities = len(cities)
    distances = []

    # Create a matrix containing zeros to store distance values later
    for row_number in range(number_of_cities):
        row = []

        # Creates the required number of rows and columns needed for the matrix
        for column_number in range(number_of_cities):
            row.append(0)

        distances.append(row)

    print("\nEnter the distance between each pair of cities.")

    # Only ask once for each pair because the distances are symmetric
    for first_city in range(number_of_cities):
        for second_city in range(first_city + 1, number_of_cities):
            message = "Distance from " + cities[first_city] + " to " + cities[second_city] + ": "

            distance = get_distance_input(message)

            # Makes the distances between the 2 cities equal because they are symmetric
            distances[first_city][second_city] = distance
            distances[second_city][first_city] = distance

    return distances

# Apply the Nearest Neighbour heuristic
def nearest_neighbour(distances, starting_city):
    number_of_cities = len(distances)

    # Creates a list to track visited cities 
    visited = [False] * number_of_cities
    # Records the route taken by the algorithm
    route = [starting_city]

    # Mark the starting city as visited
    visited[starting_city] = True
    current_city = starting_city
    total_distance = 0

    # Continue until every city has been visited
    while len(route) < number_of_cities:
        #nearest city and nearest distance is reset each time the program searches for a nearest city
        nearest_city = -1
        nearest_distance = 0

        # Search for the nearest unvisited city
        for next_city in range(number_of_cities):
            # Only searches the cities that have not been visited yet
            if not visited[next_city]:
                current_distance = distances[current_city][next_city]

                # Selects first unvisited city or replace it with a closer unvisited city
                if nearest_city == -1 or current_distance < nearest_distance:
                    nearest_city = next_city
                    nearest_distance = current_distance

        # Travel to the selected city
        route.append(nearest_city)
        visited[nearest_city] = True

        # Adds the distance travelled to the total amount
        total_distance += nearest_distance
        # Make the selected city the new current city
        current_city = nearest_city

    # Return to the starting city
    total_distance += distances[current_city][starting_city]
    route.append(starting_city)

    return route, total_distance

# Display the completed route
def display_result(cities, distances, route, total_distance):
    print("\nTravel steps:")

    for step in range(len(route) - 1):
        current_city = route[step]
        next_city = route[step + 1]
        travel_distance = distances[current_city][next_city]

        # Prints the route taken and the total distance travelled
        print(str(step + 1) + ".", cities[current_city], "->", cities[next_city], "=",travel_distance, "km")

    print("\nFinal route:")

    for position in range(len(route)):
        print(cities[route[position]], end="")

        if position < len(route) - 1:
            print(" -> ", end="")

    print("\nTotal distance:", total_distance, "km")


# Main program
def main():
    print("TSP Using the Nearest Neighbour Heuristic")
    print("-----------------------------------------")

    number_of_cities = get_integer_input(
        "Enter the number of cities: ",
        2, # Minimum of 2 cities
        10 # Limit the number of cities to 10
    )

    cities = get_city_names(number_of_cities)
    distances = get_distance_matrix(cities)

    print("\nAvailable starting cities:")

    for index in range(number_of_cities):
        print(str(index + 1) + ".", cities[index])

    starting_choice = get_integer_input("Select the starting city: ", 1, number_of_cities)

    # Convert the user's choice to an index value
    starting_city = starting_choice - 1

    route, total_distance = nearest_neighbour(
        distances,
        starting_city
    )

    display_result(
        cities,
        distances,
        route,
        total_distance
    )

# Runs main only when the file is executed directly
if __name__ == "__main__":
    main()
