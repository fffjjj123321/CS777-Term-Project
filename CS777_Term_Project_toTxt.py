import pandas as pd
 
#.csv->.txt
data = pd.read_csv('CS777_Final_Project_Test_Dataset.csv')
with open('./Covid_Data.txt','a+',encoding='utf-8') as f:
    for line in data.values:
        if pd.isnull(line[0]):
            line[3] = 0
        f.write((str(line[5])+'\t'+str(line[1])+'\t'+str(line[2])+'\t'
                +str(int(line[6]))+'\t'+str(line[8])+'\t'+str(line[0])+'\n'))


