import streamlit as st
from google import genai
from google.genai import types

st.set_page_config(page_title="Crypto Agent", page_icon="📈")
st.title("📈 Crypto Agent")
st.caption("Ask about any coin: news, risks, and global effects. This is information, not financial advice.")

client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

SYSTEM = """You are a crypto research assistant. For every question, search the web for the latest
public news and data. Cover: price trend, project or software changes, and global effects such as
wars, AI and data-center demand, mining company results and margins, ETF flows, interest rates and
government rules. Explain clearly whether each factor can push the price up or down, and how risky it is.
Use simple language. Never claim certainty about future prices. Only use public information.
End with a short reminder that this is not financial advice."""

if "messages" not in st.session_state:
    st.session_state.messages = []

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

question = st.chat_input("Ask about Bitcoin, Ethereum, or any coin...")

if question:
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)

    contents = [
        types.Content(
            role="user" if m["role"] == "user" else "model",
            parts=[types.Part(text=m["content"])],
        )
        for m in st.session_state.messages
    ]

    with st.chat_message("assistant"):
        with st.spinner("Searching the latest news..."):
            response = client.models.generate_content(
                model="gemini-3.8-flash",
                contents=contents,
                config=types.GenerateContentConfig(
                    system_instruction=SYSTEM,
                    tools=[types.Tool(google_search=types.GoogleSearch())],
                ),
            )
            answer = response.text
        st.markdown(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})
