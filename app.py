import streamlit as st
import os
from dotenv import load_dotenv
from google import genai

st.set_page_config(
    page_title="Gemini AI Assistant",
    page_icon="🤎",
    layout="centered"
)

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error("❌ Gemini API key not found.")

    st.info(
        "Create a .env file in the same folder as app.py "
        "and add:\n\n"
        "GEMINI_API_KEY=YOUR_API_KEY"
    )

    st.stop()

try:
    client = genai.Client(api_key=api_key)

except Exception as error:
    st.error("❌ Could not connect to Gemini.")
    st.code(str(error))
    st.stop()

MODEL_NAME = "gemini-3.8-flash"

if "messages" not in st.session_state:
    st.session_state.messages = []

if "interaction_id" not in st.session_state:
    st.session_state.interaction_id = None

st.markdown(
    """
<style>

.stApp {
    background:
        radial-gradient(
            circle at 15% 10%,
            #fffaf3 0%,
            transparent 28%
        ),
        radial-gradient(
            circle at 90% 15%,
            #ead7c1 0%,
            transparent 32%
        ),
        radial-gradient(
            circle at 50% 100%,
            #e5ceb4 0%,
            transparent 38%
        ),
        #f5eadc;
}


.block-container {
    max-width: 900px;
    padding-top: 35px;
    padding-bottom: 110px;
}

.main-title {
    text-align: center;
    color: #5b3927;
    font-size: 42px;
    font-weight: 800;
    margin-bottom: 5px;
}


.main-subtitle {
    text-align: center;
    color: #92745e;
    font-size: 15px;
    margin-bottom: 30px;
}

.welcome-box {
    background: #fffaf3;
    border: 1px solid #dfc8b0;
    border-radius: 22px;
    padding: 30px;
    text-align: center;
    margin: 10px auto 30px auto;
    box-shadow: 0 10px 30px rgba(91, 57, 39, 0.08);
}


/* =====================================================
   COFFEE CUP COLOR
   ===================================================== */

.welcome-icon {
    font-size: 30px;
    margin-bottom: 8px;
    color: #8B5E3C;
}


.welcome-icon .cup {
    color: #8B5E3C !important;
    font-size: 30px;
}


.welcome-heading {
    color: #65432e;
    font-size: 22px;
    font-weight: 700;
    margin-bottom: 10px;
}


.welcome-description {
    color: #8d6d55;
    font-size: 14px;
    line-height: 1.7;
}

[data-testid="stChatMessage"] {
    background: rgba(255, 250, 243, 0.96);
    border: 1px solid #dfcbb7;
    border-radius: 18px;
    margin-bottom: 12px;
    box-shadow: 0 5px 18px rgba(91, 57, 39, 0.06);
}


[data-testid="stChatMessage"] p {
    color: #5b4030 !important;
    font-size: 15px;
    line-height: 1.6;
}

[data-testid="stChatInput"] > div {
    background: #fffaf3 !important;
    border: 1px solid #d2b69a !important;
    border-radius: 18px !important;
}


[data-testid="stChatInput"] textarea {
    background: transparent !important;
    color: #543827 !important;
    border: none !important;
}


[data-testid="stChatInput"] textarea::placeholder {
    color: #a58a74 !important;
}


[data-testid="stChatInput"] textarea:focus {
    border: none !important;
    box-shadow: none !important;
}

[data-testid="stSidebar"] {
    background: #eadbc8;
}


[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    color: #5b3927 !important;
}


[data-testid="stSidebar"] p {
    color: #765640 !important;
}


/* =====================================================
   CLEAR CHAT BUTTON
   ===================================================== */

[data-testid="stSidebar"] .stButton button {
    width: 100%;
    background: #765039 !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 12px;
    padding: 10px;
    font-weight: 600;
}

[data-testid="stSidebar"] .stButton button p {
    color: #ffffff !important;
}

[data-testid="stSidebar"] .stButton button:hover {
    background: #5d3d2b !important;
    color: #ffffff !important;
}

[data-testid="stSidebar"] .stButton button:hover p {
    color: #ffffff !important;
}


/* =====================================================
   CHAT AVATAR - EMOJI ONLY
   ===================================================== */

[data-testid="stChatMessageAvatarUser"],
[data-testid="stChatMessageAvatarAssistant"] {
    background: transparent !important;
    background-color: transparent !important;
    border: none !important;
    box-shadow: none !important;
    padding: 0 !important;
}

[data-testid="stChatMessageAvatarUser"] *,
[data-testid="stChatMessageAvatarAssistant"] * {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
}


/* =====================================================
   FOOTER
   ===================================================== */

.footer {
    text-align: center;
    color: #a1846c;
    font-size: 12px;
    margin-top: 35px;
    margin-bottom: 20px;
}

</style>
""",
    unsafe_allow_html=True
)

st.markdown(
    '<div class="main-title">🤎 Gemini AI Assistant</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="main-subtitle">'
    'A calm and dreamy space for questions, ideas and learning'
    '</div>',
    unsafe_allow_html=True
)

if not st.session_state.messages:

    st.markdown(
        '<div class="welcome-box">'
        '<div class="welcome-icon">'
        '<span class="cup">☕</span>'
        '</div>'
        '<div class="welcome-heading">'
        'Welcome to your AI Assistant'
        '</div>'
        '<div class="welcome-description">'
        'Ask me about coding, projects, academics, '
        'technology, ideas or anything you want to learn.'
        '</div>'
        '</div>',
        unsafe_allow_html=True
    )


# =========================================================
# DISPLAY CHAT HISTORY
# =========================================================

for message in st.session_state.messages:

    with st.chat_message(
        message["role"],
        avatar="👩‍💻" if message["role"] == "user" else "🤎"
    ):
        st.markdown(message["content"])


# =========================================================
# CHAT INPUT
# =========================================================

user_input = st.chat_input(
    "☕ Type your message here..."
)


# =========================================================
# PROCESS USER MESSAGE
# =========================================================

if user_input:

    with st.chat_message(
        "user",
        avatar="👩‍💻"
    ):
        st.markdown(user_input)

    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )

    with st.chat_message(
        "assistant",
        avatar="🤎"
    ):

        with st.spinner("☕ Gemini is thinking..."):

            try:

                if st.session_state.interaction_id is None:

                    interaction = client.interactions.create(
                        model=MODEL_NAME,
                        input=user_input
                    )

                else:

                    interaction = client.interactions.create(
                        model=MODEL_NAME,
                        input=user_input,
                        previous_interaction_id=(
                            st.session_state.interaction_id
                        )
                    )

                st.session_state.interaction_id = interaction.id

                ai_response = interaction.output_text

                if not ai_response:

                    raise Exception(
                        "Gemini returned an empty response."
                    )

                ai_response = ai_response.strip()

                st.markdown(ai_response)

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": ai_response
                    }
                )

            except Exception as error:

                if (
                    st.session_state.messages
                    and st.session_state.messages[-1]["role"] == "user"
                ):
                    st.session_state.messages.pop()

                error_text = str(error)

                st.error(
                    "❌ Gemini could not generate a response."
                )

                with st.expander("🔍 Technical details"):
                    st.code(error_text)


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.header("☕ Chat Settings")

    st.success("🤎 Gemini AI is ready")

    st.divider()

    st.subheader("🤖 Model")

    st.write(MODEL_NAME)

    st.divider()

    if st.button("🗑️ Clear Chat"):

        st.session_state.messages = []
        st.session_state.interaction_id = None

        st.rerun()

    st.divider()

    st.subheader("✨ About")

    st.write(
        "A simple AI chatbot built with "
        "Python, Streamlit and Google Gemini."
    )

    st.divider()

    st.caption(
        "Python • Streamlit • Gemini API"
    )


# =========================================================
# FOOTER
# =========================================================

st.markdown(
    '<div class="footer">'
    'Made with ☕ Python + Streamlit + 🤎'
    '</div>',
    unsafe_allow_html=True
)