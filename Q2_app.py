import streamlit as st
import random
from PIL import Image
import requests
from io import BytesIO

# URL to the raw images in your GitHub repository
company_logo_url = "https://raw.githubusercontent.com/your-username/your-repo/main/path/to/narmada_logo.png"
background_image_url = "https://raw.githubusercontent.com/your-username/your-repo/main/path/to/green_background.jpg"

# Load images from GitHub
response_logo = requests.get(company_logo_url)
company_logo = Image.open(BytesIO(response_logo.content))

response_background = requests.get(background_image_url)
background_image = Image.open(BytesIO(response_background.content))

# Convert background image to base64
buffered = BytesIO()
background_image.save(buffered, format="JPEG")
background_image_base64 = base64.b64encode(buffered.getvalue()).decode()

# Display background image using Streamlit's image with background styling
st.markdown(
    f"""
    <style>
    .stApp {{
        background: url("data:image/jpeg;base64,{background_image_base64}") no-repeat center center fixed;
        background-size: cover;
        background-color: rgba(249, 249, 244, 0.95);
    }}
    .welcome-box {{
        display: none;
    }}
    .welcome-text {{
        color: #2d4739;
        font-size: 2.5em;
        margin-bottom: 20px;
        text-align: center;
    }}
    .welcome-subtext {{
        color: #3d5a3c;
        font-size: 1.2em;
        margin-bottom: 30px;
        text-align: center;
    }}
    .stButton>button {{
        background-color: #4CAF50;
        color: white;
        border-radius: 10px;
        padding: 12px 24px;
        font-size: 18px;
        cursor: pointer;
        transition: background-color 0.3s, transform 0.2s ease;
        border: none;
    }}
    .stButton>button:active {{
        transform: scale(0.95);
    }}
    .quiz-header {{
        font-size: 1.5em;
        font-weight: bold;
        text-align: center;
        color: #4CAF50;
        margin-top: 20px;
    }}
    .question-box {{
        background-color: rgba(255, 255, 255, 0.9);
        border-radius: 10px;
        padding: 20px;
        margin: 20px 0;
        box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
        text-align: center;
        font-size: 1.2em;
        color: #2d4739;
    }}
    .option-button {{
        display: block;
        background-color: #4CAF50;
        color: white;
        border: none;
        border-radius: 5px;
        padding: 10px 20px;
        font-size: 1em;
        margin: 10px auto;
        cursor: pointer;
        width: 80%;
    }}
    .score-box {{
        background-color: rgba(255, 255, 255, 0.85);
        border-radius: 15px;
        padding: 30px;
        margin: 20px 0;
        box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
        text-align: center;
    }}
    .score-text {{
        color: #2d4739;
        font-size: 2em;
        font-weight: bold;
        margin-top: 10px;
        margin-bottom: 20px;
    }}
    .celebration {{
        text-align: center;
        font-size: 2em;
        color: #28a745;
        margin-top: 20px;
        font-weight: bold;
    }}
    @keyframes fadeIn {{
        from {{ opacity: 0; }}
        to {{ opacity: 1; }}
    }}
    @keyframes slideIn {{
        from {{ transform: translateY(50px); }}
        to {{ transform: translateY(0); }}
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# Welcome page logic
if "welcome_page" not in st.session_state:
    st.session_state.welcome_page = True

if st.session_state.welcome_page:
    # Display the company logo and welcome box
    st.image(company_logo, use_column_width=True)

    st.markdown(f"<div class='welcome-text'>Welcome to the Quiz!</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='welcome-subtext'>Presented by Narmada Bio Chem Limited</div>", unsafe_allow_html=True)
    st.markdown(
        """
        <div class='welcome-subtext'>
        Test your knowledge about organic farming, bio-fertilizers, and sustainable agriculture. 
        Learn about the importance of organic fertilizers for a greener tomorrow!
        </div>
        """,
        unsafe_allow_html=True
    )

    if st.button("Start Quiz"):
        st.session_state.welcome_page = False
        st.experimental_rerun()

# Quiz Data
quiz_data = {
    "Which component is a key ingredient in organic fertilizers?": {
        "options": ["Compost", "Plastic", "Chemical", "Metal"],
        "answer": "Compost"
    },
    "What is the primary benefit of bio-fertilizers?": {
        "options": ["Promotes chemical growth", "Increases crop yield naturally", "Harms soil", "Decreases plant growth"],
        "answer": "Increases crop yield naturally"
    },
    "Which of the following is considered an eco-friendly fertilizer?": {
        "options": ["Bio-fertilizer", "Plastic mulch", "Synthetic chemicals", "Pesticides"],
        "answer": "Bio-fertilizer"
    },
    "Which farming method uses organic fertilizers?": {
        "options": ["Organic farming", "Hydroponic farming", "Conventional farming", "Factory farming"],
        "answer": "Organic farming"
    },
    "Which element is essential in bio-fertilizers for plant growth?": {
        "options": ["Nitrogen", "Lead", "Aluminum", "Mercury"],
        "answer": "Nitrogen"
    },
}

# Function to pick 3 random questions
def get_random_questions(quiz_data, num_questions=3):
    questions = random.sample(list(quiz_data.keys()), num_questions)
    return {question: quiz_data[question] for question in questions}

# Initialize session state for the quiz
if "questions" not in st.session_state:
    st.session_state.questions = get_random_questions(quiz_data)
    st.session_state.current_question_index = 0
    st.session_state.score = 0
    st.session_state.quiz_completed = False

# Function to handle answer selection
def handle_answer(option):
    current_question = list(st.session_state.questions.keys())[st.session_state.current_question_index]
    correct_answer = st.session_state.questions[current_question]["answer"]

    if option == correct_answer:
        st.session_state.score += 1

    st.session_state.current_question_index += 1

    if st.session_state.current_question_index >= len(st.session_state.questions):
        st.session_state.quiz_completed = True

# Display the quiz
if not st.session_state.welcome_page:
    if not st.session_state.quiz_completed:
        if st.session_state.current_question_index < len(st.session_state.questions):
            current_question = list(st.session_state.questions.keys())[st.session_state.current_question_index]
            st.markdown(f"<div class='quiz-header'>Question {st.session_state.current_question_index + 1}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='question-box'>{current_question}</div>", unsafe_allow_html=True)

            options = st.session_state.questions[current_question]["options"]

            # Display clickable option boxes
            for option in options:
                if st.button(option, key=option):
                    handle_answer(option)
                    st.experimental_rerun()

    # Show score at the end
    if st.session_state.quiz_completed:
        st.markdown("<div class='score-box'>", unsafe_allow_html=True)
        
        st.markdown(f"<div class='score-text'>Quiz Completed!</div>", unsafe_allow_html=True)
        
        if st.session_state.score == len(st.session_state.questions):
            st.markdown("<div class='score-text'>🎉 Perfect Score! 🎉</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='score-text'>Your final score is **{st.session_state.score}/{len(st.session_state.questions)}**</div>", unsafe_allow_html=True)
            st.markdown('<div class="celebration">Congratulations! You got all answers correct!</div>', unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='score-text'>Your final score is **{st.session_state.score}/{len(st.session_state.questions)}**</div>", unsafe_allow_html=True)
        
        # Additional elements
        st.markdown("**Download your personalized certificate:** [Download](#)", unsafe_allow_html=True)

        # Share the score on social media
        share_text = f"I scored {st.session_state.score}/{len(st.session_state.questions)} in the Organic Fertilizer Quiz!"
        st.write("Share your score:")
        st.markdown(f"[Share on WhatsApp](https://api.whatsapp.com/send?text={share_text})", unsafe_allow_html=True)
        st.markdown(f"[Share on Twitter](https://twitter.com/intent/tweet?text={share_text})", unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)
