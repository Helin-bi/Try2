import streamlit as st
import random

# Set background color or image using custom CSS
st.markdown(
    """
    <style>
    .stApp {
        background-image: url("https://www.yourimageurl.com/background.jpg");
        background-size: cover;
        background-attachment: fixed;
    }
    .stButton>button {
        background-color: #007bff;
        color: white;
        border-radius: 5px;
        padding: 10px 20px;
        font-size: 16px;
    }
    .stButton>button:hover {
        background-color: #0056b3;
    }
    .celebration {
        text-align: center;
        font-size: 2em;
        color: #28a745;
        margin-top: 50px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Quiz data
quiz_data = {
    "What is the capital of India?": {
        "options": ["Delhi", "Mumbai", "Chennai", "Kolkata"],
        "answer": "Delhi"
    },
    "Which nutrient is essential for plant growth?": {
        "options": ["Nitrogen", "Oxygen", "Carbon Dioxide", "Hydrogen"],
        "answer": "Nitrogen"
    },
    "What is the process of converting sunlight into energy in plants?": {
        "options": ["Photosynthesis", "Respiration", "Transpiration", "Osmosis"],
        "answer": "Photosynthesis"
    },
    "Which element is a micronutrient for plants?": {
        "options": ["Iron", "Carbon", "Hydrogen", "Oxygen"],
        "answer": "Iron"
    },
    "What is the main component of organic fertilizers?": {
        "options": ["Carbon", "Nitrogen", "Phosphorus", "Potassium"],
        "answer": "Carbon"
    },
}

# Function to pick 3 random questions
def get_random_questions(quiz_data, num_questions=3):
    questions = random.sample(list(quiz_data.keys()), num_questions)
    return {question: quiz_data[question] for question in questions}

# Initialize session state
if "questions" not in st.session_state:
    st.session_state.questions = get_random_questions(quiz_data)
    st.session_state.current_question_index = 0
    st.session_state.score = 0
    st.session_state.quiz_completed = False

# Display the current question
if not st.session_state.quiz_completed:
    if st.session_state.current_question_index < len(st.session_state.questions):
        current_question = list(st.session_state.questions.keys())[st.session_state.current_question_index]
        st.write(f"**Question {st.session_state.current_question_index + 1} of {len(st.session_state.questions)}:**")
        st.write(current_question)

        options = st.session_state.questions[current_question]["options"]

        # Display button options for answers
        for option in options:
            if st.button(option, key=f"btn_{st.session_state.current_question_index}_{option}"):
                correct_answer = st.session_state.questions[current_question]["answer"]
                if option == correct_answer:
                    st.session_state.score += 1
                
                # Move to the next question
                st.session_state.current_question_index += 1
                
                # Check if quiz is completed
                if st.session_state.current_question_index >= len(st.session_state.questions):
                    st.session_state.quiz_completed = True
                
                # Trigger the next step without st.experimental_rerun()
                st.experimental_set_query_params(step=st.session_state.current_question_index)

                # Stop further execution after an option is selected
                st.stop()

# Display the score page
if st.session_state.quiz_completed:
    st.write("## Quiz Completed!")
    
    if st.session_state.score == len(st.session_state.questions):
        st.write("## 🎉 Perfect Score! 🎉")
        st.write(f"Your final score is **{st.session_state.score}/{len(st.session_state.questions)}**")
        st.markdown('<div class="celebration">Congratulations! You got all answers correct!</div>', unsafe_allow_html=True)
    else:
        st.write(f"Your final score is **{st.session_state.score}/{len(st.session_state.questions)}**")

    # Share the score on social media
    share_text = f"I scored {st.session_state.score}/{len(st.session_state.questions)} in the Agriculture Quiz!"
    st.write("Share your score:")
    st.markdown(f"[Share on WhatsApp](https://api.whatsapp.com/send?text={share_text})", unsafe_allow_html=True)
    st.markdown(f"[Share on Twitter](https://twitter.com/intent/tweet?text={share_text})", unsafe_allow_html=True)

    # Reset the quiz
    if st.button("Retake the Quiz"):
        st.session_state.questions = get_random_questions(quiz_data)
        st.session_state.current_question_index = 0
        st.session_state.score = 0
        st.session_state.quiz_completed = False
        st.experimental_set_query_params(step=0)
        st.experimental_rerun()
