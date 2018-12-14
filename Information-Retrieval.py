# Load the three modules:
from irlib.preprocessor import Preprocessor
from irlib.matrix import Matrix
from irlib.metrics import Metrics

# Create instances for their classes:
prep = Preprocessor()
mx = Matrix()
metric = Metrics()
q_vector=[]

def generateMatrix():
    fd = open('./content_transfer_data/roto-sent-data.train-ONLYTAGS.src','r')
    count = 1
    for line in fd.readlines():
        terms = line.split(' ')
        terms = [x.strip() for x in terms]
        mx.add_doc( doc_id=str(count),
                    doc_terms=terms,
                    frequency=True,
                    do_padding=True)

        count += 1
        if count % 1000 == 0:
            print count

    mx.dump('IRmatrix.train.src.csv', delimiter='\t', header=True)

def loadMatrix():
    mx.load('IRmatrix.train.src.csv', delimiter='\t')
#we will get a list of the same objects. Their vector representation will be the same so differentiate

# TODO create a list of all of the sentences with the smallest distance away
def getClosestQuery(query):
    print query
    terms = query.split(' ')
    print terms
    q_vector = mx.query_to_vector(terms, frequency=True)
    print q_vector
    print len(mx.docs)
    smallDistDoc = []
    minDistance = metric.euclid_vectors(mx.docs[0]['terms'], q_vector)
    for doc in mx.docs:
        distance = metric.euclid_vectors(doc['terms'], q_vector)
        if distance < minDistance:
            minDistance = distance
            smallDistDoc = [doc['id']]
        elif distance == minDistance:
            smallDistDoc.append(doc['id'])
    print '\nSmallest Distance of ' + str(minDistance)
    print type(smallDistDoc)
    print smallDistDoc
    return smallDistDoc

def getLineFromFile(fileName, lineNumber):
    fd = open(fileName,'r')
    for i in xrange(lineNumber-1):
        fd.next()
    return fd.next()

def getTagOrder(line, index=1):
    tags = []
    table_rows = line.split()
    for row in table_rows:
        tags.append(row.split('|')[index])

    return tags

def main():
    # Load the data from the training data
    loadMatrix()
    
    # This grabs the row at line 150 in the table row and corresponding sentence from the files
    line_number_input = 200
    fileName = './content_transfer_data/roto-sent-data.valid.src'
    untrimmed_row = getLineFromFile(fileName, line_number_input)
    fileName = './content_transfer_data/roto-sent-data.valid.tgt'
    tgt_sentence = getLineFromFile(fileName, line_number_input)
    
    
    # Takes out row headings for use in IR
    row_tags = ' '.join(getTagOrder(untrimmed_row))

    # Get line numbers for other similar sentences in the database
    IR_line_numbers = getClosestQuery(row_tags)

    fileName = './content_transfer_data/roto-sent-data.train.tgt'
    sentence_structures = [getLineFromFile(fileName, int(IR_line)) for IR_line in IR_line_numbers]

    # Print out data

    print 'SOURCE SENTENCE: \n' + tgt_sentence +'\n'


    print 'OPTIONS: \n'
    for i in xrange(len(sentence_structures)):
        print str(i+1) + '. ' + sentence_structures[i]

if __name__ == "__main__":
    main()
