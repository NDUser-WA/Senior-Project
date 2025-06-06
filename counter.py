import os

def count_words(text):
    return len(text.split())

def find_files_to_rechunk(folder_path, word_limit=300):
    files_to_rechunk = []

    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            full_path = os.path.join(folder_path, filename)
            try:
                with open(full_path, "r", encoding="utf-8") as f:
                    text = f.read()
                    word_count = count_words(text)
                    if word_count >= word_limit:
                        files_to_rechunk.append((filename, word_count))
            except Exception as e:
                print(f"❌ Error reading {filename}: {e}")

    return files_to_rechunk

# === USAGE ===
if __name__ == "__main__":
    folder = "/Users/walid/Desktop/Senior_Project/Registrar"  # Update this
    threshold = 300  # You can adjust this number
    long_files = find_files_to_rechunk(folder, threshold)

    if long_files:
        print(f"\n📄 Files exceeding {threshold} words:")
        for fname, count in long_files:
            print(f"- {fname}: {count} words")
    else:
        print("✅ All files are within the acceptable word count.")
