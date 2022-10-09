class Place:
    id = 0
    name = ""
    people = 0
    visits = 0
    max_capacity = 0
    capacity = 0

    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.people = 0
        self.visits = 0
        self.max_capacity = 0
        self.capacity = 0


places = []
places.append(Place(1, "town"))
places.append(Place(2, "volcano"))
places.append(Place(3, "prison"))
places.append(Place(4, "tomb"))
places.append(Place(5, "bank"))
places.append(Place(6, "j-store"))
places.append(Place(7, "museum"))
places.append(Place(8, "gas station"))
places.append(Place(9, "city base"))
places.append(Place(10, "power plant"))
places.append(Place(11, "casino"))
places.append(Place(12, "crater city"))
places.append(Place(13, "race track"))
places.append(Place(14, "sand road"))
places.append(Place(15, "airport"))
places.append(Place(16, "crime port"))
places.append(Place(17, "prison road"))
places.append(Place(18, "zone 51"))
places.append(Place(19, "jump (volcano)"))
places.append(Place(20, "desert"))
places.append(Place(21, "super prison"))
places.append(Place(22, "cargo"))

total_cnt = 0
with open('log.txt') as f:
   for line in f:
       if total_cnt > 4000:    break
       line = line.replace("\n","")

       #newline1650107040.745106;&&;2-1;7-1;6-1;1-1;5-0;4-0;9-0;10-0;11-0;8-0;14-0;19-0;21-0;3-0;12-0;13-0;15-0;16-0;17-0;18-0;20-0;22-0;
       if len(line) < 10: continue

       a = line.split("newline")[1].split(";&&;")
       time = a[0].strip()
       a = a[1].split(";")

       total_cnt += 1

       #print(time, " -> ", a)
       for p in a:
           if len(p) < 1: continue
           x = p.split("-")
           id = int(x[0].strip())
           people = int(x[1].strip())
           #print("\t",id," = ",people)
           if people > 0:
               for place in places:
                    if place.id == id:
                       place.people += people
                       place.visits += 1
                       if place.max_capacity < people: place.max_capacity = people

for p in places:
    p.capacity = round(p.visits / total_cnt * 100)

places.sort(key=lambda x: x.capacity, reverse=True)

print("Results of",total_cnt,"logs (" + str(int(total_cnt/60)) + " mins):")
for p in places:
    s_name = ""
    for i in range(15 - len(p.name)):
        s_name += " "
    print("\033[94m" + p.name + s_name + "\033[0m: people =\033[92m",p.people,"\033[0m, visits =\033[92m",p.visits,"\033[0m, max_cap =\033[92m",p.max_capacity,"\033[0m, capacity = \033[93m" + str(p.capacity) + "%\033[0m")
