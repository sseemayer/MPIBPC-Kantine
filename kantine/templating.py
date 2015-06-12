import jinja2


def to_html(menu):
    env = jinja2.Environment(loader=jinja2.FileSystemLoader('assets/'))
    tmpl = env.get_template("mail_template.html")

    days = []

    for row in menu.iterrows():
        day = {
            "date": row['date'],
            "date_human": row['date'].strftime("%A %d. %b %Y"),
        }

        # TODO Add dishes

        days.apend(day)

    data = {
        "week": days[0]['date'].strftime("%W"),
        "days": days
    }

    return tmpl.render(**data)
