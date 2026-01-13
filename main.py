"""

"""
import pandas as pd
import numpy as np

# read in csv file
courses = pd.read_csv("FoED_Sustainability_Courses_Benchmark.csv", header=0)

# update column names
courses.columns = ["course_code", "course_num", "description", "grad_profile", "cap_2", "LO", "assessment", "points","o_2025","o_2024","o_2023"]

# create new column that combines course codes, e.g. "ENGGEN" + "121" = "ENGGEN121"
courses["course"] = courses["course_code"].str.strip() + courses["course_num"].str.strip()


