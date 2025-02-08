import csv
import random

class DatasetWorker:
    
    def __init__(self):
        self.data = []
        self.header = None

    def __str__(self):
        return f"{len(self.data)} items loaded. There is {len(self.header) if self.header else 0} headers."
    
    def input_handler(self):
        pass
    
    def load_data(self, path, has_header=False, delimiter=";"):
        "Reading data from given path. If the has_header parameter is set to True, the first row of the file will be treated as the header."
        "The delimiter should be change depending on the file being read (the default is ;)"

        with open(path, mode='r', newline='') as file:
            reader = csv.reader(file, delimiter=delimiter)
        
            if has_header:
                self.header = list(next(reader))

            self.data = list(reader)

        file.close()
    

    def print_headers(self):
        "Printing the headers from the file"
        if self.header:
            print(self.header)
        else:
            print("There was no header in dataset!")
        
    
    def print_dataset(self, start=0, end=None):
        "Printing the data in rows from given start to end. Default all rows."
        for i in self.data[start:end]:
            print(i)

    def split_dataset(self, train, test, valid):
        "Function split data into three lists - train, test, valid, accordingly to given percentages"
        
        random_data = self.data.copy()
        random.shuffle(random_data)
        data_lenght = len(random_data)

        train_end = int(data_lenght * (train / 100))
        test_end = train_end + int(data_lenght * (test / 100))

        train_list = random_data[:train_end]
        test_list = random_data[train_end:test_end]
        valid_list = random_data[test_end:]

        return train_list, test_list, valid_list

    def count_decision_classes(self, col_num=False):
        "Function that count decision classes in the dataset. If no column number provideded, function count decision classes in every column"
        decision_classes  = []
        try:
            colums_number = len(self.data[0])
        except:
            print("First load data!!!")
            return False

        #prepering list of dicts, each for every column
        for i in range(0,colums_number):
            decision_classes.append({})

        #iteration over every row and every value in row and count
        for row in self.data:
            for i in range(len(row)):
                col_val = row[i]
                decision_classes[i][col_val] = decision_classes[i].get(col_val, 0) + 1

        if col_num:
            print(self.header[col_num] if self.header else col_num, end=" - ")
            print(decision_classes[col_num])
        else:
            for i in range(len(decision_classes)):
                print(self.header[i] if self.header else i, end=" - ")
                print(decision_classes[i])

    def filter_data_with_decision_class(self, class_value, col_num=None):
        "Function return every row that conteins class_value in any column or in given column number - col_num"

        if not col_num:
            data_out = [row for row in self.data if row.count(class_value) > 0]
        else:
            data_out = [row for row in self.data if row[col_num] == class_value]
        return data_out

    def save_to_csv(self, data, file_path):
        "Saving given data to file on given path"
        with open(file_path, 'w') as file:
            writer = csv.writer(file)
            writer.writerows(data)
        file.close()

# Interaktywna konsola
if __name__ == "__main__":
    module = DatasetWorker()
    module.load_data('bank.csv')
    while True:
        print("\n--- Interaktywna konsola ---")
        print("1. Wczytaj dataset")
        print("2. Wypisz etykiety kolumn")
        print("3. Wypisz dane")
        print("4. Podziel dataset")
        print("5. Wypisz liczebność klas decyzyjnych")
        print("6. Filtrowanie danych dla klasy decyzyjnej")
        print("7. Zapisz dane do pliku")
        print("8. Wyjście")

        choice = input("Wybierz opcję: ")

        if choice == "1":
            file_path = input("Podaj ścieżkę do pliku: ")
            has_headers = input("Czy plik zawiera nagłówki? (tak/nie): ").strip().lower() == "tak"
            module.load_data(file_path, has_headers)
            print("Dane zostały wczytane.")
        elif choice == "2":
            module.print_headers()
        elif choice == "3":
            start = input("Podaj początek przedziału (lub pozostaw puste): ")
            end = input("Podaj koniec przedziału (lub pozostaw puste): ")
            start = int(start) if start else None
            end = int(end) if end else None
            module.print_dataset(start, end)
        elif choice == "4":
            train_ratio = float(input("Proporcja zbioru treningowego: "))
            test_ratio = float(input("Proporcja zbioru testowego: "))
            val_ratio = float(input("Proporcja zbioru walidacyjnego: "))
            if train_ratio + test_ratio + val_ratio > 100:
                print("The given percentages add up to more than 100%!!!")
                pass
            else:
                train, test, val = module.split_dataset(train_ratio, test_ratio, val_ratio)
                print("Podział zakończony.")
                print("Liczba danych: Treningowe:", len(train), "Testowe:", len(test), "Walidacyjne:", len(val))
        elif choice == "5":
            column_index = input("Podaj indeks kolumny klasy decyzyjnej: ")
            if column_index > len(module.data[0]):
                print("There is less columns!!!")
                pass
            else:
                class_column_index = int(column_index) if column_index else False
                classes = module.count_decision_classes(class_column_index)
                print("Liczebności klas:", classes)
        elif choice == "6":
            column_index = input("Podaj indeks kolumny klasy decyzyjnej: ")
            if column_index > len(module.data[0]):
                print("There is less columns!!!")
                pass
            else:
                class_column_index = int(column_index) if column_index else None
                class_value = input("Podaj wartość klasy decyzyjnej: ")
                filtered = module.filter_by_class(class_column_index, class_value)
                print("Dane dla klasy '", class_value, "':", filtered)
        elif choice == "7":
            output_file = input("Podaj nazwę pliku do zapisu: ")
            module.save_to_csv(module.data, output_file)
            print("Dane zapisane do pliku", output_file)
        elif choice == "8":
            print("Zakończenie programu.")
            break
        else:
            print("Nieprawidłowa opcja. Spróbuj ponownie.")