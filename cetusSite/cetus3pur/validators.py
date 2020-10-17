###
# validation for forms
###

# check if user name is of form abc123 or a123456
# True - valid user name
# False - does not seem valid
def validateUserName(candidateName):
    if(len(candidateName) < 3):
        return False
    elif not candidateName[0].isalpha()  or not any(char.isdigit() for char in candidateName):
        return False
    else:
        return True



