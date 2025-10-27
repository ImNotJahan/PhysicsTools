from .data import MeasuredData

class Table2D:
    def __init__(self, columns=None, rows=None, column_labels=None, row_labels=None):
        if columns is None:
            columns = []
        if column_labels is None:
            column_labels = []
        if rows is None:
            rows = []
        if row_labels is None:
            row_labels = []

        self.columns = columns
        self.rows = rows
        self.column_labels = column_labels
        self.row_labels = row_labels

    def set_columns(self, columns: list[MeasuredData], column_labels: list[str]) -> None:
        # note to self: columns are along y
        self.columns = columns
        self.column_labels = column_labels

    def set_rows(self, rows: list[MeasuredData], row_labels: list[str]) -> None:
        # note to self: rows are along x
        self.rows = rows
        self.row_labels = row_labels

    def latex(self) -> str:
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