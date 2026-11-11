from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)

def calculate_qpcr():
    # קריאת הקובץ - רק העמודות הרלוונטיות
    df = pd.read_excel("EXP.30 Results.xlsx", usecols=['Sample Name', 'Target Name', 'Ct Mean'])
    
    # סידור הנתונים כך שגן המטרה וגן הרפרנס יהיו באותה שורה עבור כל דגימה
    pivot_df = df.pivot(index='Sample Name', columns='Target Name', values='Ct Mean').reset_index()
    
    # (Target - Reference) dCt חישוב
    pivot_df['dCt'] = pivot_df['RRBP1'] - pivot_df['GAPDH']
    
    # חלוקת שם הדגימה למצב (NT/RRBP1) ולריכוז (0.5/1/1.5) כדי שנוכל להתאים ביקורת לטיפול
    pivot_df[['Condition', 'Concentration']] = pivot_df['Sample Name'].str.split(' ', expand=True)
    
    # חילוץ ערכי הביקורת (siNT)
    control_df = pivot_df[pivot_df['Condition'] == 'siNT'][['Concentration', 'dCt']].rename(columns={'dCt': 'Control_dCt'})
    
    # מיזוג ערכי הביקורת חזרה לטבלה המרכזית לפי הריכוז המתאים
    result_df = pd.merge(pivot_df, control_df, on='Concentration', how='left')
    
    # Fold Change (2^-ddCt) -ו ddCt חישוב
    result_df['ddCt'] = result_df['dCt'] - result_df['Control_dCt']
    result_df['Fold_Change'] = 2 ** (-result_df['ddCt'])
    
    # סידור העמודות הסופיות ועיגול ל-4 ספרות אחרי הנקודה
    final_df = result_df[['Sample Name', 'RRBP1', 'GAPDH', 'dCt', 'ddCt', 'Fold_Change']].copy()
    final_df.rename(columns={'RRBP1': 'Ct_Target (RRBP1)', 'GAPDH': 'Ct_Ref (GAPDH)'}, inplace=True)
    
    return final_df.round(4)

@app.route('/')
def home():
    # קריאה לפונקציית החישוב
    results_df = calculate_qpcr()
    
    # המרת טבלת הפנדס לרשימת מילונים כדי שה-HTML יוכל לקרוא אותה
    results_list = results_df.to_dict(orient='records')
    
    # שליחת התוצאות לדף האינטרנט
    return render_template('index.html', results=results_list)

if __name__ == '__main__':
    app.run(debug=True)