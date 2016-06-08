import csv
import string
import os

def to_dict(filename):
    name_dict = {}
    with open(filename, 'rb') as csvfile:
        rows = csv.DictReader(csvfile)
        for row in rows:
            name = row.get('name')
            num = row.get('num')
            sn = row.get('sn')
            if name is not None:
                names = string.split(name.strip())
                for n in names:
                    obj = {'num': num.strip(), 'sn': sn.strip(), 'full': name.strip()}                        
                    if name_dict.get(n) is None:
                        obj_list = []
                        obj_list.append(obj)
                        name_dict[n] = obj_list
                    else:
                        name_dict[n].append(obj)
                        
    return name_dict

def mismatch_score(name1, name2):
    name1_list = string.split(name1)
    name2_list = string.split(name2)
    name2_dict = {}

    for n in name2_list:
        name2_dict[n] = True

    count = len(name1_list)
    for n in name1_list:
        if name2_dict.get(n) is not None:
            count -= 1
    return count

def get_likely_match(name, name_dict):
    name_list = string.split(name)
    min_score = len(name_list)
    num = None
    sort = None
    for n in name_list:
        name_options = name_dict.get(n)
        if name_options is not None:
            for no in name_options:
                score = mismatch_score(name, no['full'])
                if score < min_score:
                    min_score = score
                    num = no['num']
                    sort = no['sn']
    return {'name': name, 'acc': num, 'sort': sort}
    

def create_matched_nums(filename, name_dict):
    matches = []
    with open(filename, 'rb') as rcsvfile:
        rows = csv.DictReader(rcsvfile)
        count = 0
        for row in rows:
            count += 1
            name = row.get('NAME')
            if name is None:
                name = row.get('NAME OF OFFICER')
            num = None
            if name is not None:
                match = get_likely_match(name.strip(), name_dict)
                row['Account Number'] = match['acc']
                row['Sort Number'] = match['sort']
                matches.append(row)
        print "Total rows: " + str(count)
    return matches

def write_to_csv(filename, rows):
    with open(filename, 'w') as csvfile:
        if len(rows) == 0:
            print "Nothin to write. Weird!"
            return
        header = rows[0].keys()
        writer = csv.DictWriter(csvfile, fieldnames=header)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)

def write_directory(dirname, name_dict):
    filenames = os.listdir(dirname)
    for filename in filenames:
        if filename.endswith('.csv'):            
            print filename
            matches = create_matched_nums(dirname + '/' + filename, name_dict)
            print "Matched rows: " + str(len(matches))
            write_to_csv(dirname + '/output/' + filename, matches)                

def write_all(dirnames):
    name_dict = to_dict('sorted.csv')
    for dirname in dirnames:
        write_directory(dirname, name_dict)
    print "Done"

write_all(['orbalga', 'udenulga', 'udunedemlga'])


