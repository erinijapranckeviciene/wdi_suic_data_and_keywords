import pandas as pd
import numpy as np
from numpy import array
import sys

'''
To change
cat data_agestd.csv | 
sed 's/Antigua_and/Antigua_and_Barbuda/' | 
sed 's/Bosnia/Bosnia_and_Herzegovina/' | 
sed 's/Democratic_Republic_Congo/Congo_Dem_Rep./' |
sed 's/Congo,/Congo_Rep.,/' | 
sed 's/Egypt/Egypt,_Arab_Rep./' | 
sed 's/Quatar/Qatar/' | 
sed 's/Iran/Iran,_Islamic_Rep./' | 
sed 's/Kyrgyzstan/Kyrgyz_Republic./' | 
sed 's/Laos/Lao_PDR/' | sed 's/Micronesia/Micronesia,_Fed_Sts../' | 
sed 's/Slovakia/Slovak_Republic/' | sed 's/Saint_Lucua/St._Lucia/' | 
sed 's/Caint_Vincent_and_Grenadines/St._Vincent_and_the_Grenadines/' | 
sed 's/Syria/Syrian_Arab_Republic/' | 
sed 's/Venezuaela/Venezuela,_RB/' | 
sed 's/Yemen/Yemen,_Rep./'
'''

file_name=sys.argv[1]

dat=pd.read_csv(file_name)
print(dat)

countries=np.unique(dat['Location'])
print(countries)
print(len(countries))

years=[2000,2001,2002,2003,2004,2005,2006,2007,2008,2009,2010,2011,2012,2013,2014,2015,2016,2017,2018,2019]
dflines=[]
# collect all data for males and females to compute percentiles
all_males=[]
all_females=[]

for country in countries:
    dslice=dat[ dat['Location']==country]
    print(dslice)

    dictitem={}
    dictitem['Country']=country

    for year in years:
        #bitem=dslice[ dslice['Period']==year]['Both']
        #mitem=dslice[ dslice['Period']==year]['Male']
        fitem=dslice[ dslice['Period']==year]['Female']

        #fbitem=float(bitem.to_string().split('    ')[1].split(' [')[0])
        #fmitem=float(mitem.to_string().split('    ')[1].split(' [')[0])
        ffitem=float(fitem.to_string().split('    ')[1].split(' [')[0])

        dictitem[str(year) + '_females']=ffitem
        all_females.append(ffitem)
        #dictitem[str(year) + '_males']=fmitem

    for year in years:
        #bitem=dslice[ dslice['Period']==year]['Both']
        mitem=dslice[ dslice['Period']==year]['Male']
        #fitem=dslice[ dslice['Period']==year]['Female']

        #fbitem=float(bitem.to_string().split('    ')[1].split(' [')[0])
        fmitem=float(mitem.to_string().split('    ')[1].split(' [')[0])
        #ffitem=float(fitem.to_string().split('    ')[1].split(' [')[0])

        #dictitem[str(year) + '_females']=ffitem
        dictitem[str(year) + '_males']=fmitem
        all_males.append(fmitem)

    print(dictitem)
    dflines.append(dictitem)

# percentiles
pf=np.percentile(all_females, [0, 34, 67, 100])
pm=np.percentile(all_males, [0, 34, 67, 100])
print("Females ",pf)
print("Males ",pm)

# columns
female_cols=[str(year)+'_females' for year in years]
male_cols=[str(year)+'_males' for year in years]


#print(dflines)
df=pd.DataFrame(data=dflines)
print(female_cols)
print(male_cols)

#extend data frame
df['low_females']=[0]*df.shape[0]
df['med_females']=[0]*df.shape[0]
df['high_females']=[0]*df.shape[0]

df['low_males']=[0]*df.shape[0]
df['med_males']=[0]*df.shape[0]
df['high_males']=[0]*df.shape[0]

print(df)

#add aditional info to the data frame
for country in countries:
    females_arr=df[df['Country']==country][female_cols]
    males_arr=df[df['Country']==country][male_cols]
    
    sl=np.sum(np.array(females_arr)<pf[1])
    sm=np.sum(np.array(females_arr)<pf[2])-sl
    
    df.loc[df['Country']==country,'low_females']=(sl/len(years))*100
    df.loc[df['Country']==country,'med_females']=(sm/len(years))*100
    df.loc[df['Country']==country,'high_females']=( (len(years)-(sm+sl))/len(years) )*100

    print(df[df['Country']==country][['low_females', 'med_females', 'high_females'] ])

    sl=np.sum(np.array(males_arr)<pm[1])
    sm=np.sum(np.array(males_arr)<pm[2])-sl
    
    df.loc[df['Country']==country,'low_males']=(sl/len(years))*100
    df.loc[df['Country']==country,'med_males']=(sm/len(years))*100
    df.loc[df['Country']==country,'high_males']=( (len(years)-(sm+sl))/len(years) )*100

    print(df[df['Country']==country][['low_males', 'med_males', 'high_males'] ])


# change country names
new_name=countries.copy()

for i,name in enumerate(countries):
    if name=='Antigua_and':
        new_name[i]='Antigua_and_Barbuda'
    if name=='Bosnia':
        new_name[i]='Bosnia_and_Herzegovina' 
    if name=='Democratic_Republic_Congo':
        new_name[i]='Congo_Dem_Rep.'
    if name=='Congo':
        new_name[i]='Congo_Rep.'
    if name=='Egypt':
        new_name[i]='Egypt_Arab_Rep.'
    if name=='Quatar':
        new_name[i]='Qatar'
    if name=='Iran':
        new_name[i]='Iran,_Islamic_Rep.'
    if name=='Kyrgyzstan':
        new_name[i]='Kyrgyz_Republic'
    if name=='Laos':
        new_name[i]='Lao_PDR'
    if name=='Micronesia':
        new_name[i]='Micronesia_Fed_Sts.'
    if name=='Slovakia':
        new_name[i]='Slovak_Republic'
    if name=='Saint_Lucua':
        new_name[i]='St._Lucia'
    if name=='Saint_Vincent_and_Grenadines':
        new_name[i]='St._Vincent_and_the_Grenadines'
    if name=='Syria':
        new_name[i]='Syrian_Arab_Republic'
    if name=='Venezuaela':
        new_name[i]='Venezuela_RB'
    if name=='Yemen':
        new_name[i]='Yemen_Rep.'

df['Country_name']=new_name

df.to_csv('age_standardized.csv')


