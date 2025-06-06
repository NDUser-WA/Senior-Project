import os
import re

def split_txt_by_titles(input_path, output_dir, toc_titles):
    os.makedirs(output_dir, exist_ok=True)

    with open(input_path, 'r', encoding='utf-8') as f:
        full_text = f.read()

    # Normalize newlines
    full_text = full_text.replace('\r\n', '\n')

    # Escape and join titles for regex, match start of line and whole line for title
    pattern = '|'.join(re.escape(title) for title in toc_titles)

    # Split text on titles, keeping titles with lookahead
    sections = re.split(f'(?=^({pattern})\\s*$)', full_text, flags=re.MULTILINE)

    i = 1
    section_num = 1
    while i < len(sections):
        title = sections[i].strip()
        content = sections[i + 1] if i + 1 < len(sections) else ''
        safe_title = re.sub(r'[^a-zA-Z0-9]+', '_', title).strip('_').lower()
        
        filename = f"{section_num:02d}_{safe_title}.txt"
        file_path = os.path.join(output_dir, filename)

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(title + '\n' + content.lstrip(title).strip())

        print(f"✅ Saved: {file_path}")
        i += 2
        section_num += 1

# TOC titles WITHOUT page numbers, in correct order:
toc_titles = [ "OFFICE OF ADMISSIONS",
              "UNDERGRADUATE ADMISSION",
                "FRESHMAN ADMISSION REQUIREMENTS"
                ,"SOPHOMORE AND FIRST-YEAR ADMISSION REQUIREMENTS",
                "TRANSFER ADMISSION REQUIREMENTS",
                "ADMISSION REQUIREMENTS FOR SECOND DEGREE SEEKERS"
                ,"ADMISSION REQUIREMENTS FOR SPECIAL STUDENTS",
                "ADMISSION REQUIREMENTS FOR AUDITORS"
                ,"ADMISSION REQUIREMENTS FOR TEACHING DIPLOMA",
                "ADMISSION REQUIREMENTS FOR UNIVERSITY EMPLOYEES",
                "ADMISSION REQUIREMENTS FOR FRENCH, INTERNATIONAL, AND LEBANESE BACCALAUREATE STUDENTS",
                "ENGLISH PROFICIENCY REQUIREMENTS",
                "GENERAL ADMISSION REQUIREMENTS",
                "TRANSFER: RAMEZ G. CHAGOURY FACULTY OF ARCHITECTURE, ARTS AND DESIGN (FAAD)",
                "TRANSFER: FACULTY OF ENGINEERING (FE)","REMEDIAL COURSE REQUIREMENTS BY FACULTY AND MAJOR"
]

split_txt_by_titles(
    input_path="/Users/walid/Desktop/Senior_Project/inputAdmissions.txt",
    output_dir="/Users/walid/Desktop/Senior_Project/Admissions",
    toc_titles=toc_titles
)
