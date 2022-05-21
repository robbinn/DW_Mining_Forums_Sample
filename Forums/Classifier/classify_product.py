import pickle, os
from scipy.sparse import hstack, csr_matrix

classifier_map = {

		'sup_english': 'svc.pickle',                                #Supervised
	    'semi_english' : 'classifier_english.pickle',               #Semi-supervised
	    'sup_russian' : 'russian_svm.pickle',                       #Supervised

		}

product_transformer_map = {

	    'sup_english': 'product_transformer.pickle',                #Supervised
	    'semi_english' : 'title_english.pickle',                    #Semi-supervised
    	'sup_russian' : 'russian_title.pickle',                     #Supervised

		}

description_transformer_map = {

		'sup_english': 'descriptions_transformer.pickle',           #Supervised
	    'semi_english' : 'descriptions_english.pickle',             #Semi-supervised
	    'sup_russian' : 'russian_desc.pickle',                      #Supervised

		}

transformers_path = '..\Classifier'
classifiers_path = '..\Classifier'

class Classifier(object):
	def __init__(self, language = 'sup_english'):
		self.update_language(language)

	def update_language(self, language):
		self.language = language

		product_transformer_file = os.path.join(transformers_path, product_transformer_map[language])
		description_transformer_file = os.path.join(transformers_path, description_transformer_map[language])
		classifier_file = os.path.join(classifiers_path, classifier_map[language])

		with open(classifier_file, 'rb') as f:
			self.clf = pickle.load(f)

		with open(product_transformer_file, 'rb') as f:
			self.product_transformer = pickle.load(f)

		with open(description_transformer_file, 'rb') as f:
			self.description_transformer = pickle.load(f)


	"""
	INPUT:
	title of description of darknet market product

	OUTPUT:
	Probability of the product being relevant to the sale of exploits

	"""

	# Supervised
	def predict(self, title, description, language = 'sup_english'):
		if language != self.language:
			self.update_language(language)

		X_1 = self.product_transformer.transform([title])
		X_2 = self.description_transformer.transform([description])

		X = hstack([X_1, X_2])

		class_prediction = self.clf.predict_proba(X)[0]
		#class_prediction1 = self.clf.predict(X)[0]

		#we want the probability of the product being relevant, ie. in class '1'
		return class_prediction[1]

	# Semi-supervised
	def predict_semi(self, title, description, language = 'semi_english'):
		if language != self.language:
			self.update_language(language)


		X_1 = self.product_transformer.transform([title])
		X_2 = self.description_transformer.transform([description])

		X = hstack([X_1, X_2])
		X = csr_matrix(X)
		temp = int(X._shape[1]/2)
		t2 = 2*temp

		# Divide the feature set
		test_left = X[:,:temp]
		test_right = X[:,temp:t2]

		p1 = self.clf[0].predict_proba(test_left)[0][1]
		p2 = self.clf[1].predict_proba(test_right)[0][1]

		final = (p1 + p2)/2

		#we want the probability of the product being relevant, ie. in class '1'
		#return class_prediction[1]
		return final

my_clf = Classifier()

"""
INPUT:
title of description of darknet market product

OUTPUT:
Probability of the product being relevant to the sale of exploits

"""
def predict(title, description, language = 'sup_english'):
	#we want the probability of the product being relevant, ie. in class '1'
	return my_clf.predict (title, description, language=language)

def predict_semi(title, description, language = 'semi_english'):
	#we want the probability of the product being relevant, ie. in class '1'
	return my_clf.predict_semi (title, description, language=language)
