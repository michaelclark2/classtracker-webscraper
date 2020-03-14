from urllib import request
from bs4 import BeautifulSoup
import csv
import re

FAKE_HEADERS = {'User-Agent': 'Mozilla/5.0'}

def scrape_replit(student_name, url):
  if not url:
    print(f'ERROR: Url not found for {student_name}')
    return
  try:
    with request.urlopen(url) as rq:
      bs = BeautifulSoup(rq, 'html.parser')

      if not bs.find('div', class_='profile-no-repls') is None:
        print(f'ERROR: {student_name} has no repls')
        return

      repls = bs.find_all('a', class_='repl-item-wrapper')
      print(f'{student_name} has {len(repls)} repls')

  except Exception as e:
    print(f'ERROR: {student_name} {e}')

def scrape_codecademy(student_name, url):
  REQUIRED_BADGES = [
    "Lesson Completed: Objects",
    "Lesson Completed: Iterators",
    "Lesson Completed: Loops",
    "Lesson Completed: Arrays",
    "Lesson Completed: Scope",
    "Lesson Completed: Functions and Operations",
    "Lesson Completed: Variables",
    "Lesson Completed: Introduction to JavaScript",
    "Lesson Completed: Tables",
    "Lesson Completed: Introduction to HTML",
    "Lesson Completed: Learn HTML: Forms",
    "Lesson Completed: Learn HTML: Form Validation",
    "Lesson Completed: Advanced CSS Grid",
    "Lesson Completed: CSS Grid Essentials",
    "Lesson Completed: CSS Typography",
    "Lesson Completed: CSS Color",
    "Lesson Completed: CSS Display and Positioning",
    "Lesson Completed: Changing the Box Model",
    "Lesson Completed: The Box Model",
    "Lesson Completed: CSS Visual Rules",
    "Lesson Completed: CSS Setup and Selectors",
  ]

  def is_achievement_url(href):
    return href and re.compile('achievements').search(href)

  def is_badge_title(tag):
    return tag.name == 'h6' and 'title' in tag['class'][0]

  if url:
    try:
      req = request.Request(url, headers=FAKE_HEADERS)
      with request.urlopen(req) as profile:
        profile_soup = BeautifulSoup(profile, 'html.parser')
        achievement_link = profile_soup.find('a', href=is_achievement_url)


        if achievement_link is not None:
          badges_url = achievement_link['href']
          badge_req = request.Request(f'https://codecademy.com{badges_url}', headers=FAKE_HEADERS)
        else:
          print(f"{student_name} needs to update their privacy settings")
          return

        with request.urlopen(badge_req) as badges:

          badge_soup = BeautifulSoup(badges, 'html.parser')
          all_badges = badge_soup.find_all(is_badge_title)

          completed_badges = 0
          for badge in all_badges:
            if badge.contents[0] in REQUIRED_BADGES:
              completed_badges += 1
          percent_complete = int((completed_badges / len(REQUIRED_BADGES)) * 100)
          # TODO: do something with this percentage

    except Exception as e:
      print(e)

def scrape_freecodecamp(student_name, url):
  pass

def main():
  with open('students.csv') as students_csv:
    reader = csv.DictReader(students_csv)
    for student in reader:
      name = f'{student["firstName"]} {student["lastName"]}'
      #scrape_replit(name, student['replIt'])
      scrape_codecademy(name, student['codeAcademy'])
      scrape_freecodecamp(name, student['freeCodeCamp'])

if __name__ == "__main__":
    main()