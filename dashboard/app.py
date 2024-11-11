import streamlit as st
import requests
import time

st.markdown(
    """
    <style>
    .stButton>button { background-color: #4CAF50; color: white; }
    .stSidebar .stTextInput>div>input { color: black; font-weight: bold; }
    .stInfo { background-color: #EAF2F8; }
    </style>
    """, unsafe_allow_html=True
)

# Set up API endpoint
FASTAPI_URL = "http://app:8000"

# Sidebar for query inputs
st.sidebar.title("Query Options")
query = st.sidebar.text_input("Enter a search query:")
top_k = st.sidebar.slider("Number of similar records to retrieve", 1, 10, 5)
product_name = st.sidebar.text_input("Filter by Product Name (optional):")
product_type = st.sidebar.text_input("Filter by Product Type (optional):")
country_filter = st.sidebar.text_input("Filter by Country (optional):")

# Main UI configuration
st.title("LLM Data Engineering Dashboard")
st.markdown("This dashboard allows you to search for similar records and generate responses using RAG.")

# Style RAG response and record display
def display_rag_response(response):
    st.markdown("### Generated Response:")
    st.info(response)

def display_record(record):
    st.markdown(f"**User ID**: {record['user_id']}")
    st.markdown(f"**Country**: {record['country']}")
    st.markdown(f"**Review**: {record['review_text']}")
    st.markdown(f"**Product Name**: {record['product_name']}")
    st.markdown(f"**Product Type**: {record['product_type']}")
    st.markdown("---")

# Add a button to trigger query
if st.sidebar.button("Retrieve Similar Records"):
    if query:
        with st.spinner("Processing query..."):
            start_time = time.time()

            # Prepare request payload with optional filters
            payload = {
                "query": query,
                "top_k": top_k,
                "product_name": product_name if product_name else None,
                "product_type": product_type if product_type else None
            }

            try:
                response = requests.post(f"{FASTAPI_URL}/query/rag", json=payload)
                response.raise_for_status()

                response_time = time.time() - start_time
                st.sidebar.success(f"Response time: {response_time:.2f} seconds")

                response_data = response.json()
                rag_response = response_data.get("response", "No response generated.")
                display_rag_response(rag_response)

                st.subheader("Similar Records Found:")
                records = response_data.get("records", [])
                if country_filter:
                    records = [r for r in records if r["country"].lower() == country_filter.lower()]

                for record in records:
                    display_record(record)

                st.sidebar.write(f"**Total records retrieved:** {len(records)}")

            except requests.exceptions.RequestException as e:
                st.error("Error retrieving data.")
                st.error(str(e))
    else:
        st.warning("Please enter a query to retrieve similar records.")
