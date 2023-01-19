"""Constants used by treatment_functions.py.
DO NOT MODIFY!
"""

from typing import List, Dict

# The "Not Available" indicator.
NA = 'NA'

# Name of the treatment attribute.
TREATMENT = 'Treatment'

# The index of the patient identifier in the dataset.
PATIENT_ID_INDEX = 0

# Dict key is name of an attribute. Corresponding dict value is value
# of an attribute.
# E.g., {'Gender': 'female', 'Age': '58'}
NAME_TO_VALUE = Dict[str, str]

# Dict key is patient ID. Corresponding dict value is a dictionary in which
# key is attribute name and value is attribute value.
# E.g., {'tcga.5l.aat0': {'Gender': 'female', 'Age': '42'},
#        'tcga.ew.a6sa': {'Gender': 'male', 'Age': 59}}
ID_TO_ATTRIBUTES = Dict[str, NAME_TO_VALUE]

# Dict key is attribute value. Corresponding dict value is a list of
# patient IDs.
# E.g., for the attribute name 'Gender' the dict could be:
#      {'female': ['tcga.5l.aat0', 'tcga.5l.aat1', 'tcga.a1.a0sp'],
#       'male': ['tcga.ew.a6sa']}
VALUE_TO_IDS = Dict[str, List[str]]

# Dict key is patient ID. Corresponding dict value is similarity measure.
# E.g., for the patient 'tcga.5l.aat0' the dict could be:
#      {'tcga.5l.aat1': 1.5, 'tcga.ew.a6sa' : 0.75}
ID_TO_SIMILARITY = Dict[str, float]


# Constants to help test code - use in docstring examples
THREE_PATIENTS = {
    'tcga.5l.aat0':
    {'Age': '42', 'Gender': 'female', 'Tumor_Size': 't2',
     'Nearby_Cancer_Lymphnodes': 'n0', 'Cancer_Spread': 'm0',
     'Histological_Type': 'h_t_1', 'Lymph_Nodes': '0', 'Treatment': 'plan_1'},
    'tcga.aq.a54o':
    {'Age': '51', 'Gender': 'male', 'Tumor_Size': 't2',
     'Nearby_Cancer_Lymphnodes': 'n0', 'Cancer_Spread': 'm0',
     'Histological_Type': 'h_t_2', 'Lymph_Nodes': '0', 'Treatment': 'plan_2'},
    'tcga.aq.a7u7':
    {'Age': '55', 'Gender': 'female', 'Tumor_Size': 't2',
     'Nearby_Cancer_Lymphnodes': 'n2a', 'Cancer_Spread': 'm0',
     'Histological_Type': 'h_t_1', 'Lymph_Nodes': '4', 'Treatment': 'plan_4'}
}

PATIENTS_WITH_NA = {
    'tcga.5l.aat0':
    {'Age': '42', 'Gender': 'female', 'Tumor_Size': 't2',
     'Nearby_Cancer_Lymphnodes': 'n0', 'Cancer_Spread': 'm0',
     'Histological_Type': 'NA', 'Lymph_Nodes': '0', 'Treatment': 'plan_1'},
    'tcga.aq.a54o':
    {'Age': '51', 'Gender': 'male', 'Tumor_Size': 't2',
     'Nearby_Cancer_Lymphnodes': 'n0', 'Cancer_Spread': 'm0',
     'Histological_Type': 'h_t_2', 'Lymph_Nodes': '0', 'Treatment': 'plan_2'},
    'tcga.aq.a7u7':
    {'Age': '55', 'Gender': 'female', 'Tumor_Size': 't2',
     'Nearby_Cancer_Lymphnodes': 'n2a', 'Cancer_Spread': 'm0',
     'Histological_Type': 'h_t_1', 'Lymph_Nodes': 'NA', 'Treatment': 'NA'}
}

NEW_PATIENT_INFO = {'Age': '50', 'Gender': 'female', 'Tumor_Size': 't2',
                    'Nearby_Cancer_Lymphnodes': 'n0', 'Cancer_Spread': 'm0',
                    'Histological_Type': 'h_t_1', 'Lymph_Nodes': '5',
                    'Treatment': 'NA'}

NEW_PATIENTS = {
    'tcga.uu.a93s':
    {'Age': '63', 'Gender': 'female', 'Tumor_Size': 't4d',
     'Nearby_Cancer_Lymphnodes': 'n3b', 'Cancer_Spread': 'm1',
     'Histological_Type': 'h_t_2', 'Lymph_Nodes': 'NA', 'Treatment': 'NA'},
    'tcga.v7.a7hq':
    {'Age': '75', 'Gender': 'female', 'Tumor_Size': 't1c',
     'Nearby_Cancer_Lymphnodes': 'n2a', 'Cancer_Spread': 'm0',
     'Histological_Type': 'h_t_2', 'Lymph_Nodes': '5', 'Treatment': 'NA'},
    'tcga.xx.a899':
    {'Age': '46', 'Gender': 'female', 'Tumor_Size': 't1c',
     'Nearby_Cancer_Lymphnodes': 'n2a', 'Cancer_Spread': 'mx',
     'Histological_Type': 'h_t_1', 'Lymph_Nodes': '5', 'Treatment': 'NA'},
}

NEW_PATIENTS_RECOMMENDATIONS = {
    'tcga.uu.a93s':
    {'Age': '63', 'Gender': 'female', 'Tumor_Size': 't4d',
     'Nearby_Cancer_Lymphnodes': 'n3b', 'Cancer_Spread': 'm1',
     'Histological_Type': 'h_t_2', 'Lymph_Nodes': 'NA', 'Treatment': 'plan_4'},
    'tcga.v7.a7hq':
    {'Age': '75', 'Gender': 'female', 'Tumor_Size': 't1c',
     'Nearby_Cancer_Lymphnodes': 'n2a', 'Cancer_Spread': 'm0',
     'Histological_Type': 'h_t_2', 'Lymph_Nodes': '5', 'Treatment': 'plan_4'},
    'tcga.xx.a899':
    {'Age': '46', 'Gender': 'female', 'Tumor_Size': 't1c',
     'Nearby_Cancer_Lymphnodes': 'n2a', 'Cancer_Spread': 'mx',
     'Histological_Type': 'h_t_1', 'Lymph_Nodes': '5', 'Treatment': 'plan_4'},
}
