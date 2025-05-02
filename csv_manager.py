import csv


class CSVManager:
    def __init__(self, in_file, out_file):
        self.in_file = in_file
        self.out_file = out_file

    def read_links(self):
        """Читает ссылки из CSV-файла"""
        links = []
        with open(self.in_file, mode='r', encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                links.append(row["link"])
        return links

    def save_headers(self, data, headers):
        with open(self.out_file, mode='a', encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=headers)
            if file.tell() == 0:
                writer.writeheader()
            writer.writerows(data)

    def save_row(self, data):
        headers = [
            "price", "date", "geo_lat", "geo_lon",
            "region", "building_type", "level", "levels",
            "rooms", "area", "kitchen_area", "object_type"
        ]

        try:
            with open(self.out_file, mode="a", encoding="utf-8", newline='') as file:
                writer = csv.DictWriter(file, fieldnames=headers)
                if file.tell() == 0:
                    writer.writeheader()
                writer.writerow(data)
        except Exception as e:
            print(f'Ошибка сохранения строки в {self.out_file}: {e}')

    def save_new_links(self, data):
        """Сохраняет собранные ссылки в CSV-файл"""
        with open(self.in_file, mode="a", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=["title", "price", "link"])
            if file.tell() == 0:  # Если файл пустой, записываем заголовки
                writer.writeheader()
            writer.writerows(data)
