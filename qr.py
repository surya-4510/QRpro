import streamlit as st
import qrcode
from PIL import Image
import numpy as np
import cv2
import os
import io
from datetime import datetime

# ======================================================
# PAGE CONFIG
# ======================================================
st.set_page_config("QR Code Studio", page_icon="📌", layout="wide")

# ======================================================
# 🌈 ATTRACTIVE UI DESIGN
# ======================================================
st.markdown("""
<style>

/* Gradient Background */
.stApp {
    background: linear-gradient(135deg, #ffecd2, #fcb69f, #a1c4fd, #c2e9fb);
    background-size: 400% 400%;
    animation: gradientBG 10s ease infinite;
    font-family: 'Poppins', sans-serif;
}

@keyframes gradientBG {
    0% {background-position: 0% 50%;}
    50% {background-position: 100% 50%;}
    100% {background-position: 0% 50%;}
}

/* Header */
h1 {
    text-align: center;
    font-size: 55px;
    font-weight: 900;
    color: #1e293b;
}

/* Subtitle */
.subtitle {
    text-align: center;
    font-size: 20px;
    font-weight: 600;
    color: #334155;
    margin-bottom: 30px;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: rgba(255,255,255,0.8);
    border-right: 2px solid #94a3b8;
}
section[data-testid="stSidebar"] * {
    color: #1e293b !important;
    font-weight: 700;
}

/* Glass Cards */
.card {
    background: rgba(255,255,255,0.85);
    border-radius: 25px;
    padding: 25px;
    margin: 20px;
    box-shadow: 0px 10px 25px rgba(0,0,0,0.15);
    border: 2px solid rgba(255,255,255,0.4);
}

/* Buttons */
div.stButton > button {
    background: linear-gradient(to right, #ff512f, #dd2476);
    color: white !important;
    border-radius: 18px;
    padding: 14px 28px;
    font-size: 18px;
    font-weight: bold;
    border: none;
    transition: 0.3s;
}
div.stButton > button:hover {
    transform: scale(1.08);
    background: linear-gradient(to right, #dd2476, #ff512f);
}

/* Inputs */
input, textarea {
    border-radius: 12px !important;
    border: 2px solid #94a3b8 !important;
    padding: 10px;
}

</style>
""", unsafe_allow_html=True)

# ======================================================
# HEADER
# ======================================================
st.markdown("<h1>✨📌 QR Code Studio</h1>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>📷 Scanner • 🎨 Generator • 🕘 History Manager</div>",
            unsafe_allow_html=True)

# ======================================================
# STORAGE SETUP
# ======================================================
SAVE_FOLDER = "saved_qr_codes"
os.makedirs(SAVE_FOLDER, exist_ok=True)

DATA_FILE = os.path.join(SAVE_FOLDER, "qr_data.txt")

# ======================================================
# SIDEBAR MENU
# ======================================================
menu = st.sidebar.radio(
    "🌟 Choose Feature",
    ["📷 QR Scanner", "🎨 QR Generator", "🕘 QR History"]
)

# ======================================================
# 📷 QR SCANNER
# ======================================================
if menu == "📷 QR Scanner":

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("📷 QR Code Scanner")

    qr_detector = cv2.QRCodeDetector()
    tab1, tab2 = st.tabs(["📸 Live Scan", "🖼 Upload Image Scan"])

    # Live Scan
    with tab1:
        st.info("💡 Note: For security reasons, web browsers require you to click 'Take Photo' to scan.")
        
        img_file_buffer = st.camera_input("📷 Scan QR Code")

        if img_file_buffer is not None:
            # Convert the file buffer to an opencv image
            bytes_data = img_file_buffer.getvalue()
            cv2_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)

            # Detect and Decode
            data, bbox, _ = qr_detector.detectAndDecode(cv2_img)

            if data:
                st.success("✅ QR Detected!")
                st.code(data)

                if data.startswith("http"):
                    st.markdown(f"🔗 Link: [{data}]({data})")
            else:
                st.warning("⚠️ No QR code detected in the image. Please try again.")

    # Upload Scan
    with tab2:
        uploaded = st.file_uploader("📂 Upload QR Image", type=["png", "jpg", "jpeg"])

        if uploaded:
            img = Image.open(uploaded).convert("RGB")
            st.image(img)

            img_np = np.array(img)
            data, bbox, _ = qr_detector.detectAndDecode(img_np)

            if data:
                st.success("✅ QR Code Found!")
                st.code(data)
            else:
                st.error("❌ No QR Found")

    st.markdown("</div>", unsafe_allow_html=True)

# ======================================================
# 🎨 QR GENERATOR
# ======================================================
elif menu == "🎨 QR Generator":

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("🎨 QR Code Generator")

    qr_type = st.radio(
        "Select Type:",
        ["🌍 URL/Text → QR", "🖼 Image → QR", "🎬 Video → QR"]
    )

    data = ""

    if qr_type == "🌍 URL/Text → QR":
        data = st.text_input("Enter URL or Text")

    elif qr_type == "🖼 Image → QR":
        img_file = st.file_uploader("Upload Image", type=["png", "jpg", "jpeg"])
        if img_file:
            data = img_file.name
            st.image(img_file)

    elif qr_type == "🎬 Video → QR":
        vid_file = st.file_uploader("Upload Video", type=["mp4", "mov", "avi"])
        if vid_file:
            data = vid_file.name
            st.video(vid_file)

    st.divider()

    st.subheader("🎨 Customize QR Design")

    col1, col2 = st.columns(2)

    with col1:
        qr_color = st.color_picker("QR Color", "#000000")
        box_size = st.slider("QR Size", 5, 20, 10)

    with col2:
        bg_color = st.color_picker("Background Color", "#FFFFFF")
        border_size = st.slider("Border Thickness", 1, 10, 4)

    if st.button("✨ Generate QR Code"):

        if data.strip() == "":
            st.warning("⚠ Please enter input!")
        else:
            qr = qrcode.QRCode(box_size=box_size, border=border_size)
            qr.add_data(data)
            qr.make(fit=True)

            img_qr = qr.make_image(
                fill_color=qr_color,
                back_color=bg_color
            ).convert("RGB")

            st.success("🎉 QR Code Generated!")
            st.image(img_qr, width=280)

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"QR_{timestamp}.png"
            filepath = os.path.join(SAVE_FOLDER, filename)
            img_qr.save(filepath)

            with open(DATA_FILE, "a") as f:
                f.write(f"{filename}||{data}\n")

            buffer = io.BytesIO()
            img_qr.save(buffer, format="PNG")
            buffer.seek(0)

            st.download_button("⬇ Download QR Code", buffer, filename)

    st.markdown("</div>", unsafe_allow_html=True)

# ======================================================
# 🕘 HISTORY + DELETE
# ======================================================
elif menu == "🕘 QR History":

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("🕘 QR Code History")

    if not os.path.exists(DATA_FILE):
        st.warning("No QR Codes Generated Yet.")
    else:
        with open(DATA_FILE, "r") as f:
            records = f.readlines()

        if records:
            options = []
            mapping = {}

            for line in records:
                file, value = line.strip().split("||")
                options.append(file)
                mapping[file] = value

            selected = st.selectbox("Select QR Code:", options)

            if selected:
                st.image(os.path.join(SAVE_FOLDER, selected), width=220)
                st.code("Stored Data: " + mapping[selected])

                if st.button("🗑 Delete QR Code"):
                    os.remove(os.path.join(SAVE_FOLDER, selected))

                    new_records = [r for r in records if not r.startswith(selected)]
                    with open(DATA_FILE, "w") as f:
                        f.writelines(new_records)

                    st.success("Deleted Successfully! Refresh Page.")
        else:
            st.warning("History Empty")
            
    st.markdown("</div>", unsafe_allow_html=True)