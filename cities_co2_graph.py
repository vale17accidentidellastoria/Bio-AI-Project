import networkx as nx
import matplotlib.pyplot as plt
import sys
import csv
import random
import getopt
import os
import shutil

random.seed()

EDGE_ATTRS = []

TRANSPORT_EDGELIST_FILE = "transport_co2.edgelist"

COUNTRIES = set() #initialize an empty set of countries

def create_edgelist_from_csv_transport_file(input_file):
    with open(input_file) as csv_file:
        transport_edgelist_file = open(TRANSPORT_EDGELIST_FILE, "w")        
        csv_reader = csv.reader(csv_file, delimiter=';')
        headers = True
        for row in csv_reader:
            if headers:
                for attr in row[2:]: #ignore the "origin country" and "destination country" columns
                    EDGE_ATTRS.append(attr)
                headers = False
            else:
                row_to_save = ""
                for i in range(0, len(row)):
                    if i <= 1:
                        row_to_save += (row[i] + " ")
                        COUNTRIES.add(row[i]) #add the country name to the set
                    else:
                        if EDGE_ATTRS[i-2] == "origin_city":
                            row_to_save += ("{'" + EDGE_ATTRS[i-2] + "\':\'" + row[i] + "\', ")
                        elif (EDGE_ATTRS[i-2] == "destination_city" 
                                or EDGE_ATTRS[i-2] == "transport_mode"):
                            row_to_save += ("\'" + EDGE_ATTRS[i-2] + "\':\'" + row[i] + "\', ")
                        elif (EDGE_ATTRS[i-2] == "freight" 
                                or EDGE_ATTRS[i-2] == "load_factor" 
                                or EDGE_ATTRS[i-2] == "distance_wtw"):
                            row_to_save += ("\'" + EDGE_ATTRS[i-2] + "\':" + row[i].replace(",", "") + ", ")
                        elif EDGE_ATTRS[i-2] == "co2_wtw":
                            row_to_save += ("\'" + EDGE_ATTRS[i-2] + "\':" + row[i] + "}\n")
                transport_edgelist_file.write(row_to_save)
        transport_edgelist_file.close()

def plot_graph(G, weight="weight", shortest_path=None):
    nx.draw_shell(G, with_labels=True, node_color='#00b4d9', node_size=2000)
    labels = nx.get_edge_attributes(G, weight)
    nx.draw_networkx_edge_labels(G, pos=nx.circular_layout(G), edge_labels=labels)
    filename = "transport_graph.png"

    if shortest_path is not None:
        pos = nx.circular_layout(G)
        # draw path in red
        path_edges = list(zip(shortest_path,shortest_path[1:]))
        nx.draw_networkx_nodes(G,pos,nodelist=shortest_path,node_color='#ff5733', node_size=2000)
        nx.draw_networkx_edges(G,pos,edgelist=path_edges,edge_color='#ff5733',width=3)
        if not os.path.exists("shortest_paths_images"):
            os.mkdir("shortest_paths_images")
        filename = f"shortest_paths_images/transport_shortest_path_{shortest_path[0]}.png"

    plt.axis('off')
    axis = plt.gca()
    axis.set_xlim([1.2*x for x in axis.get_xlim()])
    axis.set_ylim([1.2*y for y in axis.get_ylim()])
    plt.savefig(filename, dpi=300)
    plt.show()

#--------------------------------------------

def main(argv):

    destination_country = None
    data_file = None

    all_shortest_paths = {}
    all_shortest_paths_lengths = {}
  
    try:
        opts, args = getopt.getopt(argv, "d:f:", ["destination=", "data_file="])
    except:
        raise SystemExit(f"Usage: {sys.argv[0]} <destination_country> <data_file>")
  
    for opt, arg in opts:
        if opt in ['-d', '--destination']:
            destination_country = arg
        elif opt in ['-f', '--data_file']:
            data_file = arg

    try:
        create_edgelist_from_csv_transport_file(data_file) #creates a networkx edgelist starting from a data csv file
    except FileNotFoundError:
        raise SystemExit("The transport file about cities and co2 you selected does not exist!")

    try:
        G = nx.read_edgelist(TRANSPORT_EDGELIST_FILE) #generate a graph from the selected edgelist
    except TypeError:
        raise SystemExit("The list of edges has not a valid format")

    plot_graph(G, weight="co2_wtw")

    try:
        if os.path.exists("shortest_paths_images"):
            shutil.rmtree("shortest_paths_images")

        for origin_country in COUNTRIES:
            all_shortest_paths[origin_country] = nx.shortest_path(G, source=origin_country, target=destination_country, weight="co2_wtw")
            print("The shortest path from {} to {} is: {}".format(origin_country, destination_country, all_shortest_paths[origin_country]))

            for country, next_country in zip(all_shortest_paths[origin_country], all_shortest_paths[origin_country][1:]):
                print("{} - {}:".format(country, next_country))
                for attr in EDGE_ATTRS:
                    print("\t {}: {}".format(attr, G[country][next_country][attr]))

            all_shortest_paths_lengths[origin_country] = nx.shortest_path_length(G, source=origin_country, target=destination_country, weight="co2_wtw")
            print("The total amount of CO2 emissions of the travel is {} tonnes".format(all_shortest_paths_lengths[origin_country]))
            print("--------##################--------")

            plot_graph(G, weight="co2_wtw", shortest_path=all_shortest_paths[origin_country])
    
    except (nx.NetworkXNoPath, nx.NodeNotFound) as error:
        raise SystemExit("There is no path for the cities you selected. Try and check again the input cities")

    return G, all_shortest_paths, all_shortest_paths_lengths, EDGE_ATTRS, COUNTRIES


if __name__ == "__main__":   
    main(sys.argv[1:])