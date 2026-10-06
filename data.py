import csv

text_file_names = ["amazon_cells_labelled.txt", "imdb_labelled.txt", "yelp_labelled.txt"]
for text_file_name in text_file_names:
    csv_file_name = text_file_name.replace(".txt", ".csv")
    with open(text_file_name, "r", encoding="utf-8") as txt_file, open(csv_file_name, "w", newline="", encoding="utf-8") as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(["text", "label"])
        for line in txt_file:
            text, label = line.strip().split("\t")
            csv_writer.writerow([text, label])


combined_csv_file_name = "combined.csv"
with open(combined_csv_file_name, "w", newline="", encoding="utf-8") as combined_csv_file:
    csv_writer = csv.writer(combined_csv_file)
    csv_writer.writerow(["text", "label"])
    for text_file_name in text_file_names:
        csv_file_name = text_file_name.replace(".txt", ".csv")
        with open(csv_file_name, "r", encoding="utf-8") as csv_file:
            csv_reader = csv.reader(csv_file)
            next(csv_reader)  # Skip header
            for row in csv_reader:
                csv_writer.writerow(row)