import streamlit as st
from streamlit_chat import message
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
import time
import random
from langdetect import detect

# Configuration de la page
st.set_page_config(page_title="Quizzy the Assistant", page_icon="🤖", layout="centered")

# 🔒 Remplace cette clé par la tienne en local
GROQ_API_KEY = ""  # Remplace par ta clé API Groq

# Initialisation du LLM
llm = ChatGroq(api_key=GROQ_API_KEY, model="llama-3.3-70b-versatile", temperature=0.7)

# Ajout du logo dans la sidebar
st.sidebar.image("logo.png", width=200)

# Template du prompt (multilingue)
prompt_template = ChatPromptTemplate.from_template(
    """You are Quizzy, an intelligent assistant to help students use ClassQuiz. 
    You can understand and respond in English, French, and Arabic. Always answer in the same language as the user's question.
    
    Student: {question}
    Quizzy:"""
)

# Initialisation des messages en session
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hi! I'm Quizzy, your assistant for ClassQuiz. How can I help you today?"}
    ]

# Initialisation de la progression et avatar
if "progress" not in st.session_state:
    st.session_state.progress = 0
if "avatar" not in st.session_state:
    st.session_state.avatar = "👶"

st.title("Quizzy the Assistant 🤖")

# Affichage des messages existants
for i, msg in enumerate(st.session_state.messages):
    message(msg["content"], is_user=(msg["role"] == "user"), key=f"msg_{i}")

# Zone de saisie utilisateur toujours en bas
user_input = st.chat_input("Ask your question here...")

if user_input:
    # Ajout du message utilisateur
    st.session_state.messages.append({"role": "user", "content": user_input})
    message(user_input, is_user=True, key=f"user_{len(st.session_state.messages)}")

    # Détection de la langue utilisateur
    try:
        user_language = detect(user_input)
    except:
        user_language = "en"

    # Obtenir la réponse du bot
    with st.spinner("Quizzy is thinking..."):
        time.sleep(1)
        prompt = prompt_template.format(question=user_input)
        bot_response = llm.invoke(prompt)

    # Vérification du retour de `llm.invoke()`
    if isinstance(bot_response, str):
        bot_reply = bot_response
    else:
        bot_reply = bot_response.content if hasattr(bot_response, "content") else "I couldn't process that."

    # Gestion des exercices (progression et avatar)
    exercise_keywords = ["exercise", "exercice", "compléter", "تمرين"]
    if any(keyword in user_input.lower() for keyword in exercise_keywords):
        st.session_state.progress = min(st.session_state.progress + 10, 100)
        if st.session_state.progress >= 100:
            st.session_state.avatar = "🏆"
        elif st.session_state.progress >= 75:
            st.session_state.avatar = "🚀"
        elif st.session_state.progress >= 50:
            st.session_state.avatar = "🌟"
        elif st.session_state.progress >= 25:
            st.session_state.avatar = "👦"

    # Ajout de la réponse du bot
    st.session_state.messages.append({"role": "assistant", "content": bot_reply})
    message(bot_reply, is_user=False, key=f"bot_{len(st.session_state.messages)}")

# Bouton de réinitialisation
if st.button("Restart Conversation 🔄"):
    st.session_state.messages = [
        {"role": "assistant", "content": "Hi! I'm Quizzy, your assistant for ClassQuiz. How can I help you today?"}
    ]
    st.session_state.progress = 0
    st.session_state.avatar = "👶"
    st.rerun()

# ✅ Conseil du jour
tips = [
    "Don't forget to take regular breaks!",
    "Drink water to stay hydrated while learning.",
    "If you're struggling with an exercise, don't hesitate to ask for help!",
    "Celebrate every little progress you make!",
    "Mistakes are opportunities to learn something new."
]
st.sidebar.title("📌 Tip of the Day")
st.sidebar.info(random.choice(tips))

# ✅ Barre de progression
st.sidebar.title("📊 Your Progress Today")
st.sidebar.progress(st.session_state.progress)
if st.session_state.progress == 100:
    st.sidebar.success("Congratulations! You've reached 100% progress! 🎉")

# ✅ Affichage avatar évolutif
st.sidebar.title("👤 Your Avatar Evolution")
st.sidebar.markdown(f"## {st.session_state.avatar}")
st.sidebar.info(f"Progress: {st.session_state.progress}%")