# Day 04 & Day 05 Assignment - Interactive qPCR Web Application with Flask

In this assignment, I took the qPCR Fold Change calculation from Day 03 and converted it into a local web application using Flask. After completing the initial requirements, I voluntarily upgraded the application to be fully interactive, and later added automated unit tests for the core business logic.

## Project Files
* `app.py` – The main Flask web application and qPCR calculation logic (`calculate_qpcr_from_df`).
* `templates/index.html` – The HTML interface for uploading files and viewing the results table.
* `analyze_exp.30_qpcr.py` – The original standalone terminal script from Day 03.
* `EXP.30 Results.xlsx` – Experimental qPCR dataset used as the built-in example file.
* `test_app.py` – Automated `pytest` unit tests verifying the calculation logic and error handling.

## How to Run

First, open a terminal inside the `Day04` folder and ensure the required libraries are installed:
```bash
pip install flask pandas openpyxl pytest
```

### 1. Run the Interactive Web Application (`app.py`)
To launch the Flask web server, run:
```bash
python app.py
```
Then open your browser and go to `http://127.0.0.1:5000`. From there, you can upload your own `.xlsx` file or click **Load Example Data (EXP.30)** to run the calculation on the built-in dataset.

### 2. Run the Standalone Terminal Script (`analyze_exp.30_qpcr.py`)
To run the original command-line script directly without the web interface:
```bash
python analyze_exp.30_qpcr.py
```

### 3. Run the Automated Unit Tests (`test_app.py`)
To verify the qPCR calculation logic using `pytest`:
```bash
python -m pytest
```

---

## Day 04 - Interactive Web Application Details

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

---

## Day 05 Assignment - Unit Testing Business Logic

To verify the reliability of the qPCR calculation logic independently from the Flask web interface, I added automated unit tests using `pytest` in `test_app.py`:
1. **Calculation Accuracy (`test_calculate_qpcr_valid_data`):** Tests `calculate_qpcr_from_df` with controlled Ct values to verify exact `dCt`, `ddCt`, and `2^-ddCt` Fold Change outputs for baseline (`1.0`), downregulation (`0.5`), and upregulation (`2.0`).
2. **Missing Column Handling (`test_calculate_qpcr_missing_column`):** Verifies that missing required columns return a graceful error message instead of crashing.
3. **Missing Gene Handling (`test_calculate_qpcr_missing_target_gene`):** Ensures missing target/reference gene data is caught properly.