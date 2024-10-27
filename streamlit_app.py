import streamlit as st
import google.generativeai as genai
import random
import requests
from PIL import Image
# Configure Gemini API
api_key = "AIzaSyCng9o5BRpAOT5AOy-22Xrs4OM1oRiAKvU" 
genai.configure(api_key=api_key)

# Create the model configuration
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
)

health_facts = [
    "Health Hack: Gut health is closely linked to mental well-being, as a healthy microbiome can improve mood.",
    "Health Hack: Spending just 20 minutes in nature can lower stress hormones and improve mental clarity.",
    "Health Hack: Dark chocolate can improve heart health and lower blood pressure when consumed in moderation.",
    "Health Hack: Practicing gratitude can enhance overall well-being and increase happiness.",
    "Health Hack: Maintaining good posture can improve digestion and boost confidence.",
    "Health Hack: A diet high in fiber can lower the risk of developing type 2 diabetes.",
    "Health Hack: Being around pets can reduce feelings of loneliness and increase happiness.",
    "Health Hack: Even brief physical activity, like taking the stairs, can boost energy levels throughout the day.",
    "Health Hack: Your sense of smell can evoke powerful memories and improve mood.",
    "Health Hack: Drinking green tea can boost metabolism and improve brain function."
    "Health Hack: Regularly practicing mindfulness can reduce anxiety and improve emotional resilience.",
    "Health Hack: Eating with friends and family can enhance your meal experience and improve digestion.",
    "Health Hack: Listening to music can lower stress levels and enhance your mood.",
    "Health Hack: Taking short breaks throughout the day can improve focus and productivity.",
    "Health Hack: Journaling your thoughts can clarify emotions and enhance mental health.",
    "Health Hack: A diet rich in omega-3 fatty acids can support brain health and improve memory.",
    "Health Hack: Drinking a glass of water before meals can help control appetite and aid digestion.",
    "Health Hack: Spending time in the sun can boost vitamin D levels, essential for bone health.",
    "Health Hack: Engaging in creative activities can enhance brain function and reduce stress.",
    "Health Hack: Practicing deep breathing exercises can quickly reduce stress and anxiety levels."
]



# Initialize session state to keep track of the current feature
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'Home'

# Function for the home page
def home():
    st.markdown(
        "<h1 style='text-align: center; color: #4CAF50;'>Welcome to CureAI 🩺</h1>",
        unsafe_allow_html=True
    )
    
    st.markdown(
        "<h3 style='text-align: center;'>What can I do for you today?</h3>",
        unsafe_allow_html=True
    )
    user_question = st.text_input("Ask any health-related question:")
    health_prompt = f"""
You are a knowledgeable and empathetic health assistant designed to provide clear and informative responses to health-related questions. Your goal is to help users understand their inquiries by offering evidence-based information and practical advice.

1. **Thorough Analysis:** Carefully analyze the user's question to ensure a complete understanding of their concern.

2. **Informative Responses:** Provide concise, accurate, and relevant information related to the query. Use simple language to ensure the user comprehends the details.

3. **General Advice:** Whenever applicable, suggest lifestyle changes or general health tips that could be beneficial. This may include recommendations on diet, exercise, mental health practices, or wellness strategies.

4. **Encouragement for Professional Consultation:** While providing helpful information, remind the user that for personalized medical advice, it is always best to consult a qualified healthcare professional. Frame this reminder positively, emphasizing the importance of professional guidance for their specific health needs.

5. **Supportive Tone:** Maintain an empathetic and supportive tone throughout your response to ensure the user feels heard and valued.

Here’s the user's question: '{user_question}'
"""
    # If the user submits a question, get the response from Gemini
    if user_question:
        response = get_gemini_response(health_prompt)  # This should call your Gemini API function
        st.write("**Response from CureAI:**")
        st.write(response)


    # Custom CSS for styling buttons with animations
    st.markdown(""" 
        <style>
            .stButton > button {
                background-color: #4CAF50;  /* Green */
                color: white;  /* Initial text color */
                padding: 10px;
                border: none;
                border-radius: 5px;
                width: 100%;  /* Full width */
                text-align: center; /* Align text to the center */
                transition: transform 0.3s ease, background-color 0.3s ease; /* Transition for scaling and background color */
            }
            .stButton > button:hover {
                background-color: #45a049;  /* Darker green */
                transform: scale(1.05);  /* Scale up on hover */
                color: white;  /* Change text color to white on hover */
            }
            .stButton > button:active {
                background-color: #45a049; /* Maintain the hover background color on click */
                transform: scale(0.95); /* Scale down on click */
                color: white;  /* Keep text color white on click */
            }
            .stButton > button.clicked {
                color: white;  /* Keep text color white when clicked */
                background-color: #45a049; /* Maintain the background color when clicked */
            }
        </style>
    """, unsafe_allow_html=True)

    
    # Create three columns for buttons
    col1, col2, col3 = st.columns(3)

    # Button for Diet Recommendations
    with col1:
        if st.button("Reommend Diet 🥗"):
            st.session_state.current_page = 'Diet Recommendations'
            st.rerun()

    # Button for Disease Detector
    with col2:
        if st.button("Detect Disease🦠"):
            st.session_state.current_page = 'Disease Detector'
            st.rerun()

    # Button for Exercise Recommender
    with col3:
        if st.button("Plan Workout 🏋️"):
            st.session_state.current_page = 'Exercise Recommender'
            st.rerun()

    # Second row of buttons
    col4, col5, col6 = st.columns(3)

    with col4:
        if st.button("Mental Health Bot 🧠"):
            st.session_state.current_page = 'Mental Health Bot'
            st.rerun()

    with col5:
        if st.button("Calculate Food Nutrients 🍽️"):
            st.session_state.current_page = 'Food Nutrient Calculator'
            st.rerun()

    # Add additional buttons as needed
    with col6:
        if st.button("Take Health Assessment📋"):
            st.session_state.current_page = 'Health Quiz'
            st.rerun()


    random_fact = random.choice(health_facts)
    st.markdown(f"""
        <div style='padding: 10px; margin: 10px; background-color: rgba(255, 255, 255, 0.1); border-radius: 8px;'>
            <p style='color: #00bcd4; font-size: 18px; margin: 0;'><strong> {random_fact} </strong></p>
        </div>
    """, unsafe_allow_html=True)

# Function for Diet Recommendations
def diet_recommendation():
    st.title("Diet Recommendations 🥗")
    st.subheader("Get personalized diet plans based on your age, weight, height, and preferences.")
    
    age = st.number_input("Age", min_value=0, max_value=120, step=1)
    height = st.number_input("Height (in cm)", min_value=0.0, step=0.1)
    weight = st.number_input("Weight (in kg)", min_value=0.0, step=0.1)
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])
    medical_conditions = st.text_input("Medical Conditions (if any)")
    specifications = st.text_area("Any specific dietary preferences or requirements or cusine type:")
    
    if st.button("Get Recommendations 🍽️"):
        prompt = (
            f"Provide diet plan for a {age}-year-old {gender} "
            f"with a height of {height} cm and a weight of {weight} kg. "
            f"Medical conditions: {medical_conditions}. "
            f"Specific requirements: {specifications}."
            """Please provide a light and balanced meal plan with options for breakfast, lunch, dinner, and snacks.
            It can have some visual elements as well like tables, charts, 
            graphs etc. Also, you can give a weekly plan for all the meals"""
        )
        
        response = get_gemini_response(prompt)
        st.write(response)

    navigation_buttons()


# Food Nutrient Calculator 

def food_nutrient_calculator():
    st.title("Food Nutrient Calculator 📋")
    st.subheader("Upload an image of food to get detailed nutritional information.")
    # Function to upload image to Gemini API
    def upload_to_gemini(path, mime_type="image/jpeg"):
        file = genai.upload_file(path, mime_type=mime_type)
        st.write(f"Uploaded file '{file.display_name}' as: {file.uri}")
        return file

    # Function to generate disease description from image
    def analyze_image(file_path):
        file = upload_to_gemini(file_path)
        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            generation_config={
                "temperature": 1,
                "top_p": 0.95,
                "top_k": 64,
                "max_output_tokens": 8192,
                "response_mime_type": "text/plain",
            },
        )

        chat_session = model.start_chat(
            history=[
                {
                    "role": "user",
                    "parts": [
                        file,
                        """You are an advanced food detection and nutritional information assistant. Your task is to analyze the uploaded image of food items and provide detailed nutritional information for each identifiable item.

### Instructions:
1. Identify Food Items: Carefully examine the image and identify all food items present.Then give details about the the food item tha has been detected, like the cuisine, and the place where it is from and some other details as well.
2. Provide Nutritional Information: For each identified food item, deliver the following information in a clear, organized, and easy-to-read format, like a table 
   - Food Item Name: The common name of the food item.
   - Nutritional Information (per 100 grams):
     - Calories: Total calories in kilocalories (kcal).
     - Protein: Total protein content in grams (g).
     - Carbohydrates: Total carbohydrates in grams (g).
     - Fats: Total fat content in grams (g).
     - Fiber: Total dietary fiber in grams (g).
     - Sugar: Total sugar content in grams (g).
     - Sodium: Total sodium content in milligrams (mg) if available.

3. Unknown Items: If any food item cannot be identified, state "Unknown food item" and provide general nutritional information if possible, or indicate that the item is not recognized.

### Output Format:
List each detected food item along with its nutritional information in the following format:
- Food Item Name:
  - Calories: [value] kcal
  - Protein: [value] g
  - Carbohydrates: [value] g
  - Fats: [value] g
  - Fiber: [value] g
  - Sugar: [value] g
  - Sodium: [value] mg (if applicable)

### Example Output:
- Apple:
  - Calories: 52 kcal
  - Protein: 0.3 g
  - Carbohydrates: 14 g
  - Fats: 0.2 g
  - Fiber: 2.4 g
  - Sugar: 10 g
  - Sodium: 1 mg

- Banana:
  - Calories: 89 kcal
  - Protein: 1.1 g
  - Carbohydrates: 23 g
  - Fats: 0.3 g
  - Fiber: 2.6 g
  - Sugar: 12 g
  - Sodium: 1 mg

If multiple food items are detected, separate them clearly with bullet points. Ensure the information is concise and easy to understand for users who may not have a background in nutrition.
""",
                    ],
                }
            ]
        )
        response = chat_session.send_message("""You are an advanced food detection and nutritional information assistant. Your task is to analyze the uploaded image of food items and provide detailed nutritional information for each identifiable item.

### Instructions:
1. Identify Food Items: Carefully examine the image and identify all food items present.Then give details about the the food item tha has been detected, like the cuisine, and the place where it is from and some other details as well.
2. Provide Nutritional Information: For each identified food item, deliver the following information in a clear, organized, and easy-to-read format:
   - Food Item Name: The common name of the food item.
   - Nutritional Information (per 100 grams):
     - Calories: Total calories in kilocalories (kcal).
     - Protein: Total protein content in grams (g).
     - Carbohydrates: Total carbohydrates in grams (g).
     - Fats: Total fat content in grams (g).
     - Fiber: Total dietary fiber in grams (g).
     - Sugar: Total sugar content in grams (g).
     - Sodium: Total sodium content in milligrams (mg) if available.

3. Unknown Items: If any food item cannot be identified, state "Unknown food item" and provide general nutritional information if possible, or indicate that the item is not recognized.

### Output Format:
List each detected food item along with its nutritional information in the following format:
- Food Item Name:
  - Calories: [value] kcal
  - Protein: [value] g
  - Carbohydrates: [value] g
  - Fats: [value] g
  - Fiber: [value] g
  - Sugar: [value] g
  - Sodium: [value] mg (if applicable)

### Example Output:
- Apple:
  - Calories: 52 kcal
  - Protein: 0.3 g
  - Carbohydrates: 14 g
  - Fats: 0.2 g
  - Fiber: 2.4 g
  - Sugar: 10 g
  - Sodium: 1 mg

- Banana:
  - Calories: 89 kcal
  - Protein: 1.1 g
  - Carbohydrates: 23 g
  - Fats: 0.3 g
  - Fiber: 2.6 g
  - Sugar: 12 g
  - Sodium: 1 mg

If multiple food items are detected, separate them clearly with bullet points. Ensure the information is concise and easy to understand for users who may not have a background in nutrition.""")
        return response.text

    st.write("Upload an image of the food")

    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        # Display the uploaded image
        image = Image.open(uploaded_file)
        st.image(image, caption='Uploaded Image',width=250)

        # Save the uploaded file locally to send to Gemini
        with open("temp_image.jpg", "wb") as f:
            f.write(uploaded_file.getbuffer())

        # Button to submit for analysis
        if st.button("Calculate nutrients 🔍"):
            st.write("Analyzing the image...")
            analysis_result = analyze_image("temp_image.jpg")
            st.write("Diagnosis:", analysis_result)


# Function for Exercise Recommender
def exercise_recommender():
    st.title("Exercise Recommender 🏋️")
    st.subheader("Receive a customized workout plan tailored to your fitness goals.")

    # Collect user information
    gender = st.selectbox("Select your gender:", ["Male", "Female", "Other"])
    age = st.number_input("Enter your age:", min_value=0, max_value=120, value=25)
    weight = st.number_input("Enter your weight (in kg):", min_value=1.0, value=70.0)
    height = st.number_input("Enter your height (in cm):", min_value=1, value=170)
    
    fitness_goals = st.text_input("Enter your fitness goals (e.g., lose weight, gain muscle):")
    fitness_level = st.selectbox("Select your fitness level:", ["Beginner", "Intermediate", "Advanced"])
    available_equipment = st.multiselect("Select available equipment:", ["None", "Dumbbells", "Resistance Bands", "Gym Access", "Bodyweight", "Cardio Equipment"])
    preferred_exercise_type = st.selectbox("Preferred exercise type:", ["Strength Training", "Cardio", "Flexibility", "Mixed"])
    medical_conditions = st.text_area("List any medical conditions or injuries (if any):", placeholder="e.g., back pain, asthma")

    if st.button("Get Recommendations 💪"):
        # Validate user input
        if fitness_goals:
            user_info = {
                "gender": gender,
                "age": age,
                "weight": weight,
                "height": height,
                "goals": fitness_goals,
                "level": fitness_level,
                "equipment": available_equipment,
                "exercise_type": preferred_exercise_type,
                "medical_conditions": medical_conditions
            }

            # Create a detailed prompt for the Gemini API
            prompt = (
                 f"Generate a personalized exercise plan for the following user information:\n"
                f"- **Gender**: {gender}\n"
                f"- **Age**: {age}\n"
                f"- **Weight**: {weight} kg\n"
                f"- **Height**: {height} cm\n"
                f"- **Fitness Goals**: {fitness_goals}\n"
                f"- **Fitness Level**: {fitness_level}\n"
                f"- **Available Equipment**: {', '.join(available_equipment)}\n"
                f"- **Preferred Exercise Type**: {preferred_exercise_type}\n"
                f"- **Medical Conditions**: {medical_conditions}\n\n"
                "Please provide the exercise plan with the following structure:\n"
                "1. **Exercise Recommendations**:\n"
                "   - Name of exercise\n"
                "   - Description of how to perform it\n"
                "   - Number of sets and repetitions\n"
                "2. **Precautions**:\n"
                "3. **Additional Resources**:\n"
                "   - Links to articles or videos about the exercises."
            )

            # Get response from the Gemini API
            response = get_gemini_response(prompt)
            st.write(response)
        else:
            st.warning("Please enter your fitness goals.")

    navigation_buttons()



# Function for Disease Detector
def disease_detector():
    st.title("Disease Detector 🦠")
    input_text = st.text_input("Describe your symptoms:")
    
    if st.button("Get Detection 🔍"):
        if input_text:
            response = get_gemini_response(f"""Based on the following symptoms: {input_text}, please provide a comprehensive analysis that includes:
                                            1. Possible Diseases: List potential diseases that may correspond with the described symptoms.
                                            2. Precautions: Provide a set of precautions that the person should take to mitigate the symptoms and avoid worsening the condition.
                                            3. Seriousness Assessment: Indicate whether the condition is serious or requires immediate attention based on the symptoms presented.

                                            Please ensure that the response is clear, concise, and informative, focusing solely on the information requested.""")
            st.write(response)
        else:
            st.warning("Please enter your symptoms.")

    navigation_buttons()



# Mental health bot
def mental_health_bot():
    st.title("Mental Health Bot🧠")
    st.subheader("Hi! I am Zoe. I'm here to help you out.")

    # Initialize chat history in session state
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []

    # Display chat history with styled bubbles
    for chat in st.session_state.chat_history:
        st.markdown(chat['user'], unsafe_allow_html=True)
        st.markdown(chat['bot'], unsafe_allow_html=True)

    # User input for mental health queries
    input_text = st.text_input("How are you feeling today? Do you need any help?", key="input")

    if st.button("Send 📩"):
        if input_text:
            user_message = f"<div style='text-align: right; color: #1e88e5; border-radius: 15px; padding: 10px; background-color: #bbdefb; margin-bottom: 10px;'>You: {input_text}</div>"
            st.session_state.chat_history.append({"user": user_message, "bot": ""})

            # Get response from the Gemini API with the improved prompt
            response = get_gemini_response(f"Please respond empathetically to this mental health inquiry: '{input_text}'. Keep your answer brief and focused on practical advice or encouragement. Personalize it based on the user's feelings and situation.")
            bot_message = f"<div style='text-align: left; color: #388e3c; border-radius: 15px; padding: 10px; background-color: #c8e6c9; margin-bottom: 10px;'>Zoe: {response}</div>"
            st.session_state.chat_history[-1]['bot'] = bot_message

            st.rerun()
        else:
            st.warning("Please enter your message.")

    # User Name and Affirmation
    user_name = st.text_input("Please enter your name:")

    if user_name:
        affirmation = random.choice([
            f"<div style='padding: 10px; background-color: #ffe0b2; border-radius: 8px; margin-top: 10px;'>{user_name}, you are enough! 🌟</div>",
            f"<div style='padding: 10px; background-color: #ffe0b2; border-radius: 8px; margin-top: 10px;'>{user_name}, your feelings are valid. 💖</div>",
            f"<div style='padding: 10px; background-color: #ffe0b2; border-radius: 8px; margin-top: 10px;'>{user_name}, take a deep breath. You are doing great! 🌈</div>",
            f"<div style='padding: 10px; background-color: #ffe0b2; border-radius: 8px; margin-top: 10px;'>{user_name}, it's okay to ask for help. You are not alone. 🤗</div>",
            f"<div style='padding: 10px; background-color: #ffe0b2; border-radius: 8px; margin-top: 10px;'>{user_name}, remember to take care of yourself today! 🌻</div>"
        ])
        st.markdown(affirmation, unsafe_allow_html=True)

    # Start New Conversation button
    if st.button("Start New Conversation"):
        st.session_state.chat_history = []
        st.experimental_rerun()
    navigation_buttons()



# Configure Gemini API
genai.configure(api_key=api_key)

# Create the model configuration
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 2048,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
)

def health_quiz():
    st.title("Health Assessment📋")
    st.write("Answer the following questions to get personalized health tips!")

    # Prompt for Gemini to generate quiz questions
    quiz_prompt = (
        "Create a short health quiz with 5 multiple-choice questions about lifestyle, "
        "exercise, sleep, diet, and mental well-being. Each question should have 3-4 options. "
        "After the quiz, analyze the answers and provide personalized health tips based on responses."
    )
    
    # Generate quiz questions using Gemini API
    chat_session = model.start_chat(history=[])
    quiz_response = chat_session.send_message(quiz_prompt).text
    
    # Example quiz questions (in case API does not generate output as expected)
    default_quiz = [
        {
            "question": "How often do you exercise?",
            "options": ["Daily", "A few times a week", "Once a week", "Rarely"],
        },
        {
            "question": "How many hours of sleep do you get each night?",
            "options": ["7-8 hours", "5-6 hours", "Less than 5 hours", "More than 8 hours"],
        },
        {
            "question": "How balanced is your diet?",
            "options": ["Very balanced", "Somewhat balanced", "Not very balanced", "I eat whatever I want"],
        },
        {
            "question": "How often do you feel stressed?",
            "options": ["Rarely", "Occasionally", "Frequently", "Always"],
        },
        {
            "question": "How much water do you drink daily?",
            "options": ["2+ liters", "1-2 liters", "Less than 1 liter", "Rarely drink water"],
        },
    ]
    
    # Parse or use default quiz questions
    try:
        quiz = eval(quiz_response)  # Using eval assuming Gemini provides a JSON-like string
    except:
        quiz = default_quiz
    
    # Initialize user responses
    user_responses = []
    
    # Display quiz questions and capture user responses
    for idx, q in enumerate(quiz):
        st.subheader(f"Q{idx + 1}: {q['question']}")
        answer = st.radio(f"Select your answer:", q['options'], key=f"q{idx}")
        user_responses.append(answer)
    
    if st.button("Submit Answers"):
        # Prepare prompt for Gemini to analyze the answers and give personalized tips
        answers_summary = ", ".join([f"{q['question']} - {a}" for q, a in zip(quiz, user_responses)])
        
        analysis_prompt = (
            f"Based on the user's health quiz responses, provide a comprehensive analysis and personalized health tips. "
    f"Here are the responses: {answers_summary}. "
    f"Analyze the responses across areas like physical activity, sleep quality, dietary balance, stress levels, and hydration habits. "
    f"For each area, provide specific, easy-to-follow tips. Focus on the following:\n\n"
    
    f"- **Physical Activity:** If responses indicate a lack of exercise, suggest basic, achievable steps to increase activity, such as short daily walks, stretching routines, or simple exercises that fit a beginner's schedule. "
    f"Recommend ways to build consistency over time, like setting small goals or finding enjoyable physical activities.\n\n"
    
    f"- **Sleep Quality:** If sleep is insufficient, give tips on improving sleep hygiene, like establishing a pre-sleep routine, limiting screen time before bed, and creating a restful sleep environment. "
    f"Suggest healthy, non-intrusive adjustments that promote relaxation and better sleep quality.\n\n"
    
    f"- **Dietary Balance:** Based on the user’s dietary habits, offer personalized nutrition tips such as adding more whole foods, reducing processed foods, and creating balanced meals with proteins, healthy fats, and carbohydrates. "
    f"Provide realistic dietary adjustments that fit into a busy lifestyle and suggest alternatives for favorite foods if diet is less balanced.\n\n"
    
    f"- **Stress Levels:** If stress is an issue, provide gentle stress management techniques like deep breathing exercises, short relaxation breaks during the day, or journaling. "
    f"Offer simple, practical ways to manage stress that don’t require extensive time or resources and suggest mindfulness practices if applicable.\n\n"
    
    f"- **Hydration:** If water intake is low, suggest easy ways to increase it, like carrying a water bottle, setting reminders to drink, or adding fruit for flavor. "
    f"Focus on practical hydration habits that users can implement effortlessly throughout their day.\n\n"
    
    f"Ensure that each recommendation is approachable, actionable, and specific to the user’s responses, with emphasis on gradual improvement rather than drastic changes. Provide the tips in a clean, readable format, ideally in bullet points or sections for each health area."
        )
        
        # Get health tips based on user responses
        tips_response = chat_session.send_message(analysis_prompt).text
        
        # Display tips in a formatted table
        st.subheader("Your Personalized Health Tips")
        st.write(tips_response)
    navigation_buttons()


# Function to interact with the Gemini API
def get_gemini_response(prompt):
    chat_session = model.start_chat(history=[])
    response = chat_session.send_message(prompt)
    return response.text

# Function for navigation buttons
def navigation_buttons():
    st.write("\n### Navigation")
    if st.button("Go to Home 🏠"):
        st.session_state.current_page = 'Home'
        st.experimental_rerun()


# Render the current page based on the button clicked
if st.session_state.current_page == 'Home':
    home()
elif st.session_state.current_page == 'Diet Recommendations':
    diet_recommendation()
elif st.session_state.current_page == 'Food Nutrient Calculator':
    food_nutrient_calculator()
elif st.session_state.current_page == 'Exercise Recommender':
    exercise_recommender()
elif st.session_state.current_page == 'Disease Detector':
    disease_detector()
elif st.session_state.current_page == 'Mental Health Bot':
    mental_health_bot()
elif st.session_state.current_page == 'Health Quiz':
    health_quiz()

#Footer
st.markdown(
    f"<footer style='text-align: center; margin-top: 45px; color: #777;'>"
    f"Made with ❤️ by Zoya Iftekhar"
    "</footer>",
    unsafe_allow_html=True
)
