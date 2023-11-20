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

## Example:
Run the script:

```bash
(base) 💻 daniel:tallycounter $ python ./tallycounter.py -t important_trait1,important_trait2,important_trait3 -o important_counting
```
Pressing keyboard keys 1,2 and 3 will increase the count:

```bash
[ info ] Press 1, 2, 3, ..., n to increase the respective counter
[ info ] Press 'q' to quit. Counter state will be saved to file.

  1. important_trait1:  5
  2. important_trait2:  6
  3. important_trait3:  10

_________________________________________________________________
```
At the end you get this:

```
(base) 💻 daniel:tallycounter $ ls -l
Mon Nov 20 07:51:30 2023 🗋 important_counting_20231120_075130.log
Mon Nov 20 07:26:50 2023 🗋 tallycounter.py
```

```bash
(base) 💻 daniel:tallycounter $ cat important_counting_20231120_075130.log
nr	Tally	count
1	important_trait1	5
2	important_trait2	6
3	important_trait3	10
```
