import os
import copy
from fuzzywuzzy import fuzz
from prettytable import PrettyTable
from datetime import datetime
from uuid import uuid4

"""
Datas :

	fomat : { 
		id : int
		filename : str , 
		name : str , 
		price : float , 
		selected : bool 
		}

	main data : 
		- id 
		- file location
		- name
		- price
		- selected

	Additional Data :
		- persons
		- items
		- electric
		- water 
"""


class CottageDataManagement:
    __data: list[dict, ...] = []
    directory = "Cottage Pictures"

    def __init__(self, splitter=","):
        self.__load_data(splitter)

    @property
    def data(self):
        return self.__data

    def __load_data(self, splitter: str):
        os.makedirs(self.directory, exist_ok=True)
        for num, file in enumerate(os.listdir(self.directory)):
            filename: str = os.path.splitext(file)[0]
            try:
                float(filename.split(splitter)[1])
            except ValueError:
                continue

            self.__data.append(
                {
                    "id": num,
                    "filename": os.path.join(self.directory, file),
                    "name": filename.split(splitter)[0],
                    "price": float(filename.split(splitter)[1]),
                    "selected": False
                }
            )

    # ------> Reading Data
    def get_all_data(self) -> iter:
        for item in self.__data:
            yield copy.copy(item)

    def get_selected_data(self) -> iter:
        for item in self.__data:
            if item["selected"]:
                yield copy.copy(item)

    # ------> Writing Data
    def select_item(self, item_id: int):
        for item in self.__data:
            if item["id"] == int(item_id):
                item["selected"] = True
                break
        else:
            raise ValueError(f"[ ! ] {item_id} id does not exist in data")

    def unselect_item(self, item_id: int):
        for item in self.__data:
            if item["id"] == int(item_id):
                item["selected"] = False
                break
        else:
            raise ValueError(f"[ ! ] {item_id} id does not exist in data")

    def search(self, find : str  , rate = 70 , state = 'all' ) -> iter :
        found = []
        for data in self.get_all_data():
            rating = []
            for key , values in data :
                if fuzz.WRatio( str(values) , find ) > rate :
                    rating.append( fuzz.WRatio( str(values) , find ))
            found.append( ( max(rating) , data['id'] ))

        found.sort(key=lambda x: x[0], reverse=True)
        if state == 'all' :
            for data in self.get_all_data() :
                if data['id'] in found :
                    yield data
        elif state == 'selected' :
            for data in self.get_all_data():
                if data['id'] in found and data['selected'] :
                    yield data
        else :
            for data in self.get_all_data():
                if data['id'] in found and not data['selected'] :
                    yield data

def createReciept(person : float , items : float , electric : float , water : float , price : float, total : float , filename = None ) :
    """ Used to create a reciept """
    table = PrettyTable(["Tags" , "Cost"])
    table.add_row(["Persons" , f"{person:.0f}"])
    table.add_row(["Items" , f"${items:.2f}"])
    table.add_row(["Electricity" , f"${electric:.2f}"])
    table.add_row(["Water", f"${water:.2f}"])
    table.add_row(["Price", f"${price:.2f}"])
    table.add_row(["Total" , f"${total:.2f}" ])

    if not filename :
        filename = datetime.now().strftime(f"TIME = %m-%d-%Y, %H-%M-%S [ FOOD ID = {str(uuid4().hex)[:10]} ].txt")

    with open(os.path.join("reciepts folder" , filename) , 'w') as file :
        file.write("Cottage Reciept : \n")
        file.write(table.get_string())

    os.system(f'notepad.exe {os.path.join("reciepts folder", filename)}')

if __name__ == '__main__':
    print('fd'.lower())