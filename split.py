# for extracting text
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options


# fix a bug
options = Options()
options.add_argument('--disable-blink-features=AutomationControlled')

def split_text_into_paragraphs(text: str, word_count: int) -> list:
    '''
    Should iterate through text until the given word count. From then, keep going until
    reaching the next period (.) or the end of the text (null)
    text (Str): full text to split into paragraphs.
    word_count (int): specified word count to approximately stop at
    Return: a list containing each paragraph containing approximate word_count
    '''

    # first split the text into individual words
    # iterate through until reaching the word_count OR reaching a null
    paragraphs = []

    count = 0
    current_paragraph = ''
    for word in text.split():
        current_paragraph += word + ' ' 
        count += 1

        # if word count is reached, then we want to keep going until reaching a dot
        if count >= word_count:

            # if there is a dot in the word, then end of sentence is reached.
            if "." in word:
                paragraphs.append(current_paragraph)
                count = 0
                current_paragraph = ''
    
    # add leftovers to the last paragraph
    paragraphs.append(current_paragraph)
        
    return paragraphs

def retrieveText(url):
    '''
    Retrieves text from a given website (in this case novelHall)
    website: a string URL to retrieve the text from
    '''
    driver = webdriver.Chrome()
    driver.get(url)

    # find the text in the website
    elements = driver.find_elements(By.XPATH,'//*[@id="htmlContent"]')
    texts = [element.text for element in elements]

    # print extracted text and put into a text variable
    paragraph = ""
    for text in texts:
        paragraph += text

    header = driver.find_element(By.XPATH,'//*[@id="main"]/div/div/article/div[1]/h1').text
    
    driver.quit()   

    return {'text': paragraph, 'header': header}

def scrapeSite(website: str, word_limit: int):
    '''
    Scrapes the website for text, splits into paragraphs to allow insertion into openai API

    website: the url to scrape from
    word_limit: the word limit for each paragraph
    '''
    # initialize webdriver

    novel_info = retrieveText(website)
    novel_text = novel_info['text']

    novel_info['text'] = split_text_into_paragraphs(novel_text,word_limit)

    return novel_info