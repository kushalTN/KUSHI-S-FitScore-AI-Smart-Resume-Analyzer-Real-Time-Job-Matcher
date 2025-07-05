from fpdf import FPDF
import csv
import os

# PDF Report Generation
def generate_pdf_report(filename, matched_skills, missing_skills, tfidf_score, bert_score, save_path=None):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, f"Resume Analysis Report: {filename}", ln=True, align='C')
    pdf.ln(10)

    pdf.cell(200, 10, f"TF-IDF Matching Score: {tfidf_score:.2f}%", ln=True)
    pdf.cell(200, 10, f"BERT Similarity Score: {bert_score:.2f}%", ln=True)
    pdf.ln(5)

    pdf.cell(200, 10, "Matched Skills:", ln=True)
    pdf.multi_cell(0, 10, ", ".join(matched_skills) if matched_skills else "None")

    pdf.ln(5)
    pdf.cell(200, 10, "Missing Skills:", ln=True)
    pdf.multi_cell(0, 10, ", ".join(missing_skills) if missing_skills else "None")

    # Set default save path if not provided
    if not save_path:
        save_path = f"data/reports/{filename}_analysis_report.pdf"
    
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    pdf.output(save_path)

    return save_path


# CSV Report Generation
def generate_csv_report(filename, matched_skills, missing_skills, tfidf_score, bert_score, save_path=None):
    if not save_path:
        save_path = f"data/reports/{filename}_analysis_report.csv"

    os.makedirs(os.path.dirname(save_path), exist_ok=True)

    with open(save_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Resume File", filename])
        writer.writerow(["TF-IDF Matching Score (%)", f"{tfidf_score:.2f}"])
        writer.writerow(["BERT Similarity (%)", f"{bert_score:.2f}"])
        writer.writerow([])
        writer.writerow(["Matched Skills"] + (matched_skills if matched_skills else ["None"]))
        writer.writerow(["Missing Skills"] + (missing_skills if missing_skills else ["None"]))

    return save_path
