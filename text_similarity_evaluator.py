'''
:Script:       text_similarity_evaluator.py
:Version:      0.9.9
:Release Date: 01 February 2021

:Purpose:      Takes 2 text strings as inputs and outputs a binary value based
               on the similarity of the texts.

Script Process
==============

1) Takes 2 texts as input to compare
2) Scrubs the text by removing contractions and replaces synonyms in the texts
3) Compares the 2 texts as word by word with each sentences in a list of lists
4) Calculates how similar the texts based on how many words are the same per
   each sentence. Adds up those scores for each sentence and divides by total
   number of sentences resulting in a score between 0 and 1; 1 equals 100% match 

Change History
==============
==========  =======  ===================  =====================================
   Date     Version     Author                   Description
==========  =======  ===================  =====================================
2021-02-01  0.9.9    Raghu Veer Madiraju  Initial Release
==========  =======  ===================  =====================================

Script Functions
================
'''

def text_scrubber(text_to_scrub):

    contractions_synonyms_dict = {
        "ain't": "am not",
        "aren't": "are not",
        "can't": "cannot",
        "can't've": "cannot have",
        "'cause": "because",
        "could've": "could have",
        "couldn't": "could not",
        "couldn't've": "could not have",
        "didn't": "did not",
        "doesn't": "does not",
        "don't": "do not",
        "hadn't": "had not",
        "hadn't've": "had not have",
        "hasn't": "has not",
        "haven't": "have not",
        "he'd": "he would",
        "he'd've": "he would have",
        "he'll": "he will",
        "he'll've": "he will have",
        "he's": "he is",
        "how'd": "how did",
        "how'd'y": "how do you",
        "how'll": "how will",
        "how's": "how is",
        "I'd": "I would",
        "I'd've": "I would have",
        "I'll": "I will",
        "I'll've": "I will have",
        "I'm": "I am",
        "I've": "I have",
        "isn't": "is not",
        "it'd": "it had",
        "it'd've": "it would have",
        "it'll": "it will",
        "it'll've": "it will have",
        "it's": "it is",
        "let's": "let us",
        "ma'am": "madam",
        "mayn't": "may not",
        "might've": "might have",
        "mightn't": "might not",
        "mightn't've": "might not have",
        "must've": "must have",
        "mustn't": "must not",
        "mustn't've": "must not have",
        "needn't": "need not",
        "needn't've": "need not have",
        "o'clock": "of the clock",
        "oughtn't": "ought not",
        "oughtn't've": "ought not have",
        "shan't": "shall not",
        "sha'n't": "shall not",
        "shan't've": "shall not have",
        "she'd": "she would",
        "she'd've": "she would have",
        "she'll": "she will",
        "she'll've": "she will have",
        "she's": "she is",
        "should've": "should have",
        "shouldn't": "should not",
        "shouldn't've": "should not have",
        "so've": "so have",
        "so's": "so is",
        "that'd": "that would",
        "that'd've": "that would have",
        "that's": "that is",
        "there'd": "there had",
        "there'd've": "there would have",
        "there's": "there is",
        "they'd": "they would",
        "they'd've": "they would have",
        "they'll": "they will",
        "they'll've": "they will have",
        "they're": "they are",
        "they've": "they have",
        "to've": "to have",
        "wasn't": "was not",
        "we'd": "we had",
        "we'd've": "we would have",
        "we'll": "we will",
        "we'll've": "we will have",
        "we're": "we are",
        "we've": "we have",
        "weren't": "were not",
        "what'll": "what will",
        "what'll've": "what will have",
        "what're": "what are",
        "what's": "what is",
        "what've": "what have",
        "when's": "when is",
        "when've": "when have",
        "where'd": "where did",
        "where's": "where is",
        "where've": "where have",
        "who'll": "who will",
        "who'll've": "who will have",
        "who's": "who is",
        "who've": "who have",
        "why's": "why is",
        "why've": "why have",
        "will've": "will have",
        "won't": "will not",
        "won't've": "will not have",
        "would've": "would have",
        "wouldn't": "would not",
        "wouldn't've": "would not have",
        "y'all": "you all",
        "y'alls": "you alls",
        "y'all'd": "you all would",
        "y'all'd've": "you all would have",
        "y'all're": "you all are",
        "y'all've": "you all have",
        "you'd": "you had",
        "you'd've": "you would have",
        "you'll": "you will",
        "you'll've": "you will have",
        "you're": "you are",
        "you've": "you have",
        "UPCs": "barcodes",
        "cut out": "clip",
        "participating": "eligible",
        "check out": "shop",
        "products": "items",
        " the ": " ",
        " a ": " ",
        " an ": " "
        }
    

    # Replaces contractions or sysonyms with predefiend values
    for key, value in contractions_synonyms_dict.items():
        if key in text_to_scrub:
            text_to_scrub = text_to_scrub.replace(key, value)

    text_to_scrub = text_to_scrub.rstrip(" ")
    text_in_list = text_to_scrub.split(". ")
    texts_in_list = []

    # Adds each sentence to its own lists and adds the the lists of sentences in
    # to a larger list.
    for sentence in text_in_list:
        if not sentence.endswith("."):
            sentence = sentence + "."
        sentence = sentence.split(" ")
        texts_in_list.append(sentence)

    return texts_in_list

def comparison_assessor(first_text_list, second_text_list):

    i = 0
    similarity_score = 0

    # Iterates comparing the lists representing each of the sentences word
    # by word until it reaches the total number of sentences.
    while i < len(first_text_list):

        # Making sure the first list is the larger one for each calculations
        if len(first_text_list[i]) < len(second_text_list[i]):
            len_first_text = first_text_list[i]
            len_second_text = second_text_list[i]
            first_text_list[i] = len_second_text
            second_text_list[i] = len_first_text
        count = 0
        score_minder = 0

        # Iterating over each word in a sentence
        for first_text_word in first_text_list[i]:
            #print('first_text_word = ' + first_text_word)

            # Checking to see if the same word from first list exists in the
            # same index of the second sentence.
            if first_text_word == second_text_list[i][count]:
                #print('second_text_word = ' + second_text_list[i][count])
                score_minder +=1
            
            # If there is word that does not match and there is an extra word
            # in the always longer or equal lenght first sentence, and adds a
            # empty string so that matching can proceed
            elif len(first_text_list[i]) > len(second_text_list[i]):
                second_text_list[i].insert(count, "")

            else:
                # If those conditions don't match, checks to see if the word in
                # in the next position matches.
                try:
                    if first_text_word == second_text_list[i][count + 1] or \
                        first_text_list[i][count+1] == \
                            second_text_list[i][count]:
                            #print('second_text_word = ' + \
                            #    second_text_list[i][count])
                            score_minder +=1
                except:
                    pass
            count += 1

            # IF the for loop reaches end of sentence and if the number of
            # words that are the same between both lists is greater than a 75%
            # match, then add to similarity score. This represents the number
            # of words that are common between both texts per sentnece and the
            # total number of words in the sentence.
            if count == len(first_text_list[i]):
                if score_minder/len(first_text_list[i]) > .75:
                    #print(score_minder)
                    #print(len(first_text_list[i]))
                    #print((score_minder/len(first_text_list[i])))
                    similarity_score += (score_minder/len(first_text_list[i]))
            if first_text_word == first_text_list[i][-1]:
                i += 1
    #print(similarity_score)
    score = (round(similarity_score/len(first_text_list), 2))
    #print("Text similarity score = " + str(score))
    return(score)
        
if __name__ == '__main__':

    first_text = str(input("Enter the first text to compare: "))
    second_text = str(input("Enter the first text to compare: "))
    
    first_text_list = text_scrubber(first_text)
    second_text_list = text_scrubber(second_text)

    if len(first_text_list) < len(second_text_list):
            len_first_text = first_text_list
            len_second_text = second_text_list
            first_text_list = len_second_text
            second_text_list = len_first_text

    while len(first_text_list) > len(second_text_list):
        empty_list = [""]
        second_text_list.append(empty_list)

    similarity_score = comparison_assessor(first_text_list, second_text_list)
    print(similarity_score)
