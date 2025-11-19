# app.py
import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

st.set_page_config(page_title="Level → DPS 모델러", layout="wide")

st.title("스텔라소라 — 레벨별 DPS 모델러")
st.markdown(
    """
    이 도구는 캐릭터의 **공격력 성장식**과 **스킬·크리·공속** 파라미터를 넣으면
    레벨에 따른 추정 **DPS(초당 피해)** 변화를 계산해주고 표/그래프로 보여줍니다.
    """
)

# -----------------------
# 사이드바: 입력
# -----------------------
st.sidebar.header("기본 설정")

# Levels
min_level = st.sidebar.number_input("최소 레벨", min_value=1, max_value=999, value=1, step=1)
max_level = st.sidebar.number_input("최대 레벨", min_value=1, max_value=999, value=80, step=1)
if max_level < min_level:
    st.sidebar.error("최대 레벨은 최소 레벨보다 같거나 커야 합니다.")
levels = np.arange(min_level, max_level + 1)

st.sidebar.subheader("공격력(ATK) 성장")
base_atk = st.sidebar.number_input("기본 ATK (레벨 1)", min_value=0.0, value=100.0, step=1.0)
growth_mode = st.sidebar.radio("성장 방식", ("선형(고정값/레벨)", "퍼센트(비율/레벨)"))

if growth_mode == "선형(고정값/레벨)":
    atk_per_level = st.sidebar.number_input("레벨 당 ATK 증가량", value=5.0, step=0.1)
    def atk_at_level(lv):
        return base_atk + (lv - 1) * atk_per_level
else:
    atk_pct_per_level = st.sidebar.number_input("레벨 당 ATK 증가 비율(%)", value=2.0, step=0.01)
    def atk_at_level(lv):
        return base_atk * ((1 + atk_pct_per_level / 100) ** (lv - 1))

st.sidebar.subheader("딜 계산 요소")
# Skill / ability multiplier
skill_multiplier = st.sidebar.number_input("스킬 계수 (예: 2.5 = 공격력의 250%)", min_value=0.0, value=1.0, step=0.01)
# Additional flat or additive damage (optional)
flat_damage = st.sidebar.number_input("스킬 고정 피해 (평균, 한 회당)", min_value=0.0, value=0.0, step=1.0)

# Crit
crit_rate = st.sidebar.slider("치명 확률(%)", min_value=0.0, max_value=100.0, value=20.0, step=0.1) / 100.0
crit_damage = st.sidebar.slider("치명 피해 보정(치명시 추가 비율, %)", min_value=0.0, max_value=500.0, value=50.0, step=1.0) / 100.0

# Attack speed (공격/초)
attack_speed = st.sidebar.number_input("기본 공격속도(공격/초)", min_value=0.01, value=1.0, step=0.01)

# Damage type: single-hit or multi-hit / hits per attack
hits_per_attack = st.sidebar.number_input("공격당 히트 수(한 공격에 여러 히트 시)", min_value=1, value=1, step=1)

st.sidebar.markdown("---")
st.sidebar.write("추가 옵션")
# Level dependent multipliers (예: 스킬 레벨에 따른 계수 보정 입력)
use_skill_scaling = st.sidebar.checkbox("스킬 계수의 레벨별 성장 사용", value=False)
if use_skill_scaling:
    skill_scale_per_level = st.sidebar.number_input("레벨당 스킬 계수 증가량", value=0.0, step=0.01)
else:
    skill_scale_per_level = 0.0

# -----------------------
# 계산
# -----------------------
@st.cache_data
def compute_table(levels):
    atk_vals = np.array([atk_at_level(lv) for lv in levels])
    skill_coeffs = skill_multiplier + skill_scale_per_level * (levels - 1)
    # 평균 피해(한 공격 기준) = (ATK * skill_coeff + flat) * (1 + crit_rate * crit_damage) * hits_per_attack
    avg_damage_per_attack = (atk_vals * skill_coeffs + flat_damage) * (1 + crit_rate * crit_damage) * hits_per_attack
    dps_vals = avg_damage_per_attack * attack_speed
    df = pd.DataFrame({
        "level": levels,
        "ATK": np.round(atk_vals, 4),
        "skill_coeff": np.round(skill_coeffs, 4),
        "avg_damage_per_attack": np.round(avg_damage_per_attack, 4),
        "attack_speed": attack_speed,
        "DPS": np.round(dps_vals, 4)
    })
    return df

df = compute_table(levels)

# -----------------------
# UI: 요약 카드
# -----------------------
col1, col2, col3 = st.columns(3)
col1.metric("레벨 범위", f"{min_level} → {max_level}")
col2.metric("기본 ATK (레벨1)", f"{base_atk:.1f}")
col3.metric("기준 DPS (선택 레벨)", f"{df.loc[df.index[0], 'DPS']:.2f}")

st.markdown("---")

# -----------------------
# 메인: 표와 그래프
# -----------------------
st.subheader("레벨별 DPS 표")
st.dataframe(df.style.format({"ATK": "{:.2f}", "skill_coeff": "{:.3f}", "avg_damage_per_attack": "{:.2f}", "DPS": "{:.2f}"}), use_container_width=True)

st.subheader("레벨별 DPS 그래프")
chart = alt.Chart(df).mark_line(point=True).encode(
    x="level:Q",
    y=alt.Y("DPS:Q", title="DPS"),
    tooltip=["level", "ATK", "skill_coeff", "avg_damage_per_attack", "DPS"]
).interactive()
st.altair_chart(chart, use_container_width=True)

# Highlight: DPS 증가율(초기→최종)
dps_start = df.loc[0, "DPS"]
dps_end = df.loc[df.index[-1], "DPS"]
if dps_start == 0:
    pct_gain = np.inf
else:
    pct_gain = (dps_end / dps_start - 1) * 100.0

st.markdown(f"**초기 DPS (레벨 {min_level}):** {dps_start:.2f}    ·    **최종 DPS (레벨 {max_level}):** {dps_end:.2f}    ·    **증가:** {pct_gain:.2f}%")

# -----------------------
# 다운로드
# -----------------------
st.markdown("---")
st.subheader("데이터 다운로드")
csv = df.to_csv(index=False).encode("utf-8")
st.download_button("CSV로 저장", csv, file_name=f"dps_by_level_{min_level}-{max_level}.csv", mime="text/csv")

# -----------------------
# 간단한 해석 텍스트 출력
# -----------------------
st.markdown("---")
st.subheader("간단한 해석 포인트")
st.write("""
- ATK 성장 방식(선형 vs 퍼센트)에 따라 DPS 곡선 모양이 달라집니다.
- 스킬 계수(또는 스킬 레벨 성장)를 올리면 DPS가 비선형으로 크게 증가할 수 있습니다.
- 치명 확률/치명 피해는 평균 피해를 선형으로 증가시키므로 DPS를 빠르게 끌어올리는 요소입니다.
- 공격속도는 DPS에 선형으로 곱해집니다. (공속 2배 → DPS 2배)
""")

st.info("이 도구는 단순 모델입니다. 스킬 쿨다운, 버프/디버프, 적 방어/감소 등 복잡한 요소는 반영되지 않습니다.")
