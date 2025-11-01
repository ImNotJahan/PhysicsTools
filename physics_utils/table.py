from .data import MeasuredData

class Table2D:
    """
    Creates a two dimensional table, with the first row having labels for all the data
    """
    def __init__(self, rows=None, column_labels=None):
        if column_labels is None:
            column_labels = []
        if rows is None:
            rows = []

        self.rows = rows
        self.column_labels = column_labels

    def set_labels(self, column_labels: list[str]) -> None:
        """
        Sets the labels for each column in the table
        """
        # note to self: columns are along y
        self.column_labels = column_labels

    def set_data(self, rows: list[list[MeasuredData]]) -> None:
        """
        Sets the rows of the table, with each sublist in rows being a row
        """
        # note to self: rows are along x
        self.rows = rows

    def latex(self) -> str:
        """
        Generates this table in LaTeX
        """
        sb = "\\begin {center}\n\r"
        sb += "\t\\begin {tabular}"
        sb += "{" + "|c" * len(self.column_labels) + "|}\n\r"
        sb += "\t\t\\hline\n\r\n\r\t\t"

        sb += " & ".join(self.column_labels)
        sb += " \\\\\n\r\t\t\\hline\n\r\n\r"

        for row in self.rows:
            sb += "\t\t"
            sb += " & ".join([x.latex() if isinstance(x, MeasuredData) else str(x) for x in row])
            sb += " \\\\\n\r\t\t\\hline\n\r\n\r"

        sb += "\t\\end {tabular}\n\r"
        sb += "\\end {center}"

        return sb