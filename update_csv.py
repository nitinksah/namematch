# Python imports
import pandas as pd
import csv
import os


class updateCSVColumn(object):
    cwd = os.getcwd()
    abs_path = os.path.join(cwd, "csv_files")

    def __init__(self, output_csv):
        self.output_csv = output_csv

    @staticmethod
    def update_column(column=None, path=None, values=None, unnamed_flag=None):
        data_frame = pd.read_csv(path)

        if unnamed_flag:
            unnamed = [""]
            head = list(data_frame.head())[1:]
            head.append(column)
            unnamed.extend(head)
            rows = [unnamed]
        else:
            head = list(data_frame.head())
            head.append(column)
            rows = [head]
        count = 0
        for idx, row in data_frame.iterrows():

            row = list(row)
            row.append(values[count])
            rows.append(list(row))
            count += 1
        return rows

    def __call__(self, **kwargs):
        file_path = os.path.join(self.abs_path, kwargs["file_name"] + ".csv")

        rows = self.update_column(
            column=kwargs["column"],
            path=file_path,
            values=kwargs["values"],
            unnamed_flag=kwargs["unnamed_flag"],
        )

        file_path = os.path.join("\\".join(file_path.split("\\")[:-1]), self.output_csv)

        with open(file_path, "w", newline="", encoding="utf-8") as data_file:
            # create the csv writer object
            csv_writer = csv.writer(data_file, lineterminator="\n")

            # write to the same file
            csv_writer.writerows(rows)
