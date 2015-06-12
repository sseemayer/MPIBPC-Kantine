import pandas as pd
import pdftableextract as pdf
import datetime


def parse_menu(path):
    pages = ["1"]
    cells = [pdf.process_page(path, p) for p in pages]
    cells = [item for sublist in cells for item in sublist]
    li = pdf.table_to_list(cells, pages)[1]
    tbl = pd.DataFrame(li[2:-1], columns=li[1], index=[l[0] for l in li[2:-1]])

    tbl.drop(u'', 1, inplace=True)
    tbl.columns = ['date', 'meal1', 'meal2', 'sides', 'wok_or_pasta', 'special']

    tbl['date'] = tbl['date'].apply(parse_date)

    return tbl


def parse_date(date):
    date = date[(date.index(", ") + 2):]
    return datetime.datetime.strptime(date, "%d.%m.%Y").date()
