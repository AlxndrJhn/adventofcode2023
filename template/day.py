from collections import defaultdict
import re

this_folder = "\\".join(__file__.split("\\")[:-1])
input_data = open(f"{this_folder}/input2.txt", "r").read().split("\n")
