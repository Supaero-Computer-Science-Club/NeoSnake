class CustomError(Exception):
    pass


# class CustomError(Exception):
#     """Exception raised for errors in the input salary.
#
#     Attributes:
#         salary -- input salary which caused the error
#         message -- explanation of the error
#     """
#
#     def __init__(self, salary, message="Salary is not in (5000, 15000) range"):
#         self.salary = salary
#         self.message = message
#         super().__init__(self.message)
#
#     def __str__(self):
#         return f'{self.salary} -> {self.message}'

def error_handler(func):
    def wrapper(*args, **kwargs):
        try:
            res = func(*args, **kwargs)
            return res
        except CustomError as ce:
            print(ce)
        except KeyboardInterrupt:
            pass

    return wrapper
