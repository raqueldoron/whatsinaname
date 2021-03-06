def names_parser(isBoy):
    from os import listdir
    from os.path import isfile, join
    from csv import reader
    myPath = "/a/fr-05/vol/prime/stud/cppdoron/python/whatsinaname/names/"
    onlyfiles = [yearFile for yearFile in listdir(myPath) if isfile(join(myPath, yearFile))]
    onlyfiles.sort(reverse=True)
    counter = 0
    m_names_and_values = {}
    f_names_and_values = {}
    for yearFile in onlyfiles:
        counter = counter + 1
        multiplicationFactor = 1.0 / counter
        yearTable = reader(open(myPath + yearFile))
        for line in yearTable:
            #males
            if (line[1] == 'M'):
                if(line[0] in m_names_and_values):
                    m_names_and_values[line[0]] += (int(line[2]) * multiplicationFactor)
                else:
                    m_names_and_values[line[0]] = (int(line[2]) * multiplicationFactor)
            #females
            elif (line[1] == 'F'):
                if(line[0] in f_names_and_values):
                    f_names_and_values[line[0]] += (int(line[2]) * multiplicationFactor)
                else:
                    f_names_and_values[line[0]] = (int(line[2]) * multiplicationFactor)
    m_sorted_list = sorted(m_names_and_values, key = m_names_and_values.__getitem__, reverse = True)
    f_sorted_list = sorted(f_names_and_values, key = f_names_and_values.__getitem__, reverse = True)
    m_sorted_list = m_sorted_list[:500]
    f_sorted_list = f_sorted_list[:500]
    malesSorted = open("malesSorted.txt", "w")
    femalesSorted = open("femalesSorted.txt", "w")
    j = 0
    for name in m_sorted_list:
        malesSorted.write(name + "\n")
    for name in f_sorted_list:
        femalesSorted.write(name + "\n")
    malesSorted.close()
    femalesSorted.close()
    return m_sorted_list if isBoy else f_sorted_list
