import streamlit as st
import pandas as pd

# Set page configuration
st.set_page_config(
    page_title="INTER DESIGN",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
st.markdown("""
<style>
    /* Sidebar styling */
    .css-1d391kg {
        background-color: #212130;
    }
    
    /* Main header */
    .main-header {
        background-color: #673AB7;
        padding: 15px;
        color: white;
        font-size: 18px;
        font-weight: bold;
        margin-bottom: 20px;
        border-radius: 5px;
    }
    
    /* Step indicators */
    .step-container {
        display: flex;
        justify-content: space-between;
        margin-bottom: 30px;
    }
    
    .step {
        display: flex;
        flex-direction: column;
        align-items: center;
    }
    
    .step-circle {
        width: 30px;
        height: 30px;
        border-radius: 50%;
        background-color: #ccc;
        display: flex;
        justify-content: center;
        align-items: center;
        color: white;
        font-weight: bold;
        margin-bottom: 5px;
    }
    
    .step-active {
        background-color: #673AB7;
    }
    
    .step-text {
        font-size: 12px;
        text-align: center;
    }
    
    /* Form styling */
    .form-container {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    
    .form-section-title {
        font-weight: bold;
        margin-bottom: 15px;
    }
    
    /* Color selector */
    .color-container {
        display: flex;
        gap: 10px;
        margin-top: 10px;
    }
    
    .color-circle {
        width: 30px;
        height: 30px;
        border-radius: 50%;
        cursor: pointer;
    }
    
    .color-circle-selected {
        border: 2px solid #673AB7;
    }
    
    /* Button styling */
    .button-primary {
        background-color: #ff5252;
        color: white;
        padding: 8px 16px;
        border: none;
        border-radius: 5px;
        cursor: pointer;
    }
    
    .token-template {
        padding: 15px;
        border-radius: 5px;
        margin: 5px;
        text-align: center;
        cursor: pointer;
    }
    
    .token-template-selected {
        border: 2px solid #673AB7;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown('<div style="display: flex; justify-content: center; margin-bottom: 20px;"><div style="width: 60px; height: 60px; background-color: #673AB7; border-radius: 50%; display: flex; justify-content: center; align-items: center; color: white; font-weight: bold;">ID</div></div>', unsafe_allow_html=True)
    
    menu_items = {
        "หน้าหลัก": "🏠",
        "สร้างโทเค็น": "🪙",
        "โปรเจคของฉัน": "📝",
        "ซื้อ Token": "🎟️",
        "ด้านราคาฯ": "💰",
        "ประวัติการใช้งาน": "📊",
        "ตั้งค่าบัญชี": "⚙️"
    }
    
    for item, icon in menu_items.items():
        bg_color = "#673AB7" if item == "สร้างโทเค็น" else "transparent"
        text_color = "white"
        st.markdown(f"""
        <div style="padding: 10px; background-color: {bg_color}; margin-bottom: 5px; border-radius: 5px;">
            <span style="color: {text_color};">{icon} {item}</span>
        </div>
        """, unsafe_allow_html=True)

# Main content
st.markdown('<div class="main-header">INTER DESIGN | 10 Tokens</div>', unsafe_allow_html=True)

# Top navigation tabs
tabs = st.tabs(["สร้างโทเค็น", "ซื้อ Token", "โปรเจคของฉัน", "ด้านราคาฯ"])

with tabs[0]:
    # Header section
    st.markdown("<h2>สร้างโทเค็นใหม่</h2>", unsafe_allow_html=True)
    
    # Step indicators
    st.markdown("""
    <div class="step-container">
        <div class="step">
            <div class="step-circle step-active">1</div>
            <div class="step-text">ข้อมูล</div>
        </div>
        <div class="step">
            <div class="step-circle">2</div>
            <div class="step-text">สเปค</div>
        </div>
        <div class="step">
            <div class="step-circle">3</div>
            <div class="step-text">เลือกแพ็คเกจ</div>
        </div>
        <div class="step">
            <div class="step-circle">4</div>
            <div class="step-text">ยืนยัน</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Form container
    st.markdown('<div class="form-container">', unsafe_allow_html=True)
    
    # Basic information section
    st.markdown('<div class="form-section-title">ข้อมูลพื้นฐาน</div>', unsafe_allow_html=True)
    
    # Form fields
    st.markdown("<p>ชื่อโปรเจค</p>", unsafe_allow_html=True)
    project_name = st.text_input("", placeholder="ตัวอย่างเช่น โทเค็นบริหารชุมชน", label_visibility="collapsed")
    
    st.markdown("<p>ประเภทโทเค็น</p>", unsafe_allow_html=True)
    token_type = st.selectbox("", ["เลือกประเภท"], label_visibility="collapsed")
    
    st.markdown("<p>จำนวนโทเค็น (สูงสุด)</p>", unsafe_allow_html=True)
    token_amount = st.text_input("", value="35", label_visibility="collapsed")
    
    st.markdown("<p>รูปแบบโทเค็น</p>", unsafe_allow_html=True)
    token_format = st.selectbox("", ["เหรียญเสมือน"], label_visibility="collapsed")
    
    st.markdown("<p>รายละเอียดเพิ่มเติม</p>", unsafe_allow_html=True)
    additional_details = st.text_area("", placeholder="อธิบายว่าเหรียญโทเค็น ใช้ทำอะไร มีประโยชน์อย่างไรกับผู้ถือ", height=100, label_visibility="collapsed")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Template selection
    st.markdown('<div class="form-section-title">เลือกการออกแบบ</div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="token-template token-template-selected" style="background-color: #f0f0f0;">
            <p>โทเค็น</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="token-template" style="background-color: #f0f0f0;">
            <p>มินิมอล</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="token-template" style="background-color: #f0f0f0;">
            <p>แบบหลายเหลี่ยม</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="token-template" style="background-color: #f0f0f0;">
            <p>ออกแบบเอง</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Color selection
    st.markdown('<div class="form-section-title" style="margin-top: 20px;">โทนสี</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="color-container">
        <div class="color-circle color-circle-selected" style="background-color: #5D4397;"></div>
        <div class="color-circle" style="background-color: #FFB6B9;"></div>
        <div class="color-circle" style="background-color: #FFE7A0;"></div>
        <div class="color-circle" style="background-color: #8CD4CB;"></div>
        <div class="color-circle" style="background-color: #9EECA1;"></div>
    </div>
    <div style="display: flex; margin-top: 5px;">
        <small style="margin-right: 25px;">สีม่วงไทย</small>
        <small style="margin-right: 25px;">โมโนโทน</small>
        <small style="margin-right: 25px;">พาสเทล</small>
        <small style="margin-right: 25px;">สีฟ้า</small>
        <small>สีเขียว</small>
    </div>
    """, unsafe_allow_html=True)
    
    # Payment information
    st.markdown("""
    <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 30px; padding: 10px; background-color: #f5f5f5; border-radius: 5px;">
        <div>การสร้างโทเค็นนี้ใช้ไป 1 Token</div>
        <div>Token คงเหลือ: 10 ดวง</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Action buttons
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        st.button("ยกเลิก", use_container_width=True)
    
    with col2:
        st.markdown("""
        <button style="width: 100%; background-color: #673AB7; color: white; padding: 10px; border: none; border-radius: 5px;">บันทึกแล้วทำต่อภายหลัง</button>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <button style="width: 100%; background-color: #4CAF50; color: white; padding: 10px; border: none; border-radius: 5px;">สร้างการออกแบบทันที</button>
        """, unsafe_allow_html=True)
    
    # Disclaimer footer
    st.markdown("""
    <div style="background-color: #e3f2fd; padding: 15px; border-radius: 5px; margin-top: 20px; font-size: 14px;">
        <p>โปรดทราบ : เพียงการคลิกยืนยันชำระหรือทำรายการใดๆ ให้ถือว่ายินยอมตามข้อกำหนดและเงื่อนไขของเราทุกประการ</p>
    </div>
    """, unsafe_allow_html=True)
