from finder import BaseProfile, find_duplicates

# Child Class 
class Profile(BaseProfile):
    def __init__(self,first_name,last_name,email,date_of_birth=None,class_year=None):
        # Add new fields here.

        super().__init__(first_name,last_name,email,date_of_birth,class_year)

if __name__ == "__main__":

    profile1 = Profile(
        email='knowkanhai@gmail.com',
        first_name = 'Kanhai',
        last_name = 'Shah',
        class_year = 2012,
        date_of_birth = '1990-10-11',
    )
    profile2 = Profile(
        email='knowkanhai@gmail.com',
        first_name = 'Kanhai',
        last_name = 'Shah',
        class_year = 2012,
        date_of_birth = '1990-10-11'
    )

    find_duplicates(profiles=[profile1,profile2],fields=['first_name','last_name','email','class_year','date_of_birth'])
