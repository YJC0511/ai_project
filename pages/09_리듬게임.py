import streamlit as st
import time
import random
import streamlit.components.v1 as components

st.set_page_config(page_title="리듬 게임", layout="centered")

st.title("🎵 Streamlit 리듬 게임 (Keyboard Input Edition)")

st.write("스페이스바가 떨어지는 박자에 맞춰 누르세요!")

# Inject JavaScript to capture keyboard events
keyboard_js = """
<script>
let lastKey = "";

document.addEventListener('keydown', function(e) {
    lastKey = e.key;
    // send key to streamlit
    window.parent.postMessage({"keyPressed": lastKey}, "*");
});
</script>
"""
components.html(keyboard_js, height=0)

# Placeholder to receive JS messages
key_placeholder = st.empty()

# Session state
if 'score' not in st.session_state:
    st.session_state.score = 0

if 'target_time' not in st.session_state:
    st.session_state.target_time = time.time() + random.uniform(2, 4)

st.subheader(f"점수: {st.session_state.score}")

# Show a countdown / note falling
now = time.time()
remaining = st.session_state.target_time - now

if remaining > 1:
    st.write("노트 준비 중...")
elif remaining > 0:
    st.write("🎵 노트 떨어지는 중! 스페이스바 눌러!!")
else:
    st.write("❗ 지금 눌러!!")

# Receive keyboard events from JS
keyboard_event = st.experimental_get_query_params().get("keyPressed", None)

# Create a hidden iframe to listen for postMessage events
listener = """
<script>
window.addEventListener("message", (event) => {
    const queryString = window.location.search;
    const urlParams = new URLSearchParams(queryString);
    urlParams.set('keyPressed', event.data.keyPressed);
    window.location.search = urlParams.toString();
});
</script>
"""
components.html(listener, height=0)

# Game logic
if keyboard_event:
    key = keyboard_event[0]
    key_placeholder.write(f"입력 감지됨: {key}")

    if key == " ":
        diff = abs(time.time() - st.session_state.target_time)
        if diff < 0.15:
            st.success("✨ PERFECT!")
            st.session_state.score += 300
        elif diff < 0.3:
            st.info("👍 GOOD!")
            st.session_state.score += 100
        else:
            st.error("💀 MISS!")
        # reset note
        st.session_state.target_time = time.time() + random.uniform(2, 4)
        time.sleep(0.2)

st.button("🔄 게임 리셋", on_click=lambda: st.session_state.update(score=0, target_time=time.time()+2))
