# -*- coding: utf-8 -*-
"""
Created on Fri Dec 21 11:01:29 2018

@author: OWebsdell
"""


def write_csv(file,writemode,info):
    if type(file) is not str:
        print('write_csv: file path must be entered as a string.')
        return
    if type(writemode) is not str:
        print('write_csv: writemode must be a string (like "a" or "w").')
        return
    if type(info) is not tuple:
        print('write_csv: information to be written should be a tuple.')
        return
    import csv                                           # import the csv package
    with open(file, writemode,newline='',encoding="utf-8") as outfile:    # open the file
            writr = csv.writer(outfile, delimiter=',')   # define the file writer
            writr.writerows(info)                        # write the information to the file  

def import_cities(file_path: str) -> list:
    """
    Takes a file path of a csv and returns a list
    of city tuples containing a label (the city number),
    an x-coordinate, and a y-coordinate.
    """
    import csv
    from collections import namedtuple
    city = namedtuple('city','label x y')
    with open(file_path,'r', encoding = 'UTF-8') as csv_file:
         file_reader = csv.reader(csv_file, delimiter=',')
         content = []
         file_reader = list(file_reader)
         for line in file_reader[1:]:
             data_row = list(line)
             this_city = city(data_row[0],float(data_row[1]),float(data_row[2]))
             content.append(this_city)
    return content

def is_prime(city_number: int) -> bool:
    """
    Takes an int and determines whether or not it's a prime
    number.
    """
    for i in range(2,city_number):
        if city_number % i == 0:
            return False
    return True

def city_distance(city_A: tuple, city_B: tuple) -> float:
    """
    Takes two cities and calculates the Euclidean distance between them.
    """
    x_dist = (city_A.x - city_B.x)**2
    y_dist = (city_A.y - city_B.y)**2
    dist = (x_dist + y_dist)**(1/2)
    return dist

def is_near(city: tuple, x_l: float, x_u: float,
                         y_l: float, y_u: float):
    """
    Takes a city tuple and identifies if it is in a given range.
    """
    x_coor, y_coor = city.x, city.y
    if x_coor >= x_l and x_coor <= x_u:
        if y_coor >= y_l and y_coor <= y_u:
            return True
    return False

def get_unchecked_cities(full_cities: list, checked: list, boundaries: list) -> list:
    """
    Takes the lists of all cities and the nearby boundaries
    and returns a list of nearby cities that can be checked for distance.
    """
    b = boundaries
    unch = [int(c.label) for c in full_cities if is_near(c,b[0],b[1],b[2],b[3]) is True and c.label not in checked]
    return unch

def get_next_distance(r: list, that_c: tuple, all_c: list) -> float:
    bnds  = get_bounds(that_c)
    avail = get_unchecked_cities(all_c, r, bnds)
    next_ds = [[c,city_distance(that_c,all_c[c])] for c in avail]
    return next_ds[0][1]

def get_nearest(near_cities: list, this_city: tuple,
                rout: list, all_: list, step_no: int) -> int:
    dists = []
    for there in near_cities:
        there = all_[there]
        dist = city_distance(this_city,there)
        rout += [this_city.label]
        next_dist = get_next_distance(rout,there,all_)
        if step_no % 10 == 0:
            if is_prime(this_city.label) is False:
                dist = dist * 1.1
        elif step_no % 10 == 0:
            if is_prime(there.label) is False:
                next_dist = next_dist * 1.1
        stat = [there.label, dist+next_dist]
        dists.append(stat)
    dists = sorted(dists,key=lambda c: c[1])
    return dists[0][0]

def get_bounds(city_tuple: tuple, radius: int = 200) -> list:
    return [city_tuple.x - 200, city_tuple.x + 200,city_tuple.y - 200, city_tuple.y + 200]

def find_route(list_city_tuples: list, out_file_path: str) -> list:
    import time
    route, current_city, step, time_taken, no_cits = [0], 0, 1, 0, len(list_city_tuples)
    print('%s cities' % no_cits)
    while step < no_cits:
        timestart = time.time()
        print('Step: %s, city: %s, time: %s' % (step,current_city,time_taken))
        bounds = get_bounds(list_city_tuples[current_city])
        nearby_cities = get_unchecked_cities(list_city_tuples,route,bounds)
        nearest = get_nearest(nearby_cities,list_city_tuples[current_city],route,list_city_tuples,step)
        current_city = nearest
        route.append(current_city)
        step += 1
        if step % 100 == 0:
            write_csv(out_file_path,'w',tuple(route))
        time_taken = time.time() - timestart
    print('Step: %s, city: 0' % step)
    write_csv(out_file_path,'w',tuple(route))
    return route

filein = r' - FILE PATH - '
fileout = r' - FILE PATH - '
cities = import_cities(filein)
route = find_route(cities, fileout)
