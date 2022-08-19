#import argparse

#parser = argparse.ArgumentParser()
#parser.add_argument("--start_year", type=int)
#parser.add_argument("--end_year", type=int)
#parser.add_argument("--word_list", nargs="+")
#parser.add_argument("--prod_list", nargs="+" )

#args = parser.parse_args()
#print(args.start_year)
#print(args.end_year)
#print(args.word_list)
#print(args.prod_list)
#print(f'start year = {args.start_year} ... end_year = {args.list}')
#new_list_str = str(args.list)
#print(new_list_str)

from hashlib import new

# get its attention again
test = ['SEA BREEZE', 'SEABREEZE', 'HAPPY']
mystr = ''
for t in test:
    newt = t.replace(' ', '_')
    print(newt)
    mystr = mystr + newt + ' '

print(mystr)