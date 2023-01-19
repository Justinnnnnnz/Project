"""A3. Tester for the function patients_with_missing_values
in treatment_functions.
"""

import unittest
import treatment_functions as tfs

ERROR_MESSAGE = "Expected {}, but returned {}"


class TestPatientsWithMissingValues(unittest.TestCase):
    """Tester for the function patients_with_missing_values in
    treatment_functions.
    """

    def test_empty(self):
        """Empty dictionary."""

        id_to_attributes = {}
        name = 'xyz'
        expected = []
        actual = tfs.patients_with_missing_values(id_to_attributes, name)

        msg = ERROR_MESSAGE.format(expected, actual)
        self.assertEqual(expected, actual, msg)

    def test_one_patient_no_missing(self):
        """One patient, with the value present."""

        id_to_attributes = {
            'Tom':  {'Pet': 'dog', 'Car': 'NA', 'Team': 'Leafs'}
        }
        name = 'Pet'
        expected = []
        actual = tfs.patients_with_missing_values(id_to_attributes, name)

        msg = ERROR_MESSAGE.format(expected, actual)
        self.assertEqual(expected, actual, msg)

    ### ADD YOUR TESTS HERE ###
    def test_one_patient_with_missing(self):
        """One patient, with the value NA present."""

        id_to_attributes = {
            'Tom':  {'Pet': 'NA', 'Car': 'NA', 'Team': 'Leafs'}
        }
        name = 'Pet'
        expected = ['Tom']
        actual = tfs.patients_with_missing_values(id_to_attributes, name)

        msg = ERROR_MESSAGE.format(expected, actual)
        self.assertEqual(expected, actual, msg) 
        
    def test_more_patient_with_one_missing(self):
        """More than One patient, with the one NA present."""

        id_to_attributes = {
            'Tom':  {'Pet': 'NA', 'Car': 'NA', 'Team': 'Leafs'},
            'Anya':  {'Pet': 'dog', 'Car': 'NA', 'Team': 'Leafs'},
            'Iris':  {'Pet': 'cat', 'Car': 'NA', 'Team': 'Leafs'},
        }
        name = 'Pet'
        expected = ['Tom']
        actual = tfs.patients_with_missing_values(id_to_attributes, name)

        msg = ERROR_MESSAGE.format(expected, actual)
        self.assertEqual(expected, actual, msg)    


    def test_more_patient_with_two_missing(self):
        """More than One patient, with the two NA present."""

        id_to_attributes = {
            'Tom':  {'Pet': 'NA', 'Car': 'NA', 'Team': 'Leafs'},
            'Anya':  {'Pet': 'dog', 'Car': 'NA', 'Team': 'Leafs'},
            'Iris':  {'Pet': 'NA', 'Car': 'NA', 'Team': 'Leafs'},
        }
        name = 'Pet'
        expected = ['Tom', 'Iris']
        actual = tfs.patients_with_missing_values(id_to_attributes, name)

        msg = ERROR_MESSAGE.format(expected, actual)
        self.assertEqual(expected, actual, msg)    
    
    def test_sim_by_three_patients(self):
        """ Test patietns by similariteis by three patients """
        id_to_attributes = {
            'Tom':  {'Pet': '???', 'Car': 'fly', 'Team': 'Leafs'},
            'Anya':  {'Pet': 'dog', 'Car': 'NA', 'Team': 'bule'},
            'Iris':  {'Pet': 'dog', 'Car': 'run', 'Team': 'Leafs'},
        }
        name_to_value = 'Car'
        expected = ['Anya']
        actual = tfs.patients_with_missing_values(id_to_attributes, name_to_value)
        msg = ERROR_MESSAGE.format(expected, actual)
        self.assertEqual(expected, actual, msg)   
        
    def test_similarities_by_more_patients(self):
        """Test patietns by similariteis by more than three patients """
        id_to_attributes = {
            'Tom':  {'Pet': '???', 'Car': 'fly', 'Team': 'NA'},
            'Anya':  {'Pet': 'dog', 'Car': 'NA', 'Team': 'NA'},
            'Iris':  {'Pet': 'dog', 'Car': 'run', 'Team': 'NA'},
            'Jack': {'Pet' : 'cat', 'Car': 'BENCHI', 'Team': 'No team'}
        }
        name = 'Team'
        expected = ['Tom', 'Anya', 'Iris']
        actual = tfs.patients_with_missing_values(id_to_attributes, name)
        msg = ERROR_MESSAGE.format(expected, actual)
        self.assertEqual(expected, actual, msg)       
        

    def test_treatment_plan_by_patients(self):
        """Test patietns by similariteis by more than three patients """
        id_to_attributes = {
            
    'tcga.5l.aat0':
    {'Age': '42', 'Gender': 'female', 'Tumor_Size': 't2',
     'Nearby_Cancer_Lymphnodes': 'n0', 'Cancer_Spread': 'm0',
     'Histological_Type': 'h_t_1', 'Lymph_Nodes': '0', 'Treatment': 'plan_1'},
    'tcga.aq.a54o':
    {'Age': '51', 'Gender': 'NA', 'Tumor_Size': 't2',
     'Nearby_Cancer_Lymphnodes': 'n0', 'Cancer_Spread': 'm0',
     'Histological_Type': 'h_t_2', 'Lymph_Nodes': '0', 'Treatment': 'plan_2'},
    'tcga.aq.a7u7':
    {'Age': '55', 'Gender': 'female', 'Tumor_Size': 't2',
     'Nearby_Cancer_Lymphnodes': 'n2a', 'Cancer_Spread': 'm0',
     'Histological_Type': 'h_t_1', 'Lymph_Nodes': '4', 'Treatment': 'plan_4'}

        }
        name = 'Gender'
                         
                         
        expected = ['tcga.aq.a54o']
        actual = tfs.patients_with_missing_values(id_to_attributes, name)

        msg = ERROR_MESSAGE.format(expected, actual)
        self.assertEqual(expected, actual, msg)       


if __name__ == '__main__':
    unittest.main(exit=False)
