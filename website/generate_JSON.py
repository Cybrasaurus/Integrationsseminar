#TODO if ever update this also update the github, local under C:\Users\asasc\Documents\Python Scripts\DHBW\Integrationsseminar\commit_JSON_GEN
"""
The MIT License (MIT)

Copyright (c) <2023> Cybrasaurus

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""

# JSON Generator Module
import logging
import json

logging.basicConfig(level=logging.INFO)
# create and init faker generator
    # localized faker gen for Germany
    # --see docs: https://faker.readthedocs.io/en/master/#localization
    # -- docs for different localizations: https://faker.readthedocs.io/en/master/locales.html
from faker import Faker
    # localized provider for Germany: https://faker.readthedocs.io/en/master/locales/de_DE.html
fake = Faker("de_DE")


def generate_name_data(first_name=None, last_name=None, full_name=None, prefix=None, suffix=None,
                       gender_distribution=0.5, prefix_distribution=0.2, suffix_distribution=0.2):
    """

    :param first_name: Whether to generate a first name for the return dictionary
    :param last_name: Whether to generate a last name for the return dictionary
    :param full_name: Whether to generate a full name for the return dictionary, this automatically sets first_name and last_name to TRUE
    :param prefix: Whether to generate a prefix. Defaults to "Herr" or "Frau", gender dependant
    :param suffix: Whether to generate a suffix
    :param gender_distribution: Percentage chance for male or female names. Parameter represents chance for male
    :param prefix_distribution: Percentage chance for a prefix other than "Herr" or "Frau"
    :param suffix_distribution: Percentage chance for a suffix
    :return: return_dict: A dictionary containing all data of the person
    """
    import random
    assert first_name is None or first_name is True, f"Invalid parameter '{first_name}' for parameter first_name, valid options are: [None, True]"
    assert last_name is None or last_name is True, f"Invalid parameter '{last_name}' for parameter last_name, valid options are: [None, True]"
    assert full_name is None or full_name is True, f"Invalid parameter '{full_name}' for parameter full_name, valid options are: [None, True]"
    assert prefix is None or prefix is True, f"Invalid parameter '{prefix}' for parameter prefix, valid options are: [None, True]"
    assert suffix is None or suffix is True, f"Invalid parameter '{suffix}' for parameter suffix, valid options are: [None, True]"
    assert type(
        gender_distribution) == float, f"Invalid parameter '{gender_distribution}' for parameter suffix, valid options are: floats"
    assert type(
        prefix_distribution) == float, f"Invalid parameter '{prefix_distribution}' for parameter suffix, valid options are: floats"
    assert type(
        suffix_distribution) == float, f"Invalid parameter '{suffix_distribution}' for parameter suffix, valid options are: floats"

    return_dict = {
    }
    # decide whether to generate a male or a female, x<=0.5 is male, x>=0.5 is female
    gender = random.random()
    if gender <= gender_distribution:
        gender = "Male"
    else:
        gender = "Female"

    if full_name is True:
        first_name = True
        last_name = True

    if first_name is True:
        if gender == "Male":
            return_dict["Vorname"] = fake.first_name_male()
        else:
            return_dict["Vorname"] = fake.first_name_female()

    if last_name is True:
        return_dict["Nachname"] = fake.last_name()

    if full_name is True:
        return_dict["Name"] = f"{return_dict['Vorname']} {return_dict['Nachname']}"

    if prefix is True:
        if random.random() <= prefix_distribution:
            return_dict["Anrede"] = fake.prefix_nonbinary()
        else:
            if gender == "Male":
                return_dict["Anrede"] = "Herr"
            else:
                return_dict["Frau"] = "Herr"

    if suffix is True:
        if random.random() <= suffix_distribution:
            return_dict["Titel"] = fake.suffix_nonbinary()

    return return_dict

# TODO generate 1 json per person or have all of them bundled in a list (array)


def generate_adress_data():
    returndict = {}
    tempdict = {}

    tempdict["Straße"] = fake.street_name()
    tempdict["Hausnummer"] = fake.building_number()
    tempdict["PLZ"] = fake.postcode()
    tempdict["Stadt"] = fake.city_name()

    returndict["Adresse"] = tempdict
    return returndict

def country_list(visited_countries: int = 10):
    returndict = {}
    templist = []

    for i in range(visited_countries):
        templist.append(fake.country())
    returndict["Besuchte Länder"] = templist

    return returndict





def make_json_file(input_dict, json_name):
    with open(f"{json_name}.json", "w", encoding="utf-8") as outfile:
        outfile.write(json.dumps(input_dict, indent=2, ensure_ascii=False))


def make_nested_json(data_per_layer: int = 2, amount_layers: int = 2):
    returndict = {}

    prev_iteration_dict = {}

    nesting_dict = {}
    import pprint
    import copy
    for i in reversed(range(amount_layers)):
        tempdict = {}
        for k in range(data_per_layer):
            if k != (data_per_layer-1):
                tempdict[f"Layer_{i+1}_Dataset_{k+1}"] = f"Demo Data {k + 1}"
            else:
                if i == (amount_layers-1):
                    pass
                else:
                    tempdict["Nesting Here"] = {}
        logging.debug(f"Tempdict: {tempdict}")
        current_dict = {}
        logging.debug(f"prev_iteration_dict: {prev_iteration_dict}")
        if prev_iteration_dict == {}:
            prev_iteration_dict["Nesting Here"] = tempdict
        else:
            prev_iteration_dict = copy.deepcopy(prev_iteration_dict)
            tempdict["Nesting Here"] = copy.deepcopy(prev_iteration_dict)
            prev_iteration_dict = tempdict
            logging.debug(f"Tempdict after nesting: {tempdict}")

        if i == 0:
            returndict = copy.deepcopy(tempdict)

    return returndict


def generate_int_and_float(int_bool: bool = True, float_bool: bool = True, int_range_min: int = 0, int_range_max: int
                           = 100, float_range_min: float = 1, float_range_max: float = 6,
                           float_numbers_after_comma: int = 1):
    return_dict = {}
    import random
    if int_bool is True:
        return_dict["Alter"] = random.randint(int_range_min, int_range_max)
    if float_bool is True:
        return_dict["Abischnitt"] = round(random.uniform(float_range_min, float_range_max), float_numbers_after_comma)

    return return_dict

def Dataset_Generator(iterations: int, name_parameters: dict = None, name_bool: bool = False, address_bool: bool = False,
                      json_pathing: str = "jsons", country_bool: bool = False, country_param: int = 10, nested_bool:bool =
                      False, nested_parameters: dict = None, json_file_name: str = "Dataset",
                      numbers_bool: bool = False, numbers_parameters: dict = None):

    assert name_bool is True or address_bool is True or country_bool is True or nested_bool is True,\
        "One of the Bools must be true, otherwise there is no data to create a json with"
    import contextlib
    for i in range(iterations):
        if name_bool is True:
            # declare defaults for this parameter
            first_name = None
            last_name = None
            full_name = None
            prefix = None
            suffix = None
            gender_distribution = 0.5
            prefix_distribution = 0.2
            suffix_distribution = 0.2
            # attempt to get parameters from dictionary, if fails the Exception is ignored and the default declared
            # above gets used
            with contextlib.suppress(Exception):
                first_name = name_parameters["first_name"]
            with contextlib.suppress(Exception):
                last_name = name_parameters["last_name"]
            with contextlib.suppress(Exception):
                full_name = name_parameters["full_name"]
            with contextlib.suppress(Exception):
                prefix = name_parameters["prefix"]
            with contextlib.suppress(Exception):
                suffix = name_parameters["suffix"]
            with contextlib.suppress(Exception):
                gender_distribution = name_parameters["gender_distribution"]
                if gender_distribution == 0 or gender_distribution == 1:
                    gender_distribution = float(gender_distribution)
            with contextlib.suppress(Exception):
                prefix_distribution = name_parameters["prefix_distribution"]
                if prefix_distribution == 0 or prefix_distribution == 1:
                    prefix_distribution = float(prefix_distribution)
            with contextlib.suppress(Exception):
                suffix_distribution = name_parameters["suffix_distribution"]
                if suffix_distribution == 0 or suffix_distribution == 1:
                    suffix_distribution = float(suffix_distribution)
            name_data = generate_name_data(first_name=first_name,
                                           last_name=last_name,
                                           full_name=full_name,
                                           prefix=prefix,
                                           suffix=suffix,
                                           gender_distribution=gender_distribution,
                                           prefix_distribution=prefix_distribution,
                                           suffix_distribution=suffix_distribution)
        else:
            name_data = {}
        if address_bool is True:
            address_data = generate_adress_data()
        else:
            address_data = {}
        if country_bool is True:
            country_data = country_list(visited_countries=country_param)
        else:
            country_data = {}
        if nested_bool is True:

            # declare defaults for this parameter
            data_per_layer = 2
            amount_layers = 2
            # attempt to get parameters from dictionary, if fails the Exception is ignored and the default declared
            # above gets used
            with contextlib.suppress(Exception):
                data_per_layer = nested_parameters["data_per_layer"]
            with contextlib.suppress(Exception):
                amount_layers = nested_parameters["amount_layers"]

            nested_data = make_nested_json(data_per_layer=data_per_layer, amount_layers=amount_layers)
        else:
            nested_data = {}

        if numbers_bool is True:
            """
            int_bool: bool = True, float_bool: bool = True, int_range_min: int = 0, int_range_max: int
                           = 100, float_range_min: float = 1, float_range_max: float = 6,
                           float_numbers_after_comma: int = 1)
            """
            int_bool = True
            float_bool = True
            int_range_min = 0
            int_range_max = 100
            float_range_min = 1
            float_range_max = 6
            float_numbers_after_comma = 1

            with contextlib.suppress(Exception):
                int_bool = numbers_parameters["int_bool"]
            with contextlib.suppress(Exception):
                float_bool = numbers_parameters["float_bool"]
            with contextlib.suppress(Exception):
                int_range_min = numbers_parameters["int_range_min"]
            with contextlib.suppress(Exception):
                int_range_max = numbers_parameters["int_range_max"]
            with contextlib.suppress(Exception):
                float_range_min = numbers_parameters["float_range_min"]
            with contextlib.suppress(Exception):
                float_range_max = numbers_parameters["float_range_max"]
            with contextlib.suppress(Exception):
                float_numbers_after_comma = numbers_parameters["float_numbers_after_comma"]

            numbers_data = generate_int_and_float(int_bool=int_bool, float_bool=float_bool, int_range_min=int_range_min,
                                                  int_range_max=int_range_max, float_range_min=float_range_min,
                                                  float_range_max=float_range_max, float_numbers_after_comma=
                                                  float_numbers_after_comma)
        else:
            numbers_data = {}

        # combine the dictionaries into one dictionary
        dict_to_json = name_data | address_data
        dict_to_json = dict_to_json | country_data
        dict_to_json = dict_to_json | nested_data
        dict_to_json = dict_to_json | numbers_data
        if iterations == 1:
            make_json_file(dict_to_json, f"{json_pathing}/{json_file_name}")
        else:
            make_json_file(dict_to_json, f"{json_pathing}/{json_file_name}_{i+1}")





# end JSON Generator Module
#TODO handler if JSON directory does not exist yet
if __name__ == "__main__":
    print(make_nested_json(data_per_layer=3, amount_layers=4))


