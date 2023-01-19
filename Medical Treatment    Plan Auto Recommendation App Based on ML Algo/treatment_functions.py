"""Assignment 3 - Medical Treatment Planning
"""
import copy

from typing import Dict, List, TextIO
from constants import (NA, TREATMENT, PATIENT_ID_INDEX, NAME_TO_VALUE,
                       ID_TO_ATTRIBUTES, VALUE_TO_IDS, ID_TO_SIMILARITY)
from constants import (THREE_PATIENTS, PATIENTS_WITH_NA, NEW_PATIENT_INFO,
                       NEW_PATIENTS, NEW_PATIENTS_RECOMMENDATIONS)



def read_patients_dataset(patients_file: TextIO) -> ID_TO_ATTRIBUTES:
    """Return an ID_TO_ATTRIBUTES dictionary that contains all
    information from patients_file.

    Preconditions: patients_file is a TSV file,
                   patients_file is open for reading.

    >>> patients_file = open("medical_data_three.tsv")
    >>> id_to_attributes = read_patients_dataset(patients_file)
    >>> patients_file.close()
    >>> id_to_attributes == THREE_PATIENTS
    True
    
    >>> patients_data = open("medical_data.tsv")
    >>> atributes = read_patients_dataset(patients_data)
    >>> patients_data.close()
    """
    id_to_attributes = {}
    
    names = patients_file.readline().strip('\n').split('\t')
    
    for line in patients_file:
        name_to_value = {}
        values = line.strip('\n').split('\t')
        
        for i in range(1, len(values)):
            name_to_value[names[i]] = values[i]
            
        id_to_attributes[values[0]] = name_to_value
    
    
    return id_to_attributes
        
        


def build_value_to_ids(id_to_attributes: ID_TO_ATTRIBUTES,
                       name: str) -> VALUE_TO_IDS:
    """Return a VALUE_TO_IDS dictionary, in which the keys are all
    possible values of an attribute with name name that appear in
    id_to_attributes, and the values are lists of all patient IDs that
    have that value for this attribute name.

    Precondition: name is a name of an attribute that appears in
                  id_to_attributes.

    >>> value_to_ids = build_value_to_ids(THREE_PATIENTS, 'Gender')
    >>> expected = {'male': ['tcga.aq.a54o'],
    ...             'female': ['tcga.5l.aat0', 'tcga.aq.a7u7']}
    >>> same_key_to_list_dicts(expected, value_to_ids)
    True
    
    """
    
    values_to_ids = {}
    
    for p_id in id_to_attributes:
        
        value = id_to_attributes[p_id][name]
        
        if value in values_to_ids:
            
            values_to_ids[value].append(p_id)
            
        else:
            values_to_ids[value] = [p_id]
    
    return values_to_ids
    



def patients_with_missing_values(id_to_attributes: ID_TO_ATTRIBUTES,
                                 name: str) -> List[str]:
    """Return a list of patient IDs of all patients who have the value NA 
    (not available) for the given attribute name.
    
    >>> patients_with_missing_values(PATIENTS_WITH_NA, 'Lymph_Nodes')
    ['tcga.aq.a7u7']
    
    >>> value = open("medical_data_small.tsv")
    >>> attributes = read_patients_dataset(value)
    >>> patients_with_missing_values(attributes, 'Lymph_Nodes')
    ['tcga.c8.a27a', 'tcga.c8.a12m', 'tcga.c8.a1he', 'tcga.ac.a23h', 'tcga.a8.a099', 'tcga.b6.a0ws']
    >>> value.close()
    """

    ids = []
    
    for p_id in id_to_attributes:
        
        if id_to_attributes[p_id][name] == NA:
            ids.append(p_id)
            
    return ids



def similarity_score(name_to_value_1: NAME_TO_VALUE,
                     name_to_value_2: NAME_TO_VALUE) -> float:
    """Return the total similarity score, rounded to 2 places after the
    decimal point, for the two patients with data name_to_value_1 and
    name_to_value_2, respectively. Ignore attribute TREATMENT in the
    calculation.

    >>> p1 = THREE_PATIENTS['tcga.5l.aat0']
    >>> p2 = THREE_PATIENTS['tcga.aq.a54o']
    >>> abs(similarity_score(p1, p2) - 4.1) < 0.01
    True
    
    >>> p1 = PATIENTS_WITH_NA['tcga.5l.aat0']
    >>> p2 = PATIENTS_WITH_NA['tcga.aq.a7u7']
    >>> abs(similarity_score(p1, p2) - 4.07) < 0.01
    True
    """    
    score = 0.0
    
    for name in name_to_value_1:
        value_1 = name_to_value_1[name]
        value_2 = name_to_value_2[name]
        
        if name != TREATMENT:  
            
            if value_1 == NA or value_2 == NA:
                score += 0.5
            elif value_1.isdigit():
                score += 1 / (abs(int(value_1) - int(value_2)) + 1)
            elif value_1 == value_2:
                score += 1.0
    
    
    return round(score, 2)


def patient_similarities(id_to_attributes: ID_TO_ATTRIBUTES,
                         name_to_value: NAME_TO_VALUE) -> ID_TO_SIMILARITY:
    """Return a value that is a ID_TO_SIMILARITY that maps each patient ID from
    the input ID_TO_ATTRIBUTES to the computed similarity measure between that 
    patient and the patient with data from the given NAME_TO_VALUE.

    >>> patient_similarities(THREE_PATIENTS,NEW_PATIENT_INFO)
    {'tcga.5l.aat0': 5.28, 'tcga.aq.a54o': 3.67, 'tcga.aq.a7u7': 4.67}
    """

    id_to_similarity = {}
    
    for p_id in id_to_attributes:
        
        
        id_to_similarity[p_id] = similarity_score(id_to_attributes[p_id],
                                                  name_to_value)
        
    return id_to_similarity


def patients_by_similarity(id_to_attributes: ID_TO_ATTRIBUTES,
                           name_to_value: NAME_TO_VALUE) -> List[str]:
    """Return a list of all patient IDs from the given ID_TO_ATTRIBUTES,
    sorted according to the these patients' similarities with the patient data 
    in the given NAME_TO_VALUE. The output list should be sorted in descending 
    order by similarity score. In the case of a tie, the patient IDs are sorted
    in alphabetical order.
    
    >>> patients_by_similarity(THREE_PATIENTS,NEW_PATIENT_INFO)
    ['tcga.5l.aat0', 'tcga.aq.a7u7', 'tcga.aq.a54o']
    """

    result = []
    
    id_to_similarity = patient_similarities(id_to_attributes, name_to_value)
    
    ids = list(id_to_similarity.keys())
    scores = list(id_to_similarity.values())
    while ids != []:
        max_score = max(scores)
        num_of_max_score = scores.count(max_score)
    
        if num_of_max_score > 1:
            temp = []
            a = 0
            while a < (num_of_max_score):                
                max_id = ids[scores.index(max(scores))]
                
                temp.append(max_id)
                ids.remove(max_id)
                scores.remove(max_score)
                a += 1
                
            temp.sort()
            result += temp 
            
        else:
            max_id = ids[scores.index(max_score)]
            
            result.append(max_id)
            
            ids.remove(max_id)
            scores.remove(max_score)
        
    return result


def treatment_recommendations(id_to_attributes: ID_TO_ATTRIBUTES,
                              name_to_value: NAME_TO_VALUE) -> List[str]:
    """Return a list of unique values for the attribute named TREATMENT, in the
    following order. 
    
    >>> treatment_recommendations(THREE_PATIENTS,NEW_PATIENT_INFO)
    ['plan_1', 'plan_4', 'plan_2']
    
    """
    
    
    treatments = []
    
    p_ids = patients_by_similarity(id_to_attributes, name_to_value)
    
    for p_id in p_ids:
        treatment = id_to_attributes[p_id][TREATMENT]
        if treatment != NA:
            if treatment not in treatments:
                treatments.append(treatment)
                
    return treatments


def make_treatment_plans(id_to_attributes: ID_TO_ATTRIBUTES,
                         new_id_to_attributes: ID_TO_ATTRIBUTES) -> None:
    """Modify new_id_to_attributes by replacing the values of the
    TREATMENT attribute with the first recommended treatment for each patient,
    according to the existing patient data in id_to_attributes.

    >>> new_id_to_attributes = copy.deepcopy(NEW_PATIENTS) 
    >>> make_treatment_plans(THREE_PATIENTS, new_id_to_attributes)
    >>> new_id_to_attributes == NEW_PATIENTS_RECOMMENDATIONS
    True
    
    >>> make_treatment_plans(THREE_PATIENTS,NEW_PATIENTS)
    >>> NEW_PATIENTS
    {'tcga.uu.a93s': {'Age': '63', 'Gender': 'female', 'Tumor_Size': 't4d', 'Nearby_Cancer_Lymphnodes': 'n3b', 'Cancer_Spread': 'm1', 'Histological_Type': 'h_t_2', 'Lymph_Nodes': 'NA', 'Treatment': 'plan_4'}, 'tcga.v7.a7hq': {'Age': '75', 'Gender': 'female', 'Tumor_Size': 't1c', 'Nearby_Cancer_Lymphnodes': 'n2a', 'Cancer_Spread': 'm0', 'Histological_Type': 'h_t_2', 'Lymph_Nodes': '5', 'Treatment': 'plan_4'}, 'tcga.xx.a899': {'Age': '46', 'Gender': 'female', 'Tumor_Size': 't1c', 'Nearby_Cancer_Lymphnodes': 'n2a', 'Cancer_Spread': 'mx', 'Histological_Type': 'h_t_1', 'Lymph_Nodes': '5', 'Treatment': 'plan_4'}}
    """

    
    for p_id in new_id_to_attributes:
        
        name_to_value = new_id_to_attributes[p_id]
        
        treatments = treatment_recommendations(id_to_attributes, name_to_value)
        
        new_id_to_attributes[p_id][TREATMENT] = treatments[0]
        
        
        

# Provided helper functions - can be used to test two objects for `sameness'.

def same_key_to_list_dicts(key_to_list1: Dict[str, List[str]],
                           key_to_list2: Dict[str, List[str]]) -> bool:
    """Return True if and only if key_to_list1 and key_to_list2 are equal
    dictionaries, regardless of the order in which elements occur in the
    dictionaries' values.

    >>> same_key_to_list_dicts({'a': [], 'b': ['x'], 'c': ['x', 'y', 'z']},
    ...                        {'a': [], 'b': ['x'], 'c': ['y', 'z', 'x']})
    True
    >>> same_key_to_list_dicts({'a': [], 'b': ['x'], 'c': ['x', 'y', 'z']},
    ...                        {'a': [], 'b': ['x'], 'c': ['y', 'z', 'w']})
    False
    >>> same_key_to_list_dicts({'a': [], 'b': ['x'], 'd': ['x', 'y', 'z']},
    ...                        {'a': [], 'b': ['x'], 'c': ['y', 'z', 'x']})
    False
    """

    if key_to_list1.keys() != key_to_list2.keys():
        return False

    for key in key_to_list1:
        if not same_lists(key_to_list1[key], key_to_list2[key]):
            return False

    return True


def same_lists(list1: list, list2: list) -> bool:
    """Return True if and only if list1 and list2 are equal lists, regardless
    of the order in which elements occur.

    >>> same_lists(['x', 'y', 'z'], ['y', 'z', 'x'])
    True
    >>> same_lists(['x', 'y', 'k'], ['y', 'z', 'x'])
    False
    """

    return sorted(list1) == sorted(list2)


if __name__ == "__main__":
    import doctest
    doctest.testmod()

    medical_data_file = 'medical_data.tsv'
    patients_data_file = open(medical_data_file)
    patient_id_to_attributes = read_patients_dataset(patients_data_file)
    patients_data_file.close()

    medical_data_file = 'new_patients.tsv'
    new_patients_data_file = open(medical_data_file)
    new_patient_id_to_attributes = read_patients_dataset(
        new_patients_data_file)
    new_patients_data_file.close()

    make_treatment_plans(patient_id_to_attributes,
                         new_patient_id_to_attributes)

    for new_patient_id in new_patient_id_to_attributes:
        recommend_str = (
            'The recommended treatment for patient {} is {}.'.format(
                new_patient_id,
                new_patient_id_to_attributes[new_patient_id][TREATMENT]))
        # Uncomment the line below to view the treatment plans but
        # re-comment out before submitting solution.
        print(recommend_str)
