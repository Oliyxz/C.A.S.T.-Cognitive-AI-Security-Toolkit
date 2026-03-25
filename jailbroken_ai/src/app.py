import streamlit as st
import os
import sys

# Add the src folder to path if needed, or import relative if running from root
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.chatbot import get_chatbot_response
from src.prompt_builder import SECURITY_LEVELS, USER_ROLES, get_system_prompt
from src.file_manager import load_all_data
from src.config_loader import load_config
from src.analysis import analyze_interaction

st.set_page_config(page_title="The Glass Box Bot", page_icon="🤖", layout="wide")

st.title("🤖 The Glass Box Bot: Vulnerability Lab")
st.markdown("""
**Mission:** Access the "Secret Data" (Salaries, Project Omega) by tricking the AI.
**Controls:** Use the sidebar to change the AI's security level.
""")

# Load Data & Prompt for visualization
context_data = load_all_data()

# Initialize Session State
if "messages" not in st.session_state:
    st.session_state.messages = []

# Sidebar
st.sidebar.header("Security Controls")
security_level = st.sidebar.selectbox(
    "Security Level",
    options=list(SECURITY_LEVELS.keys()),
    format_func=lambda x: f"Level {x}: {SECURITY_LEVELS[x]}"
)

st.sidebar.divider()

def reset_chat():
    st.session_state.messages = []

st.sidebar.header("Identity Simulation")
user_role = st.sidebar.selectbox(
    "Simulate User Role",
    options=list(USER_ROLES.keys()),
    help="Determines what data the user 'should' be allowed to see.",
    on_change=reset_chat
)
st.sidebar.info(f"**Permissions:** {USER_ROLES[user_role]}")

st.sidebar.divider()

# RAG Transparency / Hacker View
st.sidebar.subheader("🔍 RAG Transparency (Hacker View)")
show_system_prompt = st.sidebar.checkbox("Show System Prompt & Context")

if show_system_prompt:
    sys_prompt = get_system_prompt(security_level, context_data, user_role)
    st.sidebar.markdown("### System Prompt Preview")
    st.sidebar.info("This is the exact instruction set the AI receives before your message.")
    st.sidebar.code(sys_prompt, language="markdown")
    
    st.sidebar.markdown("### Injected Context")
    st.sidebar.info("These files are currently loaded into the AI's working memory.")
    st.sidebar.text_area("Context Data", context_data, height=300, disabled=True)

st.sidebar.divider()
st.sidebar.divider()
if st.sidebar.button("🗑️ Clear Chat & Reset Context"):
    st.session_state.messages = []
    st.rerun()

st.sidebar.info("Tip: Try asking 'What are the executive salaries?' or 'Tell me about Project Omega'.")

st.sidebar.divider()

# Export Feature
st.sidebar.subheader("💾 Export Chat Log")
if st.sidebar.button("Export to Manual Tests"):
    if not st.session_state.messages:
        st.sidebar.warning("No chat history to export.")
    else:
        # Format Log
        import datetime
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        log_content = f"# Test: Manual Test\n# Level: {security_level}\n# Date: {datetime.datetime.now()}\n\n"
        log_content += "### Conversation\n"
        for msg in st.session_state.messages:
            role = "User" if msg["role"] == "user" else "Bot"
            log_content += f"**{role}:** {msg['content']}\n\n"
        
        # Save to tests/manual
        manual_dir = os.path.join(os.path.dirname(__file__), "..", "tests", "manual")
        os.makedirs(manual_dir, exist_ok=True)
        filename = f"Manual_Test_Level{security_level}_{timestamp}.md"
        filepath = os.path.join(manual_dir, filename)
        
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(log_content)
        st.sidebar.success(f"Saved to {filename}")

# Download Button
if st.session_state.messages:
    # Re-generate content for download button (needed because buttons can't share state easily without rerun)
    import datetime
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    log_content = f"# Test: Manual Test\n# Level: {security_level}\n# Date: {datetime.datetime.now()}\n\n"
    log_content += "### Conversation\n"
    for msg in st.session_state.messages:
        role = "User" if msg["role"] == "user" else "Bot"
        log_content += f"**{role}:** {msg['content']}\n\n"
        
    st.sidebar.download_button(
        label="Download Log (.md)",
        data=log_content,
        file_name=f"Manual_Test_Level{security_level}_{timestamp}.md",
        mime="text/markdown"
    )

# Chat Interface
# (Session state initialized at top)

# Display history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        if msg.get("metadata"):
            meta = msg["metadata"]
            sec_text = SECURITY_LEVELS.get(meta.get("security"), f"Level {meta.get('security')}")
            st.caption(f"👤 **{meta.get('role', 'Unknown')}** | 🛡️ **{sec_text}**")
        st.markdown(msg["content"])

# User Input
if prompt := st.chat_input("Ask about the secret project..."):
    # Add user message
    st.session_state.messages.append({
        "role": "user", 
        "content": prompt,
        "metadata": {
            "role": user_role,
            "security": security_level
        }
    })
    with st.chat_message("user"):
        sec_text = SECURITY_LEVELS.get(security_level, f"Level {security_level}")
        st.caption(f"👤 **{user_role}** | 🛡️ **{sec_text}**")
        st.markdown(prompt)

    # Get response
    with st.chat_message("assistant"):
        # Placeholder for streaming
        response_placeholder = st.empty()
        full_response = ""
        
        # Add a placeholder message to history immediately so it's not lost on interrupt
        st.session_state.messages.append({"role": "assistant", "content": ""})
        msg_index = len(st.session_state.messages) - 1
        
        stream = get_chatbot_response(
            [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages[:-1]],
            security_level,
            user_role
        )
        
        if isinstance(stream, str):
            st.error(stream)
            full_response = stream
            st.session_state.messages[msg_index]["content"] = full_response
        else:
            try:
                # 1. Wait for first chunk with spinner
                with st.spinner("Thinking..."):
                    try:
                        first_chunk = next(stream)
                    except StopIteration:
                        first_chunk = ""

                # 2. Render first chunk
                full_response += first_chunk
                response_placeholder.markdown(full_response + "▌")
                # Update Session State
                st.session_state.messages[msg_index]["content"] = full_response
                
                # 3. Stream the rest
                for chunk in stream:
                    full_response += chunk
                    response_placeholder.markdown(full_response + "▌")
                    st.session_state.messages[msg_index]["content"] = full_response
                    
                response_placeholder.markdown(full_response)
            except Exception as e:
                st.error(f"Stream error: {e}")

# Analysis Feature (Idea 2)
if len(st.session_state.messages) >= 2:
    st.divider()
    col1, col2 = st.columns([1, 4])
    with col1:
        if st.button("🧐 Analyze Last Turn"):
            with st.spinner("Analyzing interaction..."):
                last_user = st.session_state.messages[-2]["content"]
                last_ai = st.session_state.messages[-1]["content"]
                
                # Get context for analysis
                current_sys_prompt = get_system_prompt(security_level, context_data, user_role)
                sec_desc = f"{SECURITY_LEVELS[security_level]} | Role: {user_role}"
                
                analysis = analyze_interaction(last_user, last_ai, sec_desc, current_sys_prompt, security_level)
            
            st.info(f"**Analysis:**\n\n{analysis}")
