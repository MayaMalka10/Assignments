# Day 04 Assignment - Web Application with Flask

In this assignment, I took the qPCR Fold Change calculation from Day 03 and converted it into a local web application using Flask. 

### What I did:
1. Copied the files from `day03` to `day04` to keep the previous implementation intact.
2. Created a Flask application (`app.py`) that reads the `EXP.30 Results.xlsx` file and calculates the dCt and ddCt (Fold Change) using pandas.
3. Created an HTML template (`templates/index.html`) to display the calculated results in a clean table format on the browser.
4. Handled a `FileNotFoundError` by explicitly providing the correct path to the Excel file.
5. Tested the local development server to ensure both the Python backend logic and the web interface work correctly.

### Prompts used:
"I have a Python script that calculates qPCR Fold Change from an Excel file named 'EXP.30 Results.xlsx' using pandas. Please write a simple Flask web application (app.py) that reads this file, runs the dCt and ddCt calculation logic as before, and displays the final results in an HTML table on the web page. Also, provide the HTML code for 'index.html' and explain how to structure the folders."