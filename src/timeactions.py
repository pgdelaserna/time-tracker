#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
This script includes time actions to be performed by the user
"""

#================================================================#

# Built-in/Generic imports
import os
import sys

# Libraries
import datetime
import csv

__author__ = "pgdelaserna"
__version__ = "1.0"

#================================================================#

# Format to be used for each log record
dayfmt = "%d/%m/%Y"
timefmt = "%H:%M:%S"

# Headers of csv file
header = ['day', 'time', 'event', 'time_worked']

class TimeTracker:
  """
  Main class for time tracking
  """
  def __init__(self, filepath: str='time.csv') -> None:
    """
    Init function for time tracker
    """
    self.tracking_file = filepath
    self.time_in = self.get_time_in()
    self.time_out = self.time_in + datetime.timedelta(hours=2)

  def write_to_file(self, time: datetime.datetime, label: str, time_worked) -> None:
    """
    This function writes to the log file
    """
    # Break datetime into two: day and time
    day = time.strftime(dayfmt)
    time = time.strftime(timefmt)

    # Open file
    with open(self.tracking_file, 'a') as f:
      writer = csv.writer(f)
      # Write new line
      writer.writerow([day, time, label, str(time_worked)])

  def get_time_in(self) -> datetime.datetime:
    """
    This function stores the time in
    """
    # Return current time
    return datetime.datetime.now()

  def write_time_in(self) -> None:
    """
    This function writes the time in into file
    """
    self.write_to_file(self.time_in, 'TIME_IN', 'N/A')

  def write_time_out(self) -> None:
    """
    This function writes the time out into file
    """
    # When writing the time out we need to calculate time worked
    with open(self.tracking_file, 'r') as f:
      reader = csv.reader(f)

      # Ignore header
      next(reader)

      # Loop in reverse order
      for row in reversed(list(reader)):
        row_day = datetime.datetime.strptime(row[0], dayfmt)
        row_time = datetime.datetime.strptime(row[1], timefmt)

        # Look for same day and tag TIME_IN
        if row_day.day == self.time_out.day:
          # Get time in
          time_in_str = row[0] + '-' + row[1]
          self.time_in = datetime.datetime.strptime(time_in_str, dayfmt + '-' + timefmt)

          # Compute delta
          time_worked = self.time_out - self.time_in

    self.write_to_file(self.time_out, 'TIME_OUT', time_worked)


  def check_file_header(self) -> None:
    """
    This function checks if the file header exists and if not it writes it
    """
    # Check only if the file exists
    if os.path.exists(self.tracking_file):
      # Open file
      with open(self.tracking_file, 'r') as f:
        # Read first line
        reader = csv.reader(f)
        row1 = next(reader)
      # If header is not matching, write it otherwise pass
      if not row1 == header:
        self.write_file_header()
    else:
      # Write the file header if it does not exist
      self.write_file_header()

  def write_file_header(self) -> None:
    """
    This function writes the header
    """
    with open(self.tracking_file, 'w') as f:
      writer = csv.writer(f)

      # Write row
      writer.writerow(header)


# Executable code
if __name__ == '__main__':
  # Create object
  TT = TimeTracker()
  TT.check_file_header()
  TT.write_time_in()
  TT.write_time_out()