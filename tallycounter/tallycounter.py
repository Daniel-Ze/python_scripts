#!/usr/bin/env python

import argparse
import curses
import os
from datetime import datetime


class TallyCounter:
    def __init__(self, options, out):
        self.options = options
        self.out = out
        self.counters = {option: 0 for option in options}


    def display_counters(self, stdscr):
        '''
        Display the defined couters and some help.
        stdscr.addstr(x, y, "your text here")
            - x = vertical pos
            - y = horizontal pos
        '''

        stdscr.clear()
        stdscr.addstr(0, 0, "[ info ] Press 1, 2, 3, ..., n to increase the respective counter", curses.color_pair(2))
        stdscr.addstr(1, 0, "[ info ] Press 'q' to quit. Counter state will be saved to file.", curses.color_pair(2))
        
        for i, option in enumerate(self.options, start=3):
            stdscr.addstr(i, 0, f"  {i-2}. {option}:\t{self.counters[option]}")
        
        stdscr.addstr(len(self.options)+4, 0, "_________________________________________________________________", curses.color_pair(2))
        stdscr.refresh()


    def process_key(self, key):
        '''
        Check which key was pressed by the user.
        Only do something if key is a number.
        Add to counter of user supplied options.
        '''
        
        if key.isdigit():
            digit = int(key)
            if 1 <= digit <= len(self.options):
                option = self.options[digit - 1]
                self.counters[option] += 1


    def write_results(self):
        cwd = os.getcwd()
        current_datetime = datetime.now()
        fmt_datetime = current_datetime.strftime("%Y%m%d_%H%M%S")

        if self.out == None:
            self.out = "tally_out"
        
        output_file = str(cwd)+"/"+self.out+"_"+str(fmt_datetime)+".log"
        
        with open(output_file, 'w') as out:
            out.write("nr\tTally\tcount\n")
            for i,j in enumerate(self.options, start=0):
                out.write(str(str(i+1)+"\t"+self.options[i]+"\t"+str(self.counters[j])+"\n"))

    def main(self, stdscr):
        '''
        The main part of the script.
        Get colors for curses, hide the cursor, clear the screen.
        Run as long as the user doesn't press 'q' to quit.
        '''

        curses.start_color()
        curses.use_default_colors()
        for i in range(0, curses.COLORS):
            curses.init_pair(i, i, -1)

        curses.curs_set(0)  # Hide the cursor
        stdscr.clear()

        while True:
            self.display_counters(stdscr)
            key = stdscr.getch()  # Get the unicode code of the pressed key

            if key == ord('q'):  # Check if the unicode code matches that of the unicode code of 'q'
                self.write_results()
                
                break
            
            elif key in [ord(str(i)) for i in range(1, len(self.options) + 1)]:
                self.process_key(chr(key))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Tally counter with keyboard input.")
    parser.add_argument("-t", "--tallies", type=str, help="Comma-separated list of options.")
    parser.add_argument("-o", "--out", type=str, help="Name of the output (default tally_out_datetime)")
    args = parser.parse_args()

    if not args.tallies:
        parser.error("Please provide options using the -t flag.")

    options = args.tallies.split(',')
    tally_counter = TallyCounter(options, args.out)    
    curses.wrapper(tally_counter.main)

