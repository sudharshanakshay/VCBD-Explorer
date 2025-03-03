import pandas as pd

path_to_verizon_file = "C:/Users/sudharshan.acharya/Downloads/vcdb/vcdb.csv"
path_to_verizon_file = "/home/ohmkar/Downloads/vcdb.csv"

class Verizon:
    def __init__(self):
        try:
            self.verizon_df = pd.read_csv(path_to_verizon_file)
        except:
            self.verizon_df = pd.read_excel(path_to_verizon_file)
        

    def start(self):
        print("verizon, start.")

        header_split = []
        header_with_single_statement = []
        header_second_statement = []

        for header in self.verizon_df.columns.to_list():
            header_split.append(header.split('.'))
        
        for header_list in header_split:
            if(len(header_list) == 1):
                header_with_single_statement.append(header_list[0])
            if(len(header_list) >= 2 and header_list[1] not in header_second_statement):
                header_second_statement.append(header_list[1])


        print(f'[+] headers with single statement: {header_with_single_statement}')

        print()
        print(f'[+] header second phase: {header_second_statement}')


        # print(self.verizon_df.columns.to_list())

obj = Verizon()
obj.start()