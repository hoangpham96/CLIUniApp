from Utils import *

import json
import os

class Database:
    #Check if datafile exists
    def check(self) -> None:
        return os.path.exists(DATA_FILENAME)

    #Create datafile
    def create(self) -> None:
        with open(DATA_FILENAME,'w') as handler:
            handler.write("")
            handler.close()

    #Read datafile. Since file is in JSON format, result will be returned in List of Dictionaries format
    def read(self) -> any:
        result = []

        with open(DATA_FILENAME,'r') as handler:
            result = json.load(handler)
            handler.close()

        return result

    #Update datafile. Expects data in List of Dictionaries format
    def update(self, data) -> None:
        with open(DATA_FILENAME,'w') as handler:
            json.dump(data,handler,indent="\t")
            handler.close()

    #Delete datafile
    def delete(self) -> None:
        if self.check():
            os.remove(DATA_FILENAME)