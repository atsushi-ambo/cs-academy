def find_ports(db, team, host):
    sql = "SELECT port FROM endpoints WHERE team = ? AND host = ? ORDER BY port"
    return db.execute(sql, (team, host)).fetchall()


def sort_column(field):
    return {"name": "label", "number": "port"}.get(field)


def team_services(db, team, order):
    orders = {"name": "label, port", "number": "port, label"}
    columns = orders.get(order)
    if columns is None:
        return None
    sql = "SELECT label, port FROM services WHERE team = ? ORDER BY " + columns
    return db.execute(sql, (team,)).fetchall()
