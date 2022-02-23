# oma_go - Querying the orthologous matrix browser (OMA)
## What it is good for
Get GO IDs for unknown protein sequences using the client.function() function implemented in the python **omadb** REST Api.  \
The package is described here: https://github.com/DessimozLab/pyomadb \
The website of orthologous matrix browser (OMA): https://omabrowser.org/oma/home/ \

With this script you're querying a database so you need a working internet connection.

## Script basis
The basis of the script here is based on the 
example 5 from the example jupyter notebook on the official omadb github page: https://github.com/DessimozLab/pyomadb/blob/master/examples/pyomadb-examples.ipynb

From the GitHub jupyter notebook:
It uses a fast approximation of the submitted protein sequences to the closest 
relative and GO ID is assigend from this approximation.

When using this script you confirm to cite the following:

Kaleb K, Warwick Vesztrocy A, Altenhoff A and Dessimoz C. Expanding the Orthologous Matrix (OMA) programmatic interfaces: REST API and the OmaDB packages for R and Python. F1000Research 2019, 8:42 (https://doi.org/10.12688/f1000research.17548.1)

## 1. Usage
```
(base) 💻 daniel:oma_go $ python oma_go.py 

This script uses the OMA database to infer protein function.
It uses a fast approximate search against all sequences in the OMA database.

https://github.com/DessimozLab/pyomadb/blob/master/examples/pyomadb-examples.ipynb
Example 5 - annotating protein sequences not present in OMA

For big datasets a request delay can be set to prevent flooding the service.
The default delay time is set to 5s. This number can be scaled down for small datasets.


Usage: python oma_go.py -i protein.fa


        -i / --input=   Fasta formatted protein sequences
        -d / --delay=   Request submit delay in seconds (default 5s)
        -s / --start=   Resume the script at a certain protein if it failed.
```

## 2. Requirements
  - Python >= 3.6
  - pip install omadb
  - pip install pandas

## 3. Testing if all is working
```
(base) 💻 daniel:~ $ cd oma_go
(base) 💻 daniel:oma_go $ python oma_go.py -i oma_go/test/protein.fa
```
