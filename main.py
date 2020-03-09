from urllib import request
from bs4 import BeautifulSoup
import csv

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
  pass

def scrape_freecodecamp(student_name, url):
  pass

def main():
  with open('students.csv') as students_csv:
    reader = csv.DictReader(students_csv)
    for student in reader:
      name = f'{student["firstName"]} {student["LastName"]}'
      scrape_replit(name, student['replIt'])
      scrape_codecademy(name, student['codeAcademy'])
      scrape_freecodecamp(name, student['freeCodeCamp'])

if __name__ == "__main__":
    main()