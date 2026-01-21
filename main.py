"""
This script reads in course and programme data from the CSV and YAML files. It extracts
the BE(Hons) programme data and merges it with course information.

Last updated: 21/01/26 by Emi Lipoth
"""
import pandas as pd
import yaml
import matplotlib.pyplot as plt
from plotnine import *
import numpy as np

# read in csv file
courses = pd.read_csv("FoED_Sustainability_Courses_Benchmark.csv", header=0)

# update column names
courses.columns = ["course_name", "course_num", "description", "grad_profile", "cap_2", "LO", "assessment", "points","o_2025","o_2024","o_2023"]

# create new column that combines course codes, e.g. "ENGGEN" + "121" = "ENGGEN121"
courses["course_code"] = courses["course_name"].str.strip() + courses["course_num"].str.strip()


def yes_no_to_bool(s):
    # converts "Yes" and "No" string inputs in specified columns to their Boolean equivalents.
    return (
        s.astype(str)
         .str.strip()
         .str.lower()
         .map({"yes": True, "no": False})
         .astype("boolean")
    )

cols = ["cap_2","o_2025","o_2024","o_2023"]
courses[cols] = courses[cols].apply(yes_no_to_bool)

# read YAML programme file
with open("programmes.yaml") as file:
    prog_yaml = yaml.safe_load(file)

# selects only BE(Hons) data from YAML file as this programme has an extra sub-item (specialisation)
be_hons = prog_yaml["programmes"]["BE(Hons)"]

rows = []
for spec_name, spec_data in be_hons["specialisations"].items():
    for course_code, meta_data in spec_data["courses"].items():
        rows.append({"programme":"BE(Hons)",
                     "specialisation": spec_name,
                     "course_code": course_code, **meta_data
                     })

be_yaml = pd.DataFrame(rows)

# merge the CSV course data and the BE(Hons) YAML data
be_merged_df = courses.merge(
    be_yaml,
    on="course_code",
    how="inner")

# validation - how do we deal with N/A or blank values in the table?
be_merged_df["cap_2"] = be_merged_df["cap_2"].fillna(False)

# example syntax for a query - list all required (core) courses in the Civil Engineering specialisation
#print(be_merged_df.query("specialisation == 'Civil Engineering' and type == 'required'"))


# Calculates the proportion of core and elective courses per specialisation that include Capability 2
percentage_wide = (
    be_merged_df
    .groupby(["specialisation", "type"])["cap_2"]
    .mean()
    .unstack("type")
    .fillna(0)
    .mul(100)
    .round(1)
)
print("Percentage of core and elective courses that include Cap 2 (%)\n", percentage_wide)

summary_wide = (
    be_merged_df
    .groupby(["specialisation", "type", "cap_2"])["course_code"]
    .nunique()  # count unique courses in case of duplicates
    .unstack(["type", "cap_2"], fill_value=0)
)
#print(summary_wide)


plot = (
        ggplot(be_merged_df, aes("specialisation", fill="cap_2"))
        + geom_bar()
        + facet_wrap("type", nrow=2)
        + theme(axis_text_x=element_text(rotation=45, ha="right"))
        + labs(title="Percentage of courses with Capability 2 across BE(Hons) specialisations",
               x="Specialisation",
               y="Number of courses",
               fill="Capability 2")
)
plot.show()


