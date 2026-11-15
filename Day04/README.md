# Day 04 Assignment - Interactive Web Application with Flask

In this assignment, I took the qPCR Fold Change calculation from Day 03 and converted it into a local web application using Flask. After completing the initial requirements, I voluntarily upgraded the application to be fully interactive.

### What I did:
1. Copied the files from `day03` to `day04` to keep the previous implementation intact.
2. Created a Flask application (`app.py`) with an HTML template (`templates/index.html`) to display the data.
3. **Interactive Upgrade:** Added a web form with `enctype="multipart/form-data"` allowing users to upload their own `.xlsx` files for calculation.
4. **Example Data Feature:** Implemented a secondary button to automatically load and calculate my default experiment data (`EXP.30 Results.xlsx`) without needing to upload a file.
5. Added backend logic using `request.files` and `request.form` to dynamically route the user's choice and handle potential file errors gracefully.

### Prompts used:
**Initial Web App Prompt:**
"I have a Python script that calculates qPCR Fold Change from an Excel file named 'EXP.30 Results.xlsx' using pandas. Please write a simple Flask web application (app.py) that reads this file, runs the dCt and ddCt calculation logic as before, and displays the final results in an HTML table on the web page. Also, provide the HTML code for 'index.html' and explain how to structure the folders."

**Interactive Upgrade Prompt:**
"Make the Flask app interactive. I want any user to be able to upload their own Excel file with their raw data, and the site will calculate the 2^-ddCt for them. In addition, add a button to load an example file (EXP.30 Results.xlsx) so they can test it without uploading."