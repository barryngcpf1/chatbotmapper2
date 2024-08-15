import streamlit as st
from openai import OpenAI

#Front-End
with st.sidebar:
    st.markdown("<h1 style='text-align:center;font-family:Georgia'> Paper Please! </h1>",unsafe_allow_html=True)
    st.markdown("This app is designed to help folks like you and me write AOR papers easily.")    
    st.markdown("<h2 style='text-align:center;font-family:Georgia'>Features</h1>",unsafe_allow_html=True)
    st.markdown(" - 🤑 MoneyMentor FinanceGPT - This Bot is ready to answer your business needs")
    st.markdown("-------")
    openai_api_key = st.text_input('Enter OpenAI API Key', type='password')
    st.markdown("-------")
    st.markdown("<h1 style='text-align:center;font-family:Georgia'>🧾 Financial Report Generator</h1>",unsafe_allow_html=True)
    start_up_name=st.text_input("What is the name of your Start Up")
    start_up_description=st.text_input("Please describe what your start up is about and how you intend to generate revenue")
    sector = st.multiselect('What is your Start Up about', ["Technology and Software", "Healthcare and Biotechnology", "Agriculture and AgriTech", "E-commerce and Retail", "Fintech (Financial Technology)", "Food and Beverage", "Manufacturing and Industry", "Clean Energy and Sustainability", "Education and EdTech", "Transportation and Mobility", "Real Estate and Property Tech (PropTech)", "Entertainment and Media", "Travel and Tourism", "Social Impact and Nonprofits", "Space and Aerospace", "Fashion and Apparel", "Artificial Intelligence (AI) and Machine Learning (ML)", "LegalTech", "Blockchain and Cryptocurrency", "Sports and Fitness", "Gaming and Esports", "Cybersecurity", "AI in Healthcare (HealthTech)", "Supply Chain and Logistics", "Emerging Technologies"])
    funding = st.multiselect('What sort of Funding are you looking for ?', ["Angel Investment", "Venture Capital", "Seed Funding", "Series A Funding", "Series B Funding", "Series C Funding", "Crowdfunding", "Debt Financing", "Corporate Investment", "Government Grants", "Accelerator Programs", "Strategic Partnerships", "Initial Coin Offerings (ICOs)", "Initial Public Offerings (IPOs)", "Private Equity", "Convertible Notes", "Revenue-based Financing", "Equity Crowdfunding", "Strategic Investments"])
    st.markdown("-------")

    generatebutt=st.button("Generate Financial Report")


# Show title and description.
st.title("💬 Chatbot")
st.write(
    "This is a simple chatbot that uses OpenAI's GPT-3.5 model to generate responses. "
    "To use this app, you need to provide an OpenAI API key, which you can get [here](https://platform.openai.com/account/api-keys). "
)

# Ask user for their OpenAI API key via `st.text_input`.
# Alternatively, you can store the API key in `./.streamlit/secrets.toml` and access it
# via `st.secrets`, see https://docs.streamlit.io/develop/concepts/connections/secrets-management
openai_api_key = st.text_input("OpenAI API Key", type="password")
if not openai_api_key:
    st.info("Please add your OpenAI API key to continue.", icon="🗝️")
else:

    # Create an OpenAI client.
    client = OpenAI(api_key=openai_api_key)

    # Create a session state variable to store the chat messages. This ensures that the
    # messages persist across reruns.
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display the existing chat messages via `st.chat_message`.
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Create a chat input field to allow the user to enter a message. This will display
    # automatically at the bottom of the page.
    if prompt := st.chat_input("What is up?"):

        # Store and display the current prompt.
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate a response using the OpenAI API.
        stream = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )

        # Stream the response to the chat using `st.write_stream`, then store it in 
        # session state.
        with st.chat_message("assistant"):
            response = st.write_stream(stream)
        st.session_state.messages.append({"role": "assistant", "content": response})
