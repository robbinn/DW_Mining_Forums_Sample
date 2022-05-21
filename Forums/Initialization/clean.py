import codecs, re, time

def is_unicode(s):
	try:
		str(s)
		return False
	except:
		return True

def contains_num(s):
	nums = range(10)
	str_nums = [str(num) for num in nums]
	char_set = set(s)
	for num in str_nums:
		if num in char_set:
			return True
	return False


from nltk.tokenize import regexp_tokenize, wordpunct_tokenize
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
import string, re
stemmer = SnowballStemmer('english')

word_matcher = re.compile(u'[^\W\d_]+', re.UNICODE)
def is_unicode(s):
	if word_matcher.match(s):
		return True
	return False

def stem_preprocessor(s):
	return my_preprocessor(s, stem=True)

def my_preprocessor(s, stem=False):
	pattern = u'[^\W\d_]+|[^\w\s]+|\d+'
	tokens = regexp_tokenize(s, pattern)
	cleaned_tokens = []
	for token in tokens:
		if token and is_unicode(token) and not token in stopwords.words('english'):
			cleaned_token = stemmer.stem(token.lower()) if stem==True else token.lower()
			cleaned_tokens.append(cleaned_token)

	return ' '.join(cleaned_tokens)


regex = re.compile(u'[%s]' % re.escape(string.punctuation)) #see documentation here: http://docs.python.org/2/library/string.html
def my_preprocessor2(s):
	tokens = wordpunct_tokenize(s)
	cleaned_tokens = [regex.sub(u'', token) for token in tokens]
	return u' '.join(cleaned_tokens)

from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.linear_model import SGDClassifier
from sklearn.pipeline import make_pipeline
from sklearn.cross_validation import train_test_split
from sklearn.metrics import classification_report
from sklearn.neighbors import NearestCentroid
from sklearn.cross_validation import KFold

def KFold_classification_report(clf, docs, labels, K=10):
	y_pred = [-1] * len(docs)
	cv = KFold(len(docs), K, shuffle=True)
	for traincv, testcv in cv:
		train_docs = [docs[i] for i in traincv]
		train_labels = [labels[i] for i in traincv]

		clf.fit(train_docs, train_labels)

		for i in testcv:
			y_pred[i] = clf.predict([docs[i]])[0]
	
	return classification_report(labels, y_pred)

