import os
import copy

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

if __name__ == '__main__':
    print('fd'.lower())