'''

Read the readme.txt and extract the full text representations of each table tab
This reduces the model to only having one attribute per content element

'''


class Preprocess():
    def __init__(self, filePath = './content_transfer_data/readme.txt'):
        self.filePath = filePath
        self._getEntityDatabase()
        
    
    def _getEntityDatabase(self):
        # Grabs data from the readme.txt
        readMeFile = open(self.filePath,'r')

        self.EntityDatabase = dict()

        relevantLines = readMeFile.readlines()[7:]

        for line in relevantLines:
            if not '-' in line:
                continue
            data = [val.strip() for val in line.split(' ',2)]
            self.EntityDatabase[data[0]] = data[2]

    def getValueOfEntity(self, entity, value):
        # Replaces the 
        descriptionOfEntity = self.EntityDatabase[entity]
        if 'Player' in descriptionOfEntity:
            return descriptionOfEntity.replace('Player', value)
        elif 'Team' in descriptionOfEntity:
            return descriptionOfEntity.replace('Team', value)
        else:
            raise('ValueError: Player or Team not found in Database')

if __name__ == '__main__':
    p = Preprocess()
    print p.getValueOfEntity('TEAM-LOSSES', 'Atlanta_Hawks')
