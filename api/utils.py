import datetime


def days_left(birthdate):
    """Returns the number of days to the given date.

    Args:
        custom_date (date): date of format `YYYY-MM-DD`

    Returns:
        int: number of days to the given date.
    """
    today = datetime.date.today()

    if today.month == birthdate.month and today.day > birthdate.day or today.month > birthdate.month : # birthday is coming up next year - we past it
        next_birthday_year = today.year + 1
        
    else: 
        next_birthday_year = today.year # this means we are not past the birthdate yet

    update_date = datetime.date(next_birthday_year, birthdate.month, birthdate.day)
    next_birthday = update_date - today

    return next_birthday.days

def has_letters_only(user_string):
    """Returns True if string contains letters only or False otherwise.

    Args:
        custom_date (str): string to check.

    Returns:
        bool: True if string contains letters only or False otherwise.
    """
    if not user_string.isalpha():
        return False
    else:
        return True
    
def is_past_date(custom_date):
    """Checks if the given date is in the past.

    Args:
        custom_date (date): date to check

    Returns:
        bool: Returns True if the given date is in the past or False otherwise.
    """
    today = datetime.datetime.now().date()

    if custom_date < today:
        return True
    else:
        return False