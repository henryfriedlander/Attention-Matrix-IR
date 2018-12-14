'''

Create a continuous vector embedding for the table attributes and content fields

'''

from preprocess import Preprocess
import tensorflow as tf



word_ids = tf.get_variable("word_ids")

word_embeddings = tf.get_variable('word_embeddings',
    [vocabulary_size, embedding_size])
embedded_word_ids = tf.gather(word_embeddings, word_ids)


if __name__ == '__main__':
    p = Preprocess()
    print p.getValueOfEntity('TEAM-LOSSES', 'Atlanta_Hawks')
