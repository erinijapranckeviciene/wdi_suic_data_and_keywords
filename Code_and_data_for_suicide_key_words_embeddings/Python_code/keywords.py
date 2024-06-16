#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 29 10:25:04 2024

@author: erin
"""
import os
import re
import glob

def kwd_string(de,id):
    de_list=de.replace('/',';').split(";")
    id_list=id.replace('/',';').split(";")
    words=[]
    for phrase in de_list:
        word='_'.join(phrase.lstrip().rstrip().lower().split(' '))
        words.append(word)
    for phrase in id_list:
        word='_'.join(phrase.lstrip().rstrip().lower().split(' '))
        words.append(word)

    kwds=' '.join(words)+'.'
    kwds=re.sub(r'_+', '_', kwds)
   
    if len(kwds)>2:
        return kwds
    else:
        return ''


dname='/home/erin/JUDITA/mdpi_sustainability/PAPER_DATA/Web_of_Science_records/'
print(dname)
clust=['C2_clust','C4_clust','C5_clust','C6_clust','C7_clust','C8_clust','C9_clust','C10_clust']

clust_dirs=glob.glob(dname+"*_clust")
print(clust_dirs)

for clust in clust_dirs:
    # create a directory for keywords is it does not exist
    keywords_country_dir=clust+"/Keywords/"
    if not os.path.exists(keywords_country_dir):
        # Create the directory
        os.makedirs(keywords_country_dir)

    country_dirs=glob.glob(clust+"/Countries/*")
    for country in country_dirs:
        print(country)
        country_name=country.split("/")[-1]
        
        # save keywords in one file per country in Keywords
        # save each title separately in Titles/Country         
        saved_recs=glob.glob(country+"/savedrecs*.txt")
        #print(saved_recs)
        # country_texts will have all titles+keywords
        country_titles = {}
        # save dir for country texts
        titles_country_dir=clust+"/Titles/"+ country_name +"/"
        if not os.path.exists(titles_country_dir):
            # Create the directory
            os.makedirs(titles_country_dir)        
        
        # country_keywords will have all titles+keywords
        country_keywords_dict={}
        country_keywords=[]
        
        saved_recs_batch=-1
        for ddir in saved_recs:
            ## Create loop over countries
            saved_recs_batch+=1
            
            f=open(ddir)
            lines=f.read()
            #print(lines)
            records=lines.split('\nER\n\n')
            
            for i,record in enumerate(records):
                #create key as country_batch_record    
                title_key=country_name+"_"+str(saved_recs_batch)+"_"+str(i)
                #print(record)
                parts=record.split('\n')
                record_dict={}
                current_key='UNK'
                for j,part in enumerate(parts):
                    #print("\n new part \n")
                    #print(part)
                    #print(len(part))
                    #print( len(part.split())) 
                    #print("\n end new part \n")
                    if len(part.split())>0:               
                        sbegin=part.split()[0]
                        srest=part.split()[1:]
                        
                        #print(sbegin)
                        if len(sbegin)>2:
                            #print("same line, append dictionary")
                            if current_key in record_dict:
                                record_dict[current_key]=record_dict[current_key] + part
                        else:
                            #print("new line, start dict entry")
                            key=sbegin
                            record_dict[key]=' '.join(srest)
                            current_key=key
                            
                print("\n\n new record formed\n\n")
                                                
                #print(record_dict)
                text=''
                
                if 'TI' in record_dict:
                    print(record_dict[str('TI')] )
                    text=text+record_dict[str('TI')]+'. '
                if 'DE' in record_dict:
                    print(record_dict[str('DE')] )
                    DE=record_dict[str('DE')]
                else:
                    DE=''
                if 'ID' in record_dict:
                    print(record_dict[str('ID')] )
                    ID=record_dict[str('ID')]
                else:
                    ID=''

                keywords=kwd_string(DE,ID).lstrip()
                text=text+keywords
                text=re.sub(r' +', ' ', text)
                # Text must be clean
                # 
                
                
                print(title_key)
                print(text)
                # write the record
                country_titles[title_key]=text
                
                print(keywords)
                country_keywords.append(keywords.rstrip("."))

                # here we can output a record
                with open(titles_country_dir+title_key+".keywords.txt","w") as fw:
                    fw.write(text)
                
        # Write keywords only
        # Remove empty strings firs
        while('' in country_keywords):
            country_keywords.remove("")
            
        with open(keywords_country_dir+country_name+".keywords.txt","w") as fw:
            fw.write('\n'.join(country_keywords) )
        # save to the dictionary
        # From this structure we generate country-keyword pairs
        print(country_keywords)
        print(len(country_keywords))
        #country_keywords[country_name]=' '.join(country_keywords)
        country_keywords_dict[country_name]=country_keywords

    # Countries in cluster finished 
    # we could form new dictionary for per cluster data



'''
with open(ddir+"savedrecs.txt") as f:
    for line in f:
       print(line.rstrip()) 
       if line.rstrip()[0:1]=='ER':
           print("New line")
       #(key, val) = line.split()
       #d[int(key)] = val
       #print(key)
       #print(val)
 '''      