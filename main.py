import sys
import getopt
import os
import cities_co2_graph as transport_graph
import st_index as st_index
import pr_index as pr_index
from PIL import Image
import prices as prices


from pylab import *

from inspyred import benchmarks
from inspyred.ec import variators
from inspyred_utils import NumpyRandomWrapper
#from sustainability_problem import

import multi_objective

from functools import reduce
import wr_index as wr_index

# Disable
def blockPrint():
    sys.stdout = open(os.devnull, 'w')

# Restore
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

    #blockPrint()
    #Create transport graph
    G, shortest_paths, co2_path_lengths, edge_attrs, countries = transport_graph.main(['-d', DESTINATION_COUNTRY, '-f', TRANSPORT_DATA_FILE])
    #enablePrint()

    print("°°°°°°°°°°°°°°°°°°°°°°°°°°°°°")
    print("The sustainability indexes for transport are:")

    #create an empty vector for a dictionary with countries as keys and sustainability indexes as values
    st_index_countries = {}
    wr_index_countries = {}

    for c in countries:
        if c == DESTINATION_COUNTRY:
            st_index_countries[c] = 10.0
            wr_index_countries[c] = wr_index.compute_workers_sustainability_index(c)
        else:
            st_index_countries[c] = st_index.compute_transport_sustainability_index(G, shortest_paths[c], edge_attrs)
            wr_index_countries[c] = wr_index.compute_workers_sustainability_index(c)
        print("\t {} = {}".format(c, st_index_countries[c]))
        print("workers index: ", c, wr_index_countries[c])

    pr_index_countries, final_table = pr_index.compute_production_sustainability_index()

    print("°°°°°°°°°°°°°°°°°°°°°°°°°°°°°")
    print("The sustainability indexes for production are:")
    for c in pr_index_countries.keys():
        print("\t {} = {}".format(c, pr_index_countries[c]))
    print("°°°°°°°°°°°°°°°°°°°°°°°°°°°°°")
    print("Corresponding csv file has been saved in the \'data\' directory.")
    with Image.open('data/final.png') as img:
        img.show()


    prices_countries = prices.get_prices()

    print("°°°°°°°°°°°°°°°°°°°°°°°°°°°°°")
    print("Average cotton prices per country are:")
    for c in prices_countries.keys():
        print("\t {} = {}{}".format(c, prices_countries[c], "€"))


if __name__ == "__main__":
    main(sys.argv[1:])