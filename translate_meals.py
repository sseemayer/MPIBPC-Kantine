#!/usr/bin/env python
import os

import kantine.translate
import kantine.database
from kantine.models import Meal


def main():

    translator = kantine.translate.Translator(email=os.environ.get("MYMEMORY_EMAIL"), key=os.environ.get("MYMEMORY_KEY"))

    session = kantine.database.session
    for meal in session.query(Meal).filter(Meal.name_en == None).all():
        try:
            translation = translator.translate(meal.name)
            meal.name_en = translation

            print(u"{0} --translated--> {1}".format(meal.name, meal.name_en))
        except Exception as e:
            print(e)

    session.commit()

if __name__ == '__main__':
    main()
