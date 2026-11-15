from flask import Flask, render_template, request
import pandas as pd
import os

app = Flask(__name__)

# פונקציה שמקבלת את טבלת הנתונים (DataFrame) ומבצעת את החישוב
def calculate_qpcr_from_df(df):
    try:
        # קריאת העמודות הרלוונטיות בלבד
        df = df[['Sample Name', 'Target Name', 'Ct Mean']]

        pivot_df = df.pivot(index='Sample Name', columns='Target Name', values='Ct Mean').reset_index()

        pivot_df['dCt'] = pivot_df['RRBP1'] - pivot_df['GAPDH']
        pivot_df[['Condition', 'Concentration']] = pivot_df['Sample Name'].str.split(' ', expand=True)

        control_df = pivot_df[pivot_df['Condition'] == 'siNT'][['Concentration', 'dCt']].rename(columns={'dCt': 'Control_dCt'})

        result_df = pd.merge(pivot_df, control_df, on='Concentration', how='left')
        result_df['ddCt'] = result_df['dCt'] - result_df['Control_dCt']
        result_df['Fold_Change'] = 2 ** (-result_df['ddCt'])

        final_df = result_df[['Sample Name', 'RRBP1', 'GAPDH', 'dCt', 'ddCt', 'Fold_Change']].copy()
        final_df.rename(columns={'RRBP1': 'Ct_Target (RRBP1)', 'GAPDH': 'Ct_Ref (GAPDH)'}, inplace=True)

        return final_df.round(4), None
    except Exception as e:
        return None, "Error processing the file. Please ensure columns match the required format."

@app.route('/', methods=['GET', 'POST'])
def home():
    results_list = None
    error_message = None

    # אם המשתמש לחץ על אחד הכפתורים
    if request.method == 'POST':

        # אם המשתמש העלה קובץ משלו
        if 'upload_file' in request.form:
            file = request.files.get('file')
            if file and file.filename != '':
                try:
                    df = pd.read_excel(file)
                    df_result, error_message = calculate_qpcr_from_df(df)
                    if df_result is not None:
                        results_list = df_result.to_dict(orient='records')
                except Exception as e:
                    error_message = "Could not read the uploaded Excel file."
            else:
                error_message = "No file selected."

        # אם המשתמש לחץ על כפתור קובץ הדוגמה
        elif 'load_example' in request.form:
            try:
                # יצירת נתיב יציב לקובץ הדוגמה שנמצא באותה תיקייה של app.py
                base_dir = os.path.dirname(os.path.abspath(__file__))
                file_path = os.path.join(base_dir, "EXP.30 Results.xlsx")

                df = pd.read_excel(file_path)
                df_result, error_message = calculate_qpcr_from_df(df)
                if df_result is not None:
                    results_list = df_result.to_dict(orient='records')
            except Exception as e:
                error_message = f"Error loading example file: {str(e)}"

    return render_template('index.html', results=results_list, error_message=error_message)

if __name__ == '__main__':
    app.run(debug=True)