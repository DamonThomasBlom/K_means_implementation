import array
import math
import csv
import numpy as np
import random
import matplotlib.pyplot as plt
import matplotlib.ticker as tck


def display_statistics(clusters):
    # We take in a parameter of a list of all the clusters and display the statistics of each cluster
    x = 0  # x will just be our iterable so we know which cluster we are on

    # We loop over each cluster individually and calculate the stats separately
    # and display them
    for cluster in clusters:
        cluster_length = len(cluster)
        cluster_birthrate_total = 0
        cluster_life_expectancy = 0
        country_names = ""
        x += 1

        for country in cluster:
            cluster_birthrate_total += country[0]
            cluster_life_expectancy += country[1]
            country_names += country[2] + "\n"

        cluster_avg_birthrate = cluster_birthrate_total / cluster_length
        cluster_avg_life_expectancy = cluster_life_expectancy / cluster_length
        print(f'''Cluster {x} stats: 
Number of countries in this cluster: {cluster_length}       
Cluster {x} average birthrate: {round(cluster_avg_birthrate, 2)}
Cluster {x} average life expectancy: {round(cluster_avg_life_expectancy, 2)}
Country names:  
{country_names}''')


# This method will calculate the mean of x and y value of each cluster
def calculate_mean_clusters(list_clusters):
    clusters_average_points = []

    # We loop through each cluster and calculate the average of the x and y values
    # and append that the the empty array these will be our new centroids for the next
    # iteration of the K means algorithm
    for cluster in list_clusters:
        x_value_list = return_column_values(cluster, 0)
        y_value_list = return_column_values(cluster, 1)

        x_average = sum(x_value_list) / len(x_value_list)
        y_average = sum(y_value_list) / len(y_value_list)
        clusters_average_points.append([x_average, y_average])

    return clusters_average_points


# Since I was having problems with numpy array I made this function to create a list
# of all the values from a specific column in a matrix
def return_column_values(matrix, column_index):
    return_list = []
    for i in matrix:
        return_list.append(i[column_index])
    return return_list


# This method calculates the distance between two points
def calculate_distance(point1, point2):
    distance = math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)
    return distance


# Function will take in the file name as the input and return a matrix with all the data
def readFile(_file_name):
    # Start off with 3 lists that we will store everything in before we combine them
    country_name = []
    birth_rate = []
    life_expectancy = []
    with open(_file_name, 'r') as file:
        file_reader = csv.reader(file, delimiter=',')
        line_count = 0
        for row in file_reader:
            if line_count == 0:
                print(f'Column names are {", ".join(row)}')
                line_count += 1
            else:
                country_name.append(row[0])
                birth_rate.append(float(row[1]))
                life_expectancy.append(float(row[2]))
                line_count += 1
            print(f'Processed {line_count} lines.')

    # Once all the data has been read we create another list that will contain the combined data
    combined_data = []
    for i in range(len(birth_rate)):
        combined_data.append([birth_rate[i], life_expectancy[i], country_name[i]])

    return combined_data


# This method is doing the bulk of the work by calculating all the distances and creating all the lists
# of clusters
def k_means(input_data, number_of_clusters, input_centroids):
    # We check if we got in any average centroids if not we generate the samples
    if not input_centroids:
        centroids = random.sample(data, number_of_clusters)
    else:
        centroids = input_centroids

    # We loop over the number of clusters we get and append an empty list for every cluster we have
    clusters = []
    for _ in range(number_of_clusters):
        clusters.append([])

    # We loop through all our input data to calculate the distance between every point and every cluster
    for x in input_data:
        x_value = x[0]
        y_value = x[1]
        # We create an empty list every iteration which stores the distances that we calculate
        distances = []

        # For every point we have to calculate
        for y in centroids:
            distance = calculate_distance([x_value, y_value], y)
            distances.append(distance)

        # This returns the index of the smallest distance and we assign this data point to that clusters index
        index_min = np.argmin(distances)
        # When we got the index we append this data point to the corresponding cluster
        clusters[index_min].append(x)

    # Once we have assigned all the points the right clusters we can start displaying the
    # results and calculating the mean centroid of every cluster which we will return from
    # this function
    display_statistics(clusters)
    plot_clusters(clusters, centroids)
    new_centroids = calculate_mean_clusters(clusters)
    return new_centroids


# This method will handle the iteration part of the algorithm
def k_means_algorithm(input_data, _number_of_iterations, number_of_clusters):
    results = []

    for i in range(_number_of_iterations):
        # The first iteration will not have any input centroids so we feed in a empty list
        # because my k_means method will generate or the right amount of centroids the first time
        # Then it will return the average of each cluster and we then feed that into the next iteration
        if i == 0:
            results = k_means(input_data, number_of_clusters, [])
        else:
            results = k_means(input_data, number_of_clusters, results)


# This method is pretty straight forward it will handle plotting all the clusters
def plot_clusters(input_data, centroids):
    # For now we will only store 6 colours which we could always expand on later
    colours = ['b', 'r', 'g', 'c', 'm', 'y', 'orange', 'lime', 'purple', 'gold']
    # i will be our iterable which we will need later
    i = 0
    for cluster in input_data:
        centroid = centroids[i]
        x_values = return_column_values(cluster, 0)
        y_values = return_column_values(cluster, 1)
        colour = colours[i]
        plt.scatter(x_values, y_values, c=colour)
        # We will just display every centroid as a large black X
        plt.scatter(centroid[0], centroid[1], c='k', marker='x', s=200)
        plt.xlabel("Birth rate (per 1000)")
        plt.ylabel("Life expectancy")
        i += 1

    plt.show()


# ============= Main application ===============
file_choice = int(input('''Enter in the number of which file you would like to read
1) data1953
2) data2008
3) dataBoth
Choice: '''))
number_of_cluster = int(input("Enter in the number of clusters you would like to see: "))
number_of_iterations = int(input("Enter in the number of iterations you would like the algorithm to perform: "))
file_name = ""
if file_choice == 1:
    file_name = "data1953.csv"
elif file_choice == 2:
    file_name = "data2008.csv"
elif file_choice == 3:
    file_name = "dataBoth.csv"

data = readFile(file_name)
k_means_algorithm(data, number_of_iterations, number_of_cluster)
