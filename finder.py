from dataclasses import fields
from fuzzywuzzy import fuzz

class BaseProfile:
    """
    A class for Profile.
    Mandatory Fields: first_name, last_name, email
    Optional Fields:  date_of_birth, class_year 
    """
    def __init__(self,first_name,last_name,email,date_of_birth=None,class_year=None):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.date_of_birth = date_of_birth
        self.class_year = class_year

class Solution:
    def __init__(self, profiles:list):
        self.profiles = profiles

    def check_fuzz_ratio(self,fields:list) -> bool:
        """
        This methods checks the fuzz simple ratio between profiles by concatenating (first_name + last_name + email) as parameter.
        
        Return : [Bool] : checks whether the fuzz simple ratio match is greater than 80 or not.
        """
        p1, p2 = self.profiles
        part1 = []
        part2 = []
        for field in fields:
            part1.append(str(getattr(p1,field)))
            part2.append(str(getattr(p2,field)))
        ratio = fuzz.ratio( ''.join(part1), ''.join(part2) )
        if ratio <= 80 : return False 
        return True

    def check_duplicates_result(self,fields:list,sequence:list) -> str:
        """
        This method checks duplicacy between profiles by considering explicitly provided field names.

        Parameter:
            fields      [list]   : list of field names which are to be considered for duplicates check.
        
        Return: 
            Report      [string] : Duplicacy check report.   
        """
        nth, mth = sequence
        p1,p2 = self.profiles

        temp_profile = BaseProfile(None,None,None)
        all_fields = list(vars(temp_profile).keys())
        
        total_score = 0
        ignored_attributes = set([field for field in all_fields if field not in fields])

        matching_attributes = set()
        non_matching_attributes = set()

        for field in ['first_name','last_name','email']:
            if field in fields:
                if getattr(p1,field) == getattr(p2,field):matching_attributes.add(field)
                else:non_matching_attributes.add(field)


        # Scoring
        if self.check_fuzz_ratio(set(['first_name','last_name','email']).intersection(set(fields))):total_score += 1
        fields = [field for field in fields if field not in ['first_name','last_name','email']]

        for field in fields:
            if str(getattr(p1,field)) == str(getattr(p2,field)):
                matching_attributes.add(field)
                total_score += 1
            else:
                non_matching_attributes.add(field)
                total_score -= 1
        
        # Rendering Report
        return (f'Profile {nth}, Profile {mth}, total match score: {total_score}, matching_attributes: {", ".join(matching_attributes if matching_attributes else ["None"])}, non_matching_attributes: {", ".join(non_matching_attributes if non_matching_attributes else ["None"])}, ignored_attributes: {", ".join(ignored_attributes if ignored_attributes else ["None"])}')

def find_duplicates(profiles:list,fields:list) -> None:
    """
    This method prints report by checking duplicates between provided profiles after considering provided fields.

    Parameter:
        profiles    [list]   : list of profiles which are to be check.
        fields      [list]   : list of field names which are to be considered for duplicates check.
    
    Return: None
    """
    n = len(profiles)
    for profile1__idx in range(n):
        for profile2__idx in range(profile1__idx+1,n):
            profile1 = profiles[profile1__idx]
            profile2 = profiles[profile2__idx]
            sol = Solution(profiles=[profile1,profile2])
            report = sol.check_duplicates_result(fields=fields,sequence=[profile1__idx+1,profile2__idx+1])
            print(report)

