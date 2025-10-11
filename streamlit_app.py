import streamlit as st
import requests

st.set_page_config(page_title="Car Knowledge Assistant", page_icon="🚗")

API_URL = "https://automotive-sales-knowledge-app.streamlit.app/"  # Change when deployed

st.title("🚗 Car Knowledge Assistant (VW ID.4)")
st.markdown("Ask questions about VW cars and get instant, manual-based answers.")

query = st.text_input("Enter your question:")
top_k = st.slider("Number of results", 1, 5, 3)

if st.button("Ask"):
    with st.spinner("Thinking..."):
        response = requests.post(f"{API_URL}/ask", json={"question": query, "top_k": top_k})
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == "blocked":
                st.warning("Blocked by Smart Language Model gateway: " + data["reason"])
            else:
                st.subheader("Answer:")
                st.write(data["answer"])
                st.caption(f"Processed query: {data['processed_question']}")
        else:
            st.error("API request failed. Make sure your FastAPI backend is running.")

st.divider()
st.caption("Powered by FastAPI + LangChain + Streamlit")
