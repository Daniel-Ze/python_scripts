def usage():
    """
    Print usage information and exit.
    """
    
    print("\n")
    print("This script uses the OMA database to infer protein function.")
    print("It uses a fast approximate search against all sequences in the OMA database.")
    print("\n")
    print("https://github.com/DessimozLab/pyomadb/blob/master/examples/pyomadb-examples.ipynb")
    print("Example 5 - annotating protein sequences not present in OMA")
    print("\n")
    print("For big datasets a request delay can be set to prevent flooding the service.")
    print("The default delay time is set to 5s. This number can be scaled down for small datasets.")
    print("\n")
    print("Usage: python oma_go.py -i protein.fa")
    print("\n")
    print("\t-i / --input=\tFasta formatted protein sequences")
    print("\t-d / --delay=\tRequest submit delay in seconds (default 5s)")
    print("\t-s / --start=\tResume the script at a certain protein if it failed.")
    print("\n")
    exit()