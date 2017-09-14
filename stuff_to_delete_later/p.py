import csv

moons = []

with open('moons.csv', 'r') as f:
  dr = csv.DictReader(f)
  while True:
    try:
      moons.append(dr.next())
    except:
      break

print moons
