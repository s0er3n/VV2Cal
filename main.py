from bs4 import BeautifulSoup
import requests
from ics import Calendar, Event
import arrow
import tempfile
# kurse = input("Kursnummern(leertaste getrennt): ")


c = Calendar()


def add_course(kurs):
    r = requests.get(
        f"https://www.fu-berlin.de/vv/de/search?query={kurs}")
    soup = BeautifulSoup(r.text)
    dates = [(text.text.strip(
    ).split(" ")[1], text.text.strip(
    ).split(" ")[2], text.text.strip(
    ).split(" ")[4]) for text in soup.find_all(class_="course_date_time")]
    for date in dates:
        e = Event()
        e.name = soup.find_all("h1")[1].text
        year = date[0].split(".")[2]
        month = date[0].split(".")[1]
        day = date[0].split(".")[0]

        starthours = date[1].split(":")[0]
        startminutes = date[1].split(":")[1]

        endhours = date[2].split(":")[0]
        endminutes = date[2].split(":")[1]

        seconds = "00"
        begin = arrow.get(year + "-" + month + "-" + day + " " +
                          starthours + ":" + startminutes + ":" + seconds, 'YYYY-MM-DD HH:mm:ss')
        begin = begin.replace(tzinfo='Europe/Paris')
        begin = begin.to("utc")
        e.begin = begin.format('YYYY-MM-DD HH:mm:ss')
        end = arrow.get(year + "-" + month + "-" + day + " " +
                        endhours + ":" + endminutes + ":" + seconds, 'YYYY-MM-DD HH:mm:ss')
        end = end.replace(tzinfo='Europe/Paris')
        end = end.to("utc")
        e.end = end.format('YYYY-MM-DD HH:mm:ss')
        c.events.add(e)


def kal_datei_erstellen(kurse):
    kurse = kurse.split(" ")
    for kurs in kurse:
        add_course(kurs)

    temp = tempfile.TemporaryFile("w")
    temp.writelines(c)
    with open("test.txt", "wb") as test:
        test.write(temp)
    return temp
