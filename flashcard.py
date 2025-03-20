import json
import docx

# Mở file Word
file_path = "docfile/flashcard.docx"
doc = docx.Document(file_path)

# Biến lưu trữ dữ liệu
data = {}
category = None  # Lưu chủ đề hiện tại

# Đọc từng dòng trong file Word
for para in doc.paragraphs:
    text = para.text.strip()
    if not text:
        continue

    # Nếu là tiêu đề danh mục (có số thứ tự đầu dòng)
    if text[0].isdigit() and "." in text:
        category = text.split(".", 1)[1].strip()
        data[category] = []
    elif " – " in text:
        word, meaning = text.split(" – ", 1)
        if category:
            data[category].append({"word": word.strip(), "meaning": meaning.strip()})

# Lưu dữ liệu thành file JSON
output_json = "docfile/flashcards.json"
with open(output_json, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

