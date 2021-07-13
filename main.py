import sys
import getopt
import os
import cities_co2_graph as transport_graph
import st_index as st_index
import pr_index as pr_index
import wr_index as wr_index
from PIL import Image
import prices as prices

from tabulate import tabulate

from pylab import *

from inspyred import benchmarks
from inspyred.ec import variators
from inspyred_utils import NumpyRandomWrapper
#from sustainability_problem import

import multi_objective

from functools import reduce

# Disable print
def blockPrint():
    sys.stdout = open(os.devnull, 'w')

# Restore print
def enablePrint():
    sys.stdout = sys.__stdout__

def main(argv):
    try:
        opts, args = getopt.getopt(argv, "d:f:", ["destination=", "transport_data_file="])
    except:
        raise SystemExit(f"Usage: {sys.argv[0]} <destination_country> <transport_data_file>")
  
    for opt, arg in opts:
        if opt in ['-d', '--destination']:
            DESTINATION_COUNTRY = arg
        elif opt in ['-f', '--transport_data_file']:
            TRANSPORT_DATA_FILE = arg

    blockPrint()
    #Create transport graph
    G, shortest_paths, co2_path_lengths, edge_attrs, countries = transport_graph.main(['-d', DESTINATION_COUNTRY, '-f', TRANSPORT_DATA_FILE])
    enablePrint()

    data_to_print = []

    #create an empty vector for a dictionary with countries as keys and sustainability indexes as values
    st_index_countries = {}
    wr_index_countries = {}
    pr_index_countries, final_table = pr_index.compute_production_sustainability_index()

    prices_countries = prices.get_prices()

    for c in countries:
        if c == DESTINATION_COUNTRY:
            st_index_countries[c] = 10.0
        else:
            st_index_countries[c] = st_index.compute_transport_sustainability_index(G, shortest_paths[c], edge_attrs)

        wr_index_countries[c] = wr_index.compute_workers_sustainability_index(c)

        data_to_print.append([c, pr_index_countries[c], wr_index_countries[c], st_index_countries[c], prices_countries[c]])

    print(tabulate(data_to_print, headers=["Country", "Production", "Workers", "Transport", "Cotton Price (€)"]))

    #print("°°°°°°°°°°°°°°°°°°°°°°°°°°°°°")
    #print("Corresponding csv file has been saved in the \'data\' directory.")
    with Image.open('data/final.png') as img:
        img.show()


if __name__ == "__main__":
    main(sys.argv[1:])