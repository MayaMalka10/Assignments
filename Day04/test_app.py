import pandas as pd
from app import calculate_qpcr_from_df

def test_calculate_qpcr_valid_data():
    """בדיקה שהחישוב המתמטי של dCt, ddCt ו-Fold Change עובד במדויק"""
    # יצירת טבלת נתונים מדומה עם מספרים עגולים שקל לוודא
    sample_data = pd.DataFrame({
        'Sample Name': [
            'siNT 0.5', 'siNT 0.5',
            'siRRBP1 0.5', 'siRRBP1 0.5',
            'siNT 1', 'siNT 1',
            'siRRBP1 1', 'siRRBP1 1'
        ],
        'Target Name': [
            'RRBP1', 'GAPDH',
            'RRBP1', 'GAPDH',
            'RRBP1', 'GAPDH',
            'RRBP1', 'GAPDH'
        ],
        'Ct Mean': [
            25.0, 15.0,  # dCt = 10.0 (ביקורת)
            26.0, 15.0,  # dCt = 11.0 -> ddCt = 1.0 -> Fold Change = 0.5 (ירידה פי 2)
            24.0, 14.0,  # dCt = 10.0 (ביקורת)
            23.0, 14.0   # dCt = 9.0  -> ddCt = -1.0 -> Fold Change = 2.0 (עלייה פי 2)
        ]
    })

    result_df, error = calculate_qpcr_from_df(sample_data)

    # וידוא שלא חזרה שגיאה ושקיבלנו 4 שורות
    assert error is None
    assert len(result_df) == 4

    # בדיקת שורת הביקורת (חייבת להיות 1.0)
    control_row = result_df[result_df['Sample Name'] == 'siNT 0.5'].iloc[0]
    assert control_row['Fold_Change'] == 1.0

    # בדיקת דגימת טיפול 0.5 (ירידה בביטוי)
    treated_05 = result_df[result_df['Sample Name'] == 'siRRBP1 0.5'].iloc[0]
    assert treated_05['dCt'] == 11.0
    assert treated_05['ddCt'] == 1.0
    assert treated_05['Fold_Change'] == 0.5

    # בדיקת דגימת טיפול 1 (עלייה בביטוי)
    treated_1 = result_df[result_df['Sample Name'] == 'siRRBP1 1'].iloc[0]
    assert treated_1['dCt'] == 9.0
    assert treated_1['ddCt'] == -1.0
    assert treated_1['Fold_Change'] == 2.0


def test_calculate_qpcr_missing_column():
    """בדיקה שהפונקציה מחזירה הודעת שגיאה מסודרת כשחסרה עמודת Ct Mean"""
    bad_data = pd.DataFrame({
        'Sample Name': ['siNT 0.5'],
        'Target Name': ['RRBP1']
    })

    result_df, error = calculate_qpcr_from_df(bad_data)

    assert result_df is None
    assert error is not None


def test_calculate_qpcr_missing_target_gene():
    """בדיקה שהפונקציה מטפלת כראוי במקרה שחסר גן המטרה RRBP1"""
    incomplete_gene_data = pd.DataFrame({
        'Sample Name': ['siNT 0.5', 'siRRBP1 0.5'],
        'Target Name': ['GAPDH', 'GAPDH'],
        'Ct Mean': [15.0, 15.0]
    })

    result_df, error = calculate_qpcr_from_df(incomplete_gene_data)

    assert result_df is None
    assert error is not None