import spacy
import numpy as np
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import accuracy_score

from dataset import Dataset
from visualizer import plot_top_features

class Model:
    nlp = spacy.load("en_core_web_sm")

    def __init__(self, dataset: Dataset) -> None:
        """Create a machine learning model from the specified dataset."""
        self.dataset = dataset

    def spacy_tokenizer(self, doc) -> list:
        """Tokenize a document using the SpaCy package instead of the
        default regex based solution.
        """
        tokens = self.nlp(doc)
        lemmatized_tokens = [
            token.lemma_ for token in tokens
            if not token.is_stop and not token.is_punct and not token.lemma_.isspace()
        ]
        return lemmatized_tokens

    def train(self, condition: str, event: str) -> None:
        """Start training model."""

        # Collect a list of compiled texts from each patient
        texts = self.dataset.texts
        # And the label of each patient
        labels = self.dataset.labels(condition, event)

        vect = TfidfVectorizer(
                token_pattern=None,
                tokenizer=self.spacy_tokenizer,
                ngram_range=(1, 4),
                min_df=2
        )

        # Transform the texts into a TF-IDF matrix
        X = vect.fit_transform(texts)

        # Split the data into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(X, labels, test_size=0.2, random_state=42)

        # Train the linear regression model
        model = LogisticRegression(C=5, max_iter=1000)
        model.fit(X_train, y_train)
        
        # Obtain the feature names and coefficients
        feature_names = np.array(vect.get_feature_names_out())
        coefficients = model.coef_[0]

        # Call the reusable function to visualize the top features
        plot_top_features(feature_names, coefficients, 50)

        return model
