import streamlit as st
import time
import random
import streamlit.components.v1 as components
import base64

# -------------------------
# PAGE SETTINGS
# -------------------------
st.set_page_config(page_title="🎵 리듬게임 Ultimate Edition", layout="centered")
st.title("🎵 Streamlit 리듬게임 Ultimate Edition")

st.write("스페이스바를 리듬에 맞춰 누르세요!")

# -------------------------
# LOAD SOUNDS (base64)
# -------------------------
def load_sound(path):
    with open(path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

perfect_snd = load_sound("perfect.wav")
good_snd = load_sound("good.wav")
miss_snd = load_sound("miss.wav")

# JavaScript for playing sounds
sound_js = f"""
<script>
function playSound(type) {{
    var audio = new Audio();
    if (type === 'perfect') audio.src = "data:audio/wav;base64,{perfect_snd}";
    if (type === 'good') audio.src = "data:audio/wav;base64,{good_snd}";
    if (type === 'miss') audio.src = "data:audio/wav;base64,{miss_snd}";
    audio.play();
}}
</script>
"""
components.html(sound_js, height=0)

# -------------------------
# KEYBOARD CAPTURE
# -------------------------
keyboard_js = """
<script>
let lastKey = "";
document.addEventListener('keydown', function(e) {
    lastKey = e.key;
    window.parent.postMessage({"keyPressed": lastKey}, "*");
});
</script>
"""
components.html(keyboard_js, height=0)

listener = """
<script>
window.addEventListener("message", (event) => {
    const urlParams = new URLSearchParams(window.location.search);
    urlParams.set('keyPressed', event.data.keyPressed);
    window.location.search = urlParams.toString();
});
</script>
"""
components.html(listener, height=0)

# -------------------------
# INITIAL STATE
# -------------------------
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'combo' not in st.session_state:
    st.session_state.combo = 0
if 'target_time' not in st.session_state:
    st.session_state.target_time = time.time() + 3
if 'speed' not in st.session_state:
    st.session_state.speed = 1.0

# -------------------------
# DIFFICULTY SETTINGS
# -------------------------
st.subheader("난이도 선택")
diff = st.radio("", ["Easy", "Normal", "Hard"], horizontal=True)
if diff == "Easy":
    st.session_state.speed = 1.4
elif diff == "Normal":
    st.session_state.speed = 1.0
else:
    st.session_state.speed = 0.75

# -------------------------
# VISUAL NOTE FALLING
# -------------------------
st.markdown("<br><br>", unsafe_allow_html=True)

now = time.time()
remaining = st.session_state.target_time - now

if remaining > 1:
    height = 50
elif remaining > 0:
    height = int((1 - remaining) * 200)
else:
    height = 260  # Hit zone

note_html = f"""
<div style='width:100%; height:300px; border:1px solid #999; position:relative;'>
    <div style='width:40px; height:40px; background:#4fa3ff; border-radius:5px; position:absolute; left:calc(50% - 20px); top:{height}px;'></div>
    <div style='position:absolute; bottom:10px; left:calc(50% - 40px); width:80px; height:5px; background:#ff4081;'></div>
</div>
"""
st.markdown(note_html, unsafe_allow_html=True)

# -------------------------
# KEYBOARD INPUT
# -------------------------
keyboard_event = st.experimental_get_query_params().get("keyPressed", None)

if keyboard_event:
    key = keyboard_event[0]
    if key == " ":
        diff = abs(time.time() - st.session_state.target_time)
        if diff < 0.12:
            st.session_state.score += 300 + st.session_state.combo * 10
            st.session_state.combo += 1
            components.html("<script>playSound('perfect');</script>", height=0)
            st.success("✨ PERFECT!")
        elif diff < 0.25:
            st.session_state.score += 100
            st.session_state.combo += 1
            components.html("<script>playSound('good');</script>", height=0)
            st.info("👍 GOOD!")
        else:
            st.session_state.combo = 0
            components.html("<script>playSound('miss');</script>", height=0)
            st.error("💀 MISS!")

        st.session_state.target_time = time.time() + random.uniform(1.0, 2.0) * st.session_state.speed

# -------------------------
# SCORE PANEL
# -------------------------
st.markdown("---")
st.subheader(f"점수: {st.session_state.score}")
st.write(f"콤보: {st.session_state.combo}")

# -------------------------
# RESET
# -------------------------
st.button("🔄 게임 리셋", on_click=lambda: st.session_state.update(score=0, combo=0, target_time=time.time()+2))
