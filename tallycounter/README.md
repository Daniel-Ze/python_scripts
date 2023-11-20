# tallycounter.py
A script to count multiple things at the same time e.g. while sitting at the microscope.
Just define the things you want to count and put them in a comma seperated list. After quitting
the script will save the counts to file. Use '-o' to define a friendly name of the output.

The script has the following options:

```bash
(base) 💻 daniel:tallycounter $ python tallycounter.py --help
usage: tallycounter.py [-h] [-t TALLYS] [-o OUT]

Tally counter with keyboard input.

optional arguments:
  -h, --help            show this help message and exit
  -t TALLYS, --tallys TALLYS
                        Comma-separated list of options.
  -o OUT, --out OUT     Name of the output (default tally_out_datetime)
```
