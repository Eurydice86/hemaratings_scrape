def drop_table(table):
    return f"DROP TABLE IF EXISTS {table}"


def create_table(table, columns):
    create = f"CREATE TABLE {table} ("

    cols = ""

    for k, v in columns.items():
        cols += f"{k} {v}, "
    cols = cols[:-2]
    ending = ")"

    return_str = create + cols + ending

    return return_str


def insert(table, row):
    ins = f"INSERT INTO {table} ("

    rows = ""
    values = "VALUES ("
    for k, v in row.items():
        v = str(v).replace("'", "''")
        rows += f"{k}, "
        values += f"\'{v}\', "
    rows = rows[:-2] + ") "
    values = values[:-2] + ") "

    full = ins + rows + values

    return full


if __name__ == "__main__":
    club_dict = {
        "club_id": 2,
        "club_name": "EHMS",
        "club_short_name": "EHMS",
        "country": "Finland",
        "state": None,
        "city": "Helsinki",
        "parent_club_id": None,
    }

    insert("clubs", club_dict)
