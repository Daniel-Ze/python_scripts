from omadb import Client
import pandas as pd
from time import sleep
import os
import datetime

def oma_request(protein, start, out_file, sleep_time):
    """
    Using the omadb package for REST Api interaction of OMA Browser
    database. client.function() is called to retrieve the GO ID of 
    supplied protein sequnece.
    It uses a fast approximate search against all sequences in the 
    OMA database.
    https://github.com/DessimozLab/pyomadb/blob/master/examples/pyomadb-examples.ipynb

    Kaleb K, Warwick Vesztrocy A, Altenhoff A and Dessimoz C. Expanding the Orthologous Matrix (OMA) programmatic interfaces: REST API and the OmaDB packages for R and Python. F1000Research 2019, 8:42 (https://doi.org/10.12688/f1000research.17548.1)

    Connect to OMA database and request GO terms for closest match.
    The omadb python library is need to make the connection.
    Takes the parsed protein dictionary:
    
        dict = {SeqID1 : [Sequence length, 'Sequence'],
                SeqID2 : [Sequence length, 'Sequence']}
    
    For each protein sequence in dictonary request the GO terms from OMA.
    Protein sequences larger than 2500 AA are omited as this causes problems
    with the generated link to submit the data to OMA.
    Results are formated as dataframe and are saved with pandas to_csv() to 
    file in appaned mode. If restarting the script from scratch rename 
    or remove output file in folder.

    If the connection to the server is dropped unexpectedly the function 
    returns the index of the last paresed sequence in the dictonary.

    Returned result format:
    Assigned_by,,GO_ID,DB:Reference,Evidence,Approximation,Aspect,,,DB_Object_Type,Date,DB,Synonym,GeneID
    
    OMA_FastMap,,GO:0000822,OMA_Fun:002,IEA,Approx:VITVI12337:6609.6381433348415,F,,,protein,20220114,OMA_FastMap,inositol hexakisphosphate binding,VITVvi_vCabSauv08_v1.1_Haplotig000000F_038.ver1.0.g006310.t01
    """

    client = Client()
    count_p = 0
    sequence_ID = ""

    out_log = str(os.path.splitext(out_file)[0])+".log"

    logging = open(out_log, "a")
    logging.write(str(datetime.date.today())+" "+str(datetime.datetime.now())+"Start\n")

    if start > 0:
        count_p = start

    print(" %\tIndex\tProtID\n")

    try:
        for f in range(start,len(protein)):
        # extract the gene ID
            sequence_ID = list(protein)[f][1:]#.split("_")
            gene_ID = sequence_ID.lstrip()

            # Keep track of what's going on
            print(str(round((count_p / len(protein))*100,3))+"%",str(count_p+1),gene_ID.rstrip(), sep="\t", flush=True, end="\r")

            # Request the results from OMAbrowser
            if int(list(protein.values())[f][0]) < 2500:
                oma_res = client.function(list(protein.values())[f][1], as_dataframe=True)

                # Add geneID column
                oma_res['GeneID']=gene_ID

                # Export results to file
                oma_res.to_csv(out_file, mode='a', index=False, header=False)
                logging.write(str(datetime.date.today())+" "+str(datetime.datetime.now())+"\tFinished:\t{}\n".format(gene_ID))
                sleep(sleep_time)
                count_p = count_p + 1

    except Exception as err:
        logging.write(str(err))
        return int(count_p)

    logging.write("Finished.")
    logging.close()

    return len(protein)+1
    