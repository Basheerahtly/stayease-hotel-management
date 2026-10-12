
# StayEase Hotel Management System

A command-line hotel management system written in Python, built as a team project of five students at Asia Pacific University (Programming with Python module, Year 1).

This is the version submitted for assessment, kept unchanged.

## What it does

Five types of user log in to their own menu:

- **Guest:** check room availability, make and cancel bookings, view bills and payment history, make special requests
- **Receptionist:** register guests, check them in and out, charge late check-out fees
- **Accountant:** record payments, view income and outstanding amounts, generate monthly reports
- **Housekeeping:** update cleaning status, report maintenance issues, build a daily cleaning schedule
- **Manager:** add, update and remove rooms, view a system summary, generate daily and monthly reports

All data is stored in CSV files. Every input is validated, and each login locks after three failed attempts.

## My contribution

I developed the **Manager module**:

- Adding, updating and removing rooms, with prices set automatically by room type
- A system summary showing total bookings, occupancy rate and total income
- Daily and monthly reports, displayed on screen and saved to files

## Running it

```bash
python Combined_Assignment.py
```

Demo login for the manager role: username `manager`, password `admin123`.
