

def getTagOrder(line, index=1):
    tags = []
    table_rows = line.split()
    for row in table_rows:
        tags.append(row.split('|')[index])

    return tags


file = open('./content_transfer_data/roto-sent-data.valid.src','r')
tagFile = open('./content_transfer_data/roto-sent-data.valid-ONLYTAGSTOY.src','w')

lines = file.readlines()

for line in lines[:20]:
    tagFile.write(' '.join(getTagOrder(line))+'\n')

file.close()
tagFile.close()
