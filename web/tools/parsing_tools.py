import pandas as pd


def parse_html_table(html_table: str) -> pd.DataFrame:
    data = pd.read_html("<table>" + html_table + "</table>")[0]
    data = data.drop(19, axis=1).drop([0, 1, 2], axis=0)
    data.columns = [
        "id",
        "name",
        "all",
        "all_aud",
        "all_lec",
        "all_prac",
        "all_lab",
        "indep",
        "control",
        "first_lec",
        "first_prac",
        "first_lab",
        "first_ex",
        "first_test",
        "second_lec",
        "second_prac",
        "second_lab",
        "second_ex",
        "second_test",
    ]
    return data
