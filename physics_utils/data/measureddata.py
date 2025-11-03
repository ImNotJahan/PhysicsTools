from .md_steps import StepsExtension

class MeasuredData(StepsExtension):
    """
    Represents a numerical measurement with uncertainty

    Attributes
    ----------
    value : float
        The actual value of the data
    reading_error : float
        The error from the instrument reading
    standard_error : float
        The statistical standard error

    Notes
    -----
    This class automatically propagates uncertainty through calculations
    """
    def __init__(self, measurement: float, reading_error: float, standard_error=0.0):
        self.value = measurement
        self.reading_error = reading_error
        self.standard_error = standard_error



if __name__ == "__main__":
    import doctest
    doctest.testmod()
