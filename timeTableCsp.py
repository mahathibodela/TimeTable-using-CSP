import time
import collections
import copy
def makeDomain():
    secSub = ["pssp", "dld", "dldlab", "dsa", "dsalab", "os", "dm", "oslab"]
    thirdSub = ["lp", "tdpl", "tdpllab", "mp", "mplab", "ai", "ailab", "oe"]
    fourthSub = ["crypo", "bd", "dl", "bdlab", "dbms", "ee", "projlab"]
    assignments = {}
    
    # converting sub to no (as takes less space), for lab using -ve no to identify
    # creating domain for every period in 2nd, 3rd, 4rth year
    # populating totPer :- no of periods per course

    totPer = {}
    subToNo = {}
    c = 1
    subs = {}
    second = set()
    for sub in secSub:
        if len(sub) > 3 and sub[-3:] == "lab":
            k = -1 * c 
            totPer[k] = 1
        else:
            k = c 
            totPer[k] = 3

        second.add(k)
        subToNo[sub] = k
        c += 1
    second.add(100)
    totPer[100] = 6
    subs[0] = second
    
    third = set()
    for sub in thirdSub:
        if len(sub) > 3 and sub[-3:] == "lab":
            k = -1 * c 
            totPer[k] = 1
        else:
            k = c 
            totPer[k] = 3

        third.add(k)
        subToNo[sub] = k
        c += 1
    third.add(101)
    totPer[101] = 6
    subs[1] = third
    
    forth = set()
    for sub in fourthSub:
        if len(sub) > 3 and sub[-3:] == "lab":
            k = -1 * c 
            totPer[k] = 1
        else:
            k = c 
            totPer[k] = 3

        forth.add(k)
        subToNo[sub] = k
        c += 1
    totPer[102] = 6
    forth.add(102)
    subs[2] = forth

    # populating subToPro
    subToPro = {}
    subToPro[subToNo["pssp"]] = "samadrita"
    subToPro[subToNo["dld"]] = "dhanusree"
    subToPro[subToNo["dldlab"]] = "dhanusree"
    subToPro[subToNo["dsa"]] = "karthik"
    subToPro[subToNo["dsalab"]] = "karthik"
    subToPro[subToNo["os"]] = "gireesh"
    subToPro[subToNo["dm"]] = "koushik"
    subToPro[subToNo["oslab"]] = "gireesh"


    subToPro[subToNo["lp"]] = "mg"
    subToPro[subToNo["tdpl"]] = "mounica"
    subToPro[subToNo["tdpllab"]] = "sunil"
    subToPro[subToNo["mp"]] = "prakash"
    subToPro[subToNo["mplab"]] = "prakash"
    subToPro[subToNo["ai"]] = "himabindhu"
    subToPro[subToNo["ailab"]] = "prasad"
    subToPro[subToNo["oe"]] = "meenakshi"


    subToPro[subToNo["crypo"]] = "sunil"
    subToPro[subToNo["bd"]] = "battu"
    subToPro[subToNo["bdlab"]] = "srilatha"
    subToPro[subToNo["dl"]] = "srilatha"
    subToPro[subToNo["dbms"]] = "prasad"
    subToPro[subToNo["ee"]] = "chaitra"
    subToPro[subToNo["projlab"]] = "prasad"
    totPer[subToNo["projlab"]] = 2

    # populating proToSub
    proToSub = collections.defaultdict(list)
    for key, item in subToPro.items():
        proToSub[item].append(key)
    
    # creating matric of varibles with thier respective domains
    domain = []
    for i in range(5): # 5 days for 5 days a week
        hours = []
        for j in range(6): # 6 for 6 hours a day (max working)
            years = []
            for k in range(3): # 3 for 3 years we are handling
                s = subs[k].copy()
                years.append(s)
            hours.append(years)
        domain.append(hours)
    
    return (domain, subToPro, proToSub, subToNo, subs, totPer, assignments)

def nextPeriod(day, hour, year):
    if hour < 5:
        return (day, hour + 1, year)
    if hour == 5 and day < 4:
        return (day + 1, 0, year)
    return (0, 0, year + 1)

def addAll(q, day, hour, year, reverse):

    #add all the hours of the class - also in reverse order
    for i in range(hour+ 1, 6): 
        if reverse == 1:
           q.append(((day, i, year), (day, hour, year)))
        q.append(((day, hour, year), (day, i, year)))

    #add all the hours for another classes - also in reverse order
    for i in range(year + 1, 3):
        if reverse == 1:
           q.append(((day, hour, i), (day, hour, year)))
        q.append(((day, hour, year), (day, hour, i)))



def arcConsistent(day, hour, year, domains, totPer, sub, subToPro, proToSub, freeTime):
    ndomains = copy.deepcopy(domains)
    a = set()
    a.add(sub)
    ndomains[day][hour][year] = a
    ntotPer = {}

    for key, item in totPer.items():
        ntotPer[key] = item
    ntotPer[sub] = ntotPer[sub] - 1

    if ntotPer[sub] == 0: # if no of periods of sub is completed then all domains se usko nikalna hain
        for i in range(day + 1, 5):
            for j in range(6):
                if sub in ndomains[i][j][year]:
                    ndomains[i][j][year].remove(sub)
                    if len(ndomains[i][j][year]) == 0:
                        return (None, None, None)
    

    q = [] #jo assigen nehi kiya sirph uska add karenge bas
    addAll(q, day, hour, year, 1)
   
    # we check, if for every value in right do we have a value in left or not
    while q :
        left, right = q.pop(0)

        if left[2] == right[2]: #same year -- same day

            tempDomain = ndomains[right[0]][right[1]][right[2]].copy()
            leftDomain = ndomains[left[0]][left[1]][left[2]]

            for value in tempDomain:
                if value in leftDomain and len(leftDomain) == 1:
                    ndomains[right[0]][right[1]][right[2]].remove(value)
                    if len(ndomains[right[0]][right[1]][right[2]]) == 0:
                        return (None, None, None)
                    addAll(q, right[0], right[1], right[2], 0)
        
        else:

            leftProfSet = set()

            for sub in ndomains[left[0]][left[1]][left[2]]:
                if sub != 100 and sub != 101 and sub != 102:
                   leftProfSet.add(subToPro[sub])
            tempDomain = ndomains[right[0]][right[1]][right[2]].copy()

            for value in tempDomain:
                if value != 100 and value != 101 and value != 102:
                    prof = subToPro[value]
                    if prof in leftProfSet and len(leftProfSet) == 1:
                        ndomains[right[0]][right[1]][right[2]].remove(value)
                        if len(ndomains[right[0]][right[1]][right[2]]) == 0:
                            return (None, None, None)
                        addAll(q, right[0], right[1], right[2], 0)

    return (ndomains, ntotPer, freeTime)


def forwardChecking(day, hour, year, domains, totPer, sub, subToPro, proToSub, freeTime):
    ndomains = copy.deepcopy(domains)
    ntotPer = {}
    nfreeTime = {}
  
    for key, item in totPer.items():
        ntotPer[key] = item
    
    ntotPer[sub] = ntotPer[sub] - 1
    if ntotPer[sub] == 0: # if no of periods of sub is completed then all domains se usko nikalna hain
        for i in range(day + 1, 5):
            for j in range(6):
                if sub in ndomains[i][j][year]:
                    ndomains[i][j][year].remove(sub)
                    if len(ndomains[i][j][year]) == 0:
                        return (None, None, None)

    k = 1
    if sub < 0 : k = 3
    if sub < 100 or ((sub == 100 or sub == 101 or sub == 102) and (ntotPer[sub] == 0)):
      for i in range(hour + k , 6): # this works same even if its a lab
          if sub in ndomains[day][i][year]: 
              ndomains[day][i][year].remove(sub) # making sure ki wo wont get repeated in the same day bt it should be done for lesuire periods right
              if len(ndomains[day][i][year]) == 0:
                  return (None, None, None)
    
    if sub == 100 or sub == 101 or sub == 102:
       return (ndomains, ntotPer, nfreeTime)

    prof = subToPro[sub]
  
    a = set()
    a.add(sub)
    for i in range(year + 1, 3): # removing the sub taught by same professor for other classes
        for j in range(k): # now this also works same even if its a lab
            for diffCour in proToSub[prof]:
                if diffCour in ndomains[day][hour + j][i]:
                    ndomains[day][hour + j][i].remove(diffCour)
                    ndomains[day][hour + j][year] = a
                    if len(ndomains[day][hour + j][i]) == 0:
                       return (None, None, None)

    return (ndomains, ntotPer, nfreeTime)


def makeTimeTable(day, hour, year, domains, subToPro, proToSub, sumToNo, subs, totPer, freeTime, assignments, n, start_time):
    # print("***********************")
    # for k in range(3):
    #     for i in range(5):
    #         for j in range(6):
    #                 if (i, j, k) in assignments:
    #                     print("(", i, j, k, ")", assignments[(i, j, k)])
    #     print("_--------------") 

    if n > 21 or year == 3 :
        return True

    for sub in domains[day][hour][year]:
        if sub < 0:
            if (hour != 0 and hour != 3): continue
            for i in range(3):
                assignments[(day, hour + i, year)] = sub
            if hour == 0:
                nday, nhour, nyear = day, 3, year
            else:
                nday, nhour, nyear = nextPeriod(day, 5, year)

        else:
            nday, nhour, nyear = nextPeriod(day, hour, year)
            assignments[(day, hour, year)] = sub
           
     
        ndomains, ntotPer, nfreeTime = arcConsistent(day, hour, year, domains, totPer, sub, subToPro, proToSub, freeTime)
  
        if ndomains != None and makeTimeTable(nday, nhour, nyear, ndomains, subToPro, proToSub, sumToNo, subs, ntotPer, nfreeTime, assignments, n + 1, start_time):
            return True

        k = 1
        if sub < 0:
            k = 3
        for i in range(k):
            assignments.pop((day, hour + i, year))
    

    return False


if __name__ == "__main__":
    domains, subToPro, proToSub, sumToNo, subs, totPer, assignments = makeDomain()
    # /assignments = {}
    tried = {}
    freeTime = {
                  0 : 6,
                  1 : 6,                   
                  2 : 6
               }

    print(domains[0][0][0], domains[0][0][1],domains[0][0][2])
    print(assignments)
    start_time= []
    start_time.append(time.time())
    k = makeTimeTable(0, 0, 0, domains, subToPro, proToSub, sumToNo, subs, totPer, freeTime, assignments, 0, start_time)

    print(k)
    for k in range(3):
        for i in range(5):
            for j in range(6):
                    if (i, j, k) in assignments:
                        print("(", i, j, k, ")", assignments[(i, j, k)])
      