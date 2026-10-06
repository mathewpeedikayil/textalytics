import csv
from pathlib import Path

data_dir = Path("data")
text_file_names = ["amazon_cells_labelled.txt", "imdb_labelled.txt", "yelp_labelled.txt"]
for text_file_name in text_file_names:
    csv_file_name = text_file_name.replace(".txt", ".csv")
    txt_path = data_dir / text_file_name
    csv_path = data_dir / csv_file_name
    with open(txt_path, "r", encoding="utf-8") as txt_file, open(csv_path, "w", newline="", encoding="utf-8") as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(["text", "label"])
        for line in txt_file:
            text, label = line.strip().split("\t")
            csv_writer.writerow([text, label])


combined_csv_file_name = data_dir / "combined.csv"
with open(combined_csv_file_name, "w", newline="", encoding="utf-8") as combined_csv_file:
    csv_writer = csv.writer(combined_csv_file)
    csv_writer.writerow(["text", "label"])
    for text_file_name in text_file_names:
        csv_file_name = text_file_name.replace(".txt", ".csv")
        with open(data_dir / csv_file_name, "r", encoding="utf-8") as csv_file:
            csv_reader = csv.reader(csv_file)
            next(csv_reader)  # Skip header
            for row in csv_reader:
                csv_writer.writerow(row)