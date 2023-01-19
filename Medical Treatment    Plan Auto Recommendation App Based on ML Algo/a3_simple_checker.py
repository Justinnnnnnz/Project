"""A simple checker for types of functions in treatment_functions.py."""

import io
import sys
from typing import Callable, Dict, List
sys.path.insert(0, 'pyta')
import python_ta
import treatment_functions as tf


##### Generic functions #####

def type_error_message(func_name: str, expected: str, got: str) -> str:
    """Return an error message for function func_name returning type got,
    where the correct return type is expected.
    """

    return ('{} should return a {}, but returned {}' +
            '.').format(func_name, expected, got)


def check_function(func: Callable, args: list, ret_type: type) -> None:
    """Check that func called with arguments args returns a value of type
    ret_type. Display the progress and the result of the check.
    """

    print('Checking {}...'.format(func.__name__))
    got = func(*args)
    assert isinstance(got, ret_type), \
        type_error_message(func.__name__, ret_type.__name__, type(got))
    print('  check complete')


def check_type_details(assertion: bool, func_name: str, expected: str,
                       got: str) -> None:
    """Check that assertion is True. Display the progress and the result
    of the check. Failure means that function func_name was expected
    to return expected, but returned a value whose str represenation
    is got.

    Useful when return type is, for example, a nested list or a
    complex dict.

    """

    print('Checking {}...'.format(func_name))
    assert assertion, type_error_message(func_name, expected, got)
    print('  check complete')


###############

print('=====================================================================')
print('=====================================================================')
print('=====================================================================')
print('==================== Start: checking coding style ===================')

python_ta.check_all('treatment_functions.py', config='pyta/a3_pyta.txt')

print('=================== End: checking coding style ====================\n')


print('== Start: checking whether initial values of constants are modified ==')

# Get the initial values of the constants
CONSTS_BEFORE = [
    tf.NA, tf.TREATMENT, tf.PATIENT_ID_INDEX, tf.NAME_TO_VALUE,
    tf.ID_TO_ATTRIBUTES, tf.VALUE_TO_IDS, tf.ID_TO_SIMILARITY]

print('Check whether the constants are unchanged from the starter code.')

assert CONSTS_BEFORE == ['NA', 'Treatment', 0, Dict[str, str],
                         Dict[str, Dict[str, str]], Dict[str, List[str]],
                         Dict[str, float]],\
    ('You have modified the value of some constant(s). Edit your code so that'
     + ' the values of constants are the same as in the starter code.')

print('  check complete')

print('== End: checking whether initial values of constants are modified ==\n')


print('============ Start: checking parameter and return types ============')

d = {
    'tcga.5l.aat0': {
        'Age': '42', 'Gender': 'female', 'Tumor_Size': 't2',
        'Nearby_Cancer_Lymphnodes': 'n0', 'Cancer_Spread': 'm0',
        'Histological_Type': '1', 'Lymph_Nodes': '0', 'Treatment': 'A'},
    'tcga.5l.aat1': {
        'Age': 'NA', 'Gender': 'female', 'Tumor_Size': 't2',
        'Nearby_Cancer_Lymphnodes': 'n0', 'Cancer_Spread': 'm1',
        'Histological_Type': '1', 'Lymph_Nodes': '0', 'Treatment': 'B'}
}
p = {'Age': '42', 'Gender': 'female', 'Tumor_Size': 't2',
     'Nearby_Cancer_Lymphnodes': 'n0', 'Cancer_Spread': 'm0',
     'Histological_Type': '1', 'Lymph_Nodes': '0', 'Treatment': 'A'}

########### read_patients_dataset
data = ('Patient_ID\tAge\tGender\tTumor_Size\tNearby_Cancer_Lymphnodes\t'
        'Cancer_Spread\tHistological_Type\tLymph_Nodes\tTreatment\n'
        'tcga.5l.aat0\t42\tfemale\tt2\tn0\tm0\t1\t0\tA\n'
        'tcga.5l.aat1\tNA\tfemale\tt2\tn0\tm1\t1\t0\tB')

data_io = io.StringIO(data)
actual = tf.read_patients_dataset(data_io)
check_type_details(
    isinstance(actual, dict) and 'tcga.5l.aat0' in actual and
    isinstance(actual['tcga.5l.aat0'], dict) and
    'Gender' in actual['tcga.5l.aat0'] and
    isinstance(actual['tcga.5l.aat0']['Gender'], str),
    'read_patients_dataset(a non-empty file)',
    'a non-empty Dict[str, Dict[str, str]]',
    actual)

########## build_value_to_ids
actual = tf.build_value_to_ids(d, 'Gender')
check_type_details(
    isinstance(actual, dict) and 'female' in actual and
    isinstance(actual['female'], list) and actual['female'] != [] and
    isinstance(actual['female'][0], str),
    'build_value_to_ids',
    'a non-empty Dict[str, List[str]] with a non-empty value',
    actual)

######### patients_with_missing_values
actual = tf.patients_with_missing_values(d, 'Age')
check_type_details(
    isinstance(actual, list) and actual != [] and isinstance(actual[0], str),
    'patients_with_missing_values',
    'a non-empty List[str]',
    actual)

######### similarity_score
check_function(tf.similarity_score, [d['tcga.5l.aat0'], p], float)

######### patient_similarities
actual = tf.patient_similarities(d, p)
check_type_details(
    isinstance(actual, dict) and 'tcga.5l.aat0' in actual and
    isinstance(actual['tcga.5l.aat0'], float),
    'patient_similarities',
    'a non-empty Dict[str, float]',
    actual)

######### patients_y_similarity
actual = tf.patients_by_similarity(d, p)
check_type_details(
    isinstance(actual, list) and actual != [] and isinstance(actual[0], str),
    'patients_by_similarity',
    'a non-empty List[str]',
    actual)

######## treatment_recommendations
actual = tf.treatment_recommendations(d, p)
check_type_details(
    isinstance(actual, list) and actual != [] and isinstance(actual[0], str),
    'treatment_recommendations',
    'a non-empty List[str]',
    actual)

######## recommend_treatments
check_function(tf.make_treatment_plans, [d, d], type(None))


print('============= End: checking parameter and return types =============\n')

print('======= Start: checking whether functions modify constants =======')

# Get the final values of the constants
CONSTS_AFTER = [
    tf.NA, tf.TREATMENT, tf.PATIENT_ID_INDEX, tf.NAME_TO_VALUE,
    tf.ID_TO_ATTRIBUTES, tf.VALUE_TO_IDS, tf.ID_TO_SIMILARITY]

# Check whether the constants are unchanged.
print('Checking whether functions modify constants...')
assert CONSTS_BEFORE == CONSTS_AFTER, \
    ('Your function(s) modified the value of some constant(s). Edit your' +
     '\ncode so that the values of constants are unchanged by your functions.')
print('  check complete')

print('=========== End: checking whether functions modify constants ====')
