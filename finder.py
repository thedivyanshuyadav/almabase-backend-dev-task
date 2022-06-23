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

    def check_fuzz_ratio(self) -> bool:
        """
        This methods checks the fuzz simple ratio between profiles by concatenating (first_name + last_name + email) as parameter.
        
        Return : [Bool] : checks whether the fuzz simple ratio match is greater than 80 or not.
        """
        n = len(self.profiles)
        for i in range(n):
            for j in range(i,n):
                p1 = self.profiles[i]
                p2 = self.profiles[j]
                if fuzz.ratio( getattr(p1,'first_name') + getattr(p1,'last_name') + getattr(p1,'email'), getattr(p2,'first_name') + getattr(p2,'last_name') + getattr(p2,'email') ) <= 80 : return False 
        return True

    def check_duplicates_result(self,fields:list) -> str:
        """
        This method checks duplicacy between profiles by considering explicitly provided field names.

        Parameter:
            fields      [list]   : list of field names which are to be considered for duplicates check.
        
        Return: 
            Report      [string] : Duplicacy check report.   
        """
        temp_profile = BaseProfile(None,None,None)
        all_fields = list(vars(temp_profile).keys())
        
        total_score = 0
        non_matching_attributes = set()
        
        ignored_attributes = set([field for field in all_fields if field not in fields])

        matching_attributes = set([field for field in fields if field in ['first_name','last_name','email']])
        fields = [field for field in fields if field not in ['first_name','last_name','email']]

        if self.check_fuzz_ratio():total_score += 1

        n = len(self.profiles)
        for i in range(n):
            for j in range(i+1,n):
                p1 = self.profiles[i]
                p2 = self.profiles[j]
                for field in fields:
                    if not getattr(p1,field) or not getattr(p2,field):
                        ignored_attributes.add(field)
                    elif getattr(p1,field) == getattr(p2,field):
                        matching_attributes.add(field)
                        total_score += 1
                    else:
                        non_matching_attributes.add(field)
                        total_score -= 1
        
        return (f'Profile 1, Profile 2, total match score: {total_score}, matching_attributes: {", ".join(matching_attributes if matching_attributes else ["None"])}, non_matching_attributes: {", ".join(non_matching_attributes if non_matching_attributes else ["None"])}, ignored_attributes: {", ".join(ignored_attributes if ignored_attributes else ["None"])}')

def find_duplicates(profiles:list,fields:list) -> None:
    """
    This method prints report by checking duplicates between provided profiles after considering provided fields.

    Parameter:
        profiles    [list]   : list of profiles which are to be check.
        fields      [list]   : list of field names which are to be considered for duplicates check.
    
    Return: None
    """
    sol = Solution(profiles=profiles)
    report = sol.check_duplicates_result(fields=fields)
    print(report)

