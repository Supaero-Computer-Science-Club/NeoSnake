def log(*args, sep=' ', end='\n'):
    """
        Logs a list of elements inside the 'log.log' file.

        Args
        ----
        args : list of anything with a str method
            all the elements to log into 'log.log'
        sep : str
            the separator between each element.
        end : str
            the end of the final string that will be logged.

        Returns
        -------
        None
    """
    with open("log.log", 'a') as file:
        file.write(sep.join(map(str, args)) + end)
