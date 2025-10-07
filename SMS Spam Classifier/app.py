import streamlit as st
import pickle
import nltk
from nltk.stem.porter import PorterStemmer
import string
from nltk.corpus import stopwords

tfidf = pickle.load(open("tfidf.pkl", "rb"))
model = pickle.load(open("model.pkl", "rb"))

st.title("Email/SMS Spam Classifier")
input_sms = st.text_input("Enter the message")

# 1- Preprocess
# 2- Vectorize
# 3- Predict
# 4- Display

if st.button("Predict"):
    # 1- Preprocess
    ps = PorterStemmer()
    def transform_text(text):
        # Lower Case
        text = text.lower()

        # Tokenization
        text = nltk.word_tokenize(text)

        # Removing Special Characters
        y = []
        for i in text:
            if i.isalnum():
                y.append(i)

        text = y.copy()
        y.clear()

        # Removing Stop Words and Punctuation
        for i in text:
            if i not in stopwords.words("english") and i not in string.punctuation:
                y.append(i)

        text = y.copy()
        y.clear()
        # Stemming
        for i in text:
            y.append(ps.stem(i))    
        
        return " ".join(y)

    transformed_sms = transform_text(input_sms)

    # 2- Vectorize
    vector_input = tfidf.transform([transformed_sms])

    # 3- Predict
    result = model.predict(vector_input)

    # 4- Display
    if result == 1:
        st.header("Spam")

    else:
        st.header("Not Spam")
