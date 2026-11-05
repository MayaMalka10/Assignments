# Day 03 Assignment - qPCR Analysis

In this assignment, I wrote a Python script to calculate gene expression fold change using the 2^-ddCt method.
The data is stored in `qpcr_data.csv`.
In addition, I also uploaded a xlsx file with real results I had called `EXP.30 Results.xlsx`, and created a new python code that reads this file and calculate the gene expression fold change using the 2^-ddCt method.

## Prompts used for csv file:
"Write a Python program that reads a CSV file named 'qpcr_data.csv' with columns: Sample, Target_Ct, Reference_Ct. Create a function that calculates the Fold Change using the 2^(-delta delta Ct) method. Use the 'Control' sample as the baseline. Print the final Fold Change for the 'Treated' sample"

## Prompts used for Excel file:
"Write a Python program using pandas that reads the Excel file 'EXP.30 Results.xlsx'.

Read only the columns: 'Sample Name', 'Target Name', and 'Ct Mean'.

The reference gene is 'GAPDH' and the target gene is 'RRBP1'.

Create a function that calculates the Fold Change (2^-ddCt). First, calculate dCt (Ct_Target - Ct_Reference) for each sample.

Then, calculate ddCt by subtracting the dCt of the relevant control ('siNT') from the dCt of the treated samples ('siRRBP1'). Note that there are different concentrations (0.5, 1, 1.5), so match 'siRRBP1 0.5' with 'siNT 0.5' as its control, and so on.

Calculate and print the final 2^-ddCt Fold Change for the treated samples."