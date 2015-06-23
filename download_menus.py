#!/usr/bin/env python
import os
import datetime
import tempfile
import redis

import kantine.download
import kantine.parse
import kantine.database
import kantine.models


def main():

    r = redis.Redis.from_url(os.environ.get("REDIS_URL"))

    menu_urls = kantine.download.get_menu_urls()

    print("see URLs: {0}".format(menu_urls))

    dl_urls = [mu for mu in menu_urls if not r.hget("seen", mu)]

    for du in dl_urls:

        try:
            print("download: {0}".format(du))

            with tempfile.NamedTemporaryFile() as f:
                kantine.download.download_menu(du, f)
                menu = kantine.parse.parse_menu(f.name)

            meals = []
            for mtype in menu.columns[1:]:
                for date, meal in zip(menu['date'], menu[mtype]):
                    if meal.strip():
                        meals.append(kantine.models.Meal(name=meal, name_en=None, date=date, mealtype=mtype))

            kantine.database.session.add_all(meals)
            kantine.database.session.commit()

            r.hset("seen", du, datetime.datetime.now())

        except Exception as e:
            print("Error: {0}".format(e))

if __name__ == '__main__':
    main()
