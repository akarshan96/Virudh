import spacy
import language_check
import requests
import re


def get_proper_nouns(text):
    # This function extracts proper nouns like name, day, country etc.
    proper_noun_list_ = []
    nlp = spacy.load("en")
    text = nlp(text)
    for word in list(text.sents)[0]:
        if word.tag_ == "NNP":
            proper_noun_list_.append(str(word))
    return proper_noun_list_


def grammar_check(text, proper_noun_list):
    # This function returns a list of grammatical errors and spelling mistakes
    incorrect_list_ = []
    tool = language_check.LanguageTool('en-GB')
    matches = tool.check(text)
    for i in range(len(matches)):
        incorrect_text = text[matches[i].fromx:]
        incorrect_text = incorrect_text.split(" ")
        if incorrect_text[0] not in proper_noun_list and incorrect_text[0] not in incorrect_list_:
            incorrect_list_.append(incorrect_text[0])
    return incorrect_list_


def grammar_check_2(text):
    try:
        incorrect_list_ = []
        url = "https://languagetool.org/api/v2/check?text=" + text + "&language=en-GB&enabledOnly=false"
        response = requests.get(url).json()
        matches = response['matches']
        if matches:
            for i in range(len(matches)):
                incorrect_list_.append(text[response['matches'][i]['offset']: response['matches'][i]['offset'] +
                                                                              response['matches'][i]['length']])
        return incorrect_list_
    except:
        return []


def check_capitals(text):
    text = text.replace(" ", "")
    no_of_capitals = len(re.findall(r'[A-Z]', text))
    return no_of_capitals / len(text) * 100


def spl_charecters(text):
    text = text.replace(" ", "")
    no_of_spl_chars = len(re.sub('[\w]+', '', text))
    return no_of_spl_chars / len(text) * 100


def repetition_case(text):
    count = 0
    r = re.compile(r'(.)\1*')
    for m in r.finditer(text):
        if len(m.group()) > 2:
            count += 1
    return count


def perform_soft_tests(news_text):
    # Stage_1
    proper_noun_list = get_proper_nouns(news_text)

    # Stage 2
    incorrect_list = grammar_check(news_text, proper_noun_list)
    incorrect_list_2 = grammar_check_2(news_text)

    # Stage 3
    capital_percentage = check_capitals(news_text)

    # Stage 4
    repetitive_characters = repetition_case(news_text)

    # Stage 5
    special_percentage = spl_charecters(news_text)
    return {"critical_words": proper_noun_list, "incorrect_text_1": incorrect_list,
            "capital_percentage": capital_percentage, "repetitive_characters": repetitive_characters,
            "special_percentage": special_percentage}

#a = perform_soft_tests("""BJP spokesperson Sambit Patra said Congress' leaders had come to the Mahatma Gandhi’s memorial to talk about non-violence but the presence of Kumar and Tytler exposed the party’s real violent face.""")
#print(a)