# Load the three modules:
from irlib.preprocessor import Preprocessor
from irlib.matrix import Matrix
from irlib.metrics import Metrics
import difflib

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
def getClosestQuery(query, number_of_closest_docs):
    print query
    terms = query.split(' ')
    q_vector = mx.query_to_vector(terms, frequency=True)
    print q_vector
    # the smallest 20 documents away from the target with key being the distance they are away
    smallest_n_distance_away_documents = dict()
    minDistance = metric.euclid_vectors(mx.docs[0]['terms'], q_vector)
    distSet = set()
    count = 0
    for doc in mx.docs[:number_of_closest_docs]:
        count += 1
        distance = metric.euclid_vectors(doc['terms'], q_vector)
        distSet.add(distance)
        if distance in smallest_n_distance_away_documents.keys():
            smallest_n_distance_away_documents[distance].append(doc['id'])
        else:
            smallest_n_distance_away_documents[distance] = [doc['id']]
        if distance > minDistance:
            minDistance = distance
    for doc in mx.docs[number_of_closest_docs:]:
        distance = metric.euclid_vectors(doc['terms'], q_vector)
        if distance in smallest_n_distance_away_documents.keys():
            smallest_n_distance_away_documents[distance].append(doc['id'])
            if len(smallest_n_distance_away_documents[minDistance]) > 1:
                smallest_n_distance_away_documents[minDistance].pop()
            else:
                smallest_n_distance_away_documents.pop(minDistance)
                minDistance = max(smallest_n_distance_away_documents.keys())            
        else:
            if distance < minDistance:
                if len(smallest_n_distance_away_documents[minDistance]) > 1:
                    smallest_n_distance_away_documents[minDistance].pop()
                else:
                    smallest_n_distance_away_documents.pop(minDistance)
                    minDistance = max(smallest_n_distance_away_documents.keys())
                smallest_n_distance_away_documents[distance] = [doc['id']]
    
#    for doc in mx.docs:
#        distance = metric.euclid_vectors(doc['terms'], q_vector)
#        if distance < minDistance:
#            minDistance = distance
#            smallDistDoc = [doc['id']]
#        elif distance == minDistance:
#            smallDistDoc.append(doc['id'])
    return smallest_n_distance_away_documents

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

def getSentencesFromLineNumbersDict(distancesDict, fileName):
    for distance in distancesDict.keys():
        lineNumbers = distancesDict[distance]
        sentences = []
        for line in lineNumbers:
            sentences.append(getLineFromFile(fileName, int(line)))
        distancesDict[distance] = sentences
    return distancesDict

def printOutDistanceDict(distancesDict):
    # Prints out Closest Valuess
    print 'OPTIONS: \n'
    count = 1
    print sorted(distancesDict)
    for distance in sorted(distancesDict):
        for sentence in distancesDict[distance]:
            print 'Distance: ' + str(distance)
            print str(count) + '. ' + sentence + '\n'
            count += 1    

def normalizeArray(arr):
    return [float(i)/sum(arr) for i in arr]

def normalizeMatrix(matrix):
    return [normalizeArray(row) for row in matrix]

def calculateDifferenceScore(w1, w2):
    score = 1
    for i,s in enumerate(difflib.ndiff(w1,w2)):
        if s[0]==' ': continue
        elif s[0]=='-' or s[0]=='+':
            score+=2
    return 1/float(score)

def getDistributionBetweenSentences(sent1, sent2):
    IR_Matrix = []
    for word1 in sent1.split():
        word_distribution = []
        for word2 in sent2.split():
            word_distribution += [calculateDifferenceScore(word1, word2)]
        IR_Matrix += [word_distribution]
    return normalizeMatrix(IR_Matrix)

   

def main():
    # Load the data from the training data
    loadMatrix()
    
    # This grabs the row at line 150 in the table row and corresponding sentence from the files
    line_number_input = 1
    fileName = './content_transfer_data/roto-sent-data.valid.src'
    untrimmed_row = getLineFromFile(fileName, line_number_input)
    
    
    # Takes out row headings for use in IR
    row_tags = ' '.join(getTagOrder(untrimmed_row))

    # Get line numbers for other similar sentences in the database
    number_of_closest_docs = 20
    distancesDict = getClosestQuery(row_tags, number_of_closest_docs)
    fileName = './content_transfer_data/roto-sent-data.train.tgt'
    srcFileName = './content_transfer_data/roto-sent-data.train.src'
    getSentencesFromLineNumbersDict(distancesDict, fileName,srcFileName)
     

    # Print out data
    
    # Prints out target data
    fileName = './content_transfer_data/roto-sent-data.valid.tgt'
    tgt_sentence = getLineFromFile(fileName, line_number_input)

    print 'SOURCE SENTENCE: \n' + tgt_sentence +'\n'
    
    # Print out closest Values
    printOutDistanceDict(distancesDict)

def getLine():
    fileName = './content_transfer_data/roto-sent-data.valid.src'
    f1 = open('./content_transfer_data/roto-sent-data.test.src','r')
    f2 = open('./content_transfer_data/roto-sent-data.test.tgt','r')
    wr = open('./content_transfer_data/attentionOutput.txt','w')
    for line in f.readlines():
        trimmed_line = ' '.join(getTagOrder(line))
        wr.write(str(getDistributionBetweenSentences(trimmed_line.strip(),tgt_row.strip()))+'\n')
    

if __name__ == "__main__":
    #main()
    getLine()
