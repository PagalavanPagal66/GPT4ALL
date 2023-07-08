from time import sleep

import streamlit as st
from streamlit_chat import message
from utils import get_initial_message, get_chatgpt_response, update_chat
import os

import openai
import Coworker as coworker
import googletrans
from streamlit_option_menu import option_menu


openai.api_key = st.secrets['auth_key']

st.title("")

model = "gpt-3.5-turbo"


langtocode = {
    "Bengali": "bn-IN",
    "English-Aus": "en-AU",
    "English-Can": "en-CA",
    "English-Ind": "en-IN",
    "English-US": "en-US",
    "French": "fr-FR",
    "German": "de-DE",
    "Gujarati": "gu-IN",
    "Hindi": "hi-IN",
    "Japanese": "ja-JP",
    "Kannada": "kn-IN",
    "Malayalam": "ml-IN",
    "Marathi": "mr-IN",
    "Tamil": "ta-IN",
    "Telugu": "te-IN",
}
LANGUAGES = {
    'arabic' : 'ar' ,
    'bengali' : 'bn',
    'english' : 'en',
    'french' : 'fr',
    'german' : 'de',
    'greek' : 'el',
    'gujarati' :'gu',
    'japanese' : 'ja',
    'kannada' : 'kn',
    'malayalam' : 'ml',
    'marathi' : 'mr',
    'hindi' : 'hi',
    'tamil' : 'ta',
    'telugu' : 'te'
}

selected = option_menu(
    menu_title= None,
    options = ['Home','Text','Speech'],
    icons = ['house','book','mic-fill'],
    menu_icon = "cast",
    default_index = 0,
    orientation = "horizontal"
)
def body():
    if(selected == 'Home'):
        st.subheader("Hello...! I am your personal Assistant.....")
        with open('speaking.txt', 'w') as f:
            f.write("No Data to answer....Please give some input to me and try again...")
    if(selected == "Text"):
        #try:
            if 'generatedt' not in st.session_state:
                st.session_state['generatedt'] = []
            if 'pastt' not in st.session_state:
                st.session_state['pastt'] = []
            query = st.text_input("Query: ", key="input")
            if 'messagest' not in st.session_state:
                st.session_state['messagest'] = get_initial_message()

            if st.button("START"):
                with st.spinner("generating..."):
                    messages = st.session_state['messagest']
                    messages = update_chat(messages, "user", query)
                    response = get_chatgpt_response(messages, model)
                    messages = update_chat(messages, "assistant", response)
                    st.session_state.pastt.append(query)
                    st.session_state.generatedt.append(response)
                #file writing
                    with open('speaking.txt', 'w') as f:
                        d = str(response)
                        f.write(d)

            if st.session_state['generatedt']:
                for i in range(len(st.session_state['generatedt']) - 1, -1, -1):
                    message(st.session_state['pastt'][i], is_user=True, key=str(i) + '_user')
                    message(st.session_state["generatedt"][i], key=str(i))

            lang = st.selectbox("Choose Your Language: ",
                                (
                                'arabic',
                                'bengali',
                                'english',
                                'french',
                                'german',
                                'greek',
                                'gujarati',
                                'hindi',
                                'japanese',
                                'kannada',
                                'malayalam',
                                'marathi',
                                'tamil',
                                'telugu'
                                )
                                )
            if (st.checkbox("SPEAK")):
                code = LANGUAGES[lang]
                with open('speaking.txt', 'r') as f:
                    data = f.read()
                translated = coworker.trans(data,code)

            #splitting and getting only specific lang text
                tr = translated.text
                print(tr)
                st.success(tr)
                coworker.save(tr, code)
                audio_file = open('voicespeech.mp3', 'rb')  # enter the filename with filepath
                audio_bytes = audio_file.read()  # reading the file
                st.audio(audio_bytes, format='audio/ogg')
        #except:
         #   st.warning("OOPS...! Something went wrong...Check your network connection and try again...")
    elif (selected == 'Speech'):
        #try:
            index = 0
            if 'generated' not in st.session_state:
                st.session_state['generated'] = []
            if 'past' not in st.session_state:
                st.session_state['past'] = []
            if 'messages' not in st.session_state:
                st.session_state['messages'] = get_initial_message()
            col1, col2 = st.columns(2)
            with col1:
                lang = st.selectbox("Choose Your Language: ",
                            ("Bengali",
                             "English-Aus",
                             "English-Can",
                             "English-Ind",
                             "English-US",
                             "French",
                             "German",
                             "Gujarati",
                             "Hindi",
                             "Japanese",
                             "Kannada",
                             "Malayalam",
                             "Marathi",
                             "Tamil",
                             "Telugu")
                            )
            with col2:
                lang2 = st.selectbox("Choose any language to speak:",
                         (
                             'arabic',
                             'bengali',
                             'english',
                             'french',
                             'german',
                             'greek',
                             'gujarati',
                             'hindi',
                             'japanese',
                             'kannada',
                             'malayalam',
                             'marathi',
                             'tamil',
                             'telugu'
                         )
                         )
            if(st.button("START")):
                    st.warning("Listening...")
                    st.session_state['past'] = []
                    st.session_state['generated'] = []
                    code = langtocode[lang]
                    query = coworker.takeCommand(code)
                    st.info("Recognizing...")
                    if query:
                        with st.spinner("generating..."):
                            messages = st.session_state['messages']
                            messages = update_chat(messages, "user", query)
                            response = get_chatgpt_response(messages, model)
                            text = response

                            translator = googletrans.Translator()
                            raw_trans = translator.translate(text, src= LANGUAGES[lang2])
                            translation = raw_trans.text

                            with open("lango.txt", "w", encoding="utf-8") as f:
                                f.write(translation)




                            messages = update_chat(messages, "assistant", response)
                            st.session_state.past.append(query)
                            st.session_state.generated.append(response)
                    if st.session_state['generated']:
                        for i in range(len(st.session_state['generated']) - 1, -1, -1):
                            message(st.session_state['past'][i], is_user=True, key=str(index) + '_user')
                            message(st.session_state["generated"][i], key=str(index))
                            index = index+1
            if (st.checkbox("SPEAK")):

                    with open("lango.txt", "r", encoding="utf-8") as f:
                        stringvoice = f.read()
                    translated = coworker.trans(stringvoice,LANGUAGES[lang2])
                    # splitting and getting only specific lang text
                    tr = translated.text
                    print(tr)
                    st.success(tr)
                    coworker.save(tr,LANGUAGES[lang2])
                    audio_file = open('voicespeech.mp3','rb')  # enter the filename with filepath
                    audio_bytes = audio_file.read()  # reading the file
                    st.audio(audio_bytes, format='audio/ogg')
        #except:
        #   st.warning("OOPS...Something went wrong...Please Check your network connection and try again....")

if __name__ == '__main__':
    body()
