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
toc_titles = [
    "OFFICE OF THE REGISTRAR",
    "STUDENT CLASSES",
    "FULL-TIME STUDENTS",
    "PART-TIME STUDENTS",
    "SPECIAL STUDENTS OR NON-DEGREE STUDENTS",
    "TRANSFER STUDENTS",
    "UNDERGRADUATE FRESHMAN TRANSFER POLICY",
    "STUDENT EXCHANGE PROGRAM",
    "CREDIT TRANSFER FOR EXCHANGE STUDENTS",
    "AUDITORS",
    "HOURS OF CLASSES",
    "ATTENDANCE POLICY",
    "EXAMINATIONS AND QUIZZES",
    "FINAL EXAMINATION MAKE-UP",
    "GRADED FINAL EXAMINATION PAPER",
    "FINAL GRADES",
    "TRANSCRIPTS",
    "CHANGE OF GRADE",
    "CHANGE OF PROVISIONAL GRADE",
    "GRADES FOR REPEATED COURSES",
    "GRADES UPON CHANGE OF MAJOR",
    "SYSTEM OF GRADES",
    "GRADE POINT AVERAGE",
    "ACADEMIC STANDING",
    "ACADEMIC RECOGNITION",
    "ACADEMIC MISCONDUCT",
    "CHANGE OF MAJOR",
    "GRADUATION REQUIREMENTS",
    "TEACHING DIPLOMA REQUIREMENTS",
    "CONFERRING OF DEGREES",
    "REPLACEMENT DIPLOMA",
    "RESIDENCY REQUIREMENTS",
    "PARTICIPATION IN COMMENCEMENT EXERCISES",
    "COURSE DESIGNATION",
    "UNDERGRADUATE REGISTRATION",
    "REGISTRATION ELIGIBILITY",
    "REGISTRATION IN ABSTENTIA",
    "LATE REGISTRATION",
    "CROSS-REGISTRATION",
    "EXCHANGE STUDENTS REGISTRATION",
    "OUTGOING EXCHANGE STUDENTS",
    "INCOMING EXCHANGE STUDENTS",
    "IMPROPER REGISTRATION",
    "CHANGES IN REGISTRATION",
    "ADDING AND/OR DROPPING COURSES",
    "WITHDRAWAL FROM COURSES",
    "ATTENDANCE AFTER WITHDRAWING",
    "STUDENT REINSTATEMENT",
    "DROPPING A COURSE WHILE ON PROBATION",
    "REGISTRATION IN A COURSE WITH AN ”I” GRADE",
    "STUDENT ACADEMIC LOAD",
    "TUITION AND FEES",
    "UNDERGRADUATE ACADEMIC MINORS",
    "RATIONALE",
    "GENERAL RULES AND REGULATIONS FOR MINORS AT NDU",
    "SELF-DESIGNED INTERDISCIPLINARY MINORS"
]

split_txt_by_titles(
    input_path="/Users/walid/Desktop/Senior_Project/input.txt",
    output_dir="/Users/walid/Desktop/Senior_Project/Registrar",
    toc_titles=toc_titles
)
