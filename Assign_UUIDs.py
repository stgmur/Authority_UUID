'''
Created on Aug 12, 2015

@author: SGmur
'''

import unicodecsv
import os
import uuid
import csv

def getAuthDict(auth_doc_path):
    """ makes a dictionary for the accepted values present in an autority
    document """

    auth_dict = {}
    with open(auth_doc_path, 'rU') as f:
        fields = ['conceptid','Preflabel','altlabels','ParentConceptid',
                      'ConceptType','Provider']
        rows = unicodecsv.DictReader(f, fieldnames=fields,
            encoding='utf-8-sig', delimiter=',', restkey='ADDITIONAL',
                                     restval='MISSING')
        rows.next()
        for row in rows:
            auth_dict[row['Preflabel']] = row['conceptid']

    return auth_dict


def makeEntityAuthDocDict(auth_doc_directory):
    """ makes a dictionary of the items in the ENTITY_TYPE_X_ADOC.csv file """

    entity_auth = os.path.join(auth_doc_directory,"ENTITY_TYPE_X_ADOC.csv")
    if not os.path.isfile(entity_auth):
        print("""Unable to locate the ENTITY_TYPE_X_ADOC.csv document.  This document must be
                  present and correctly named in the authority document directory in order for you to continue.
                AUTHORITY DOCUMENT DIRECTORY: {0}""".format(auth_doc_directory))
        exit()

    entity_auth_dict = {}
    with open(entity_auth, 'rU') as f:
        fields = ['entitytype','authoritydoc','authoritydocconceptschemename']
        rows = unicodecsv.DictReader(f, fieldnames=fields,
            encoding='utf-8-sig', delimiter=',', restkey='ADDITIONAL',
                                     restval='')
        rows.next()
        for row in rows:
            entity_auth_dict[row['entitytype']] = os.path.join(
                auth_doc_directory,row['authoritydoc'])

    missing = [v for v in entity_auth_dict.values() if not os.path.isfile(v)]
    if len(missing) > 0:
        print("""The authority documents listed below are used in ENTITY_TYPE_X_ADOC.csv, but
              do not exist in the authority document directory.  Fix this problem before trying again.""")
        for m in missing:
            print("    {0}".format(os.path.basename(m)))               
        exit()

    return entity_auth_dict

if __name__ == '__main__':
    auth_doc_directory = r'C:\Users\sgmur\Documents\GitHub\Authority_UUID\concepts\authority_files'
    output_directory = r'C:\Users\sgmur\Documents\GitHub\Authority_UUID\UID_authority_documents'
    
    log_directory = out_dir = os.path.dirname(os.path.realpath(__file__))
    
        # create a dictionary of authority documents with the entity_id as the key
    authorityDocDictionary = makeEntityAuthDocDict(auth_doc_directory)
    
    log_file = open(log_directory + '\\' + 'log_reassignment.txt','wb')
    log_file.write('uid|conceptid|preflabel|AltLabels|ParentConceptid|ConceptType|Provider|Concept_id|Authority_doc_path\n')
    
    for item_key,item_value in authorityDocDictionary.iteritems():
        dict_name = item_value.split('\\')[-1]
        output_file = open(output_directory + '\\' + dict_name,'wb')
        output_file.write('conceptid,PrefLabel,AltLabels,ParentConceptid,ConceptType,Provider\n')
        with open(item_value, 'rU') as f:
            fields = ['conceptid','Preflabel','AltLabels','ParentConceptid','ConceptType','Provider']
            rows = unicodecsv.DictReader(f, fieldnames=fields, encoding='utf-8-sig', delimiter=',', restkey='ADDITIONAL',restval='MISSING')
            rows.next()
            
            for row in rows:
                row_uuid = uuid.uuid4()
                output_file.write(str(row_uuid) + ',' + row['Preflabel'] + ',' + row['AltLabels'] + ',' +
                                   row['ParentConceptid'] + ',' + row['ConceptType'] + ',' + row['Provider'] + '\n')
                log_file.write(str(row_uuid) + '|' + row['conceptid'] + '|' + row['Preflabel'] + '|' + row['AltLabels'] + '|' +
                                   row['ParentConceptid'] + '|' + row['ConceptType'] + '|' + row['Provider'] + '|' + item_key + '|' + item_value + '\n')