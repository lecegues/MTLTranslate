with open('sites.txt', 'r') as f:
    lines = f.readlines()

for line in lines:
    print("main("+line.strip()+")")
