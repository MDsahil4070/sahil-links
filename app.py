from flask import Flask, render_template, request, redirect, url_for, session, send_file
import json
import os
import re
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "sahil_secret_key_123"

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

DATA_FILE = os.path.join(BASE_DIR, "data.json")

def extract_video_id(url):
    if not url: return None
    patterns = [
        r'(?:https?:\/\/)?(?:www\.)?youtube\.com\/shorts\/([a-zA-Z0-9_-]+)',
        r'(?:https?:\/\/)?(?:www\.)?youtube\.com\/watch\?v=([a-zA-Z0-9_-]+)',
        r'(?:https?:\/\/)?youtu\.be\/([a-zA-Z0-9_-]+)'
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None

def load_data():
    if not os.path.exists(DATA_FILE):
        default_data = {
            "admin_user": "admin",
            "admin_pass": "SahilPassword@590",
            "total_views": 0,
            "title": "Sahil.com 590",
            "tagline": "@sahil.com590_",
            "bio": "🎬 Content Creator & Comedy Skits\n🔥 Connect with me on all official handles!",
            "about_story": "नमस्ते दोस्तों! 🙏 मैं साहिल हूँ, बिहार से। मेरा लक्ष्य अपने देसी अंदाज, खांटी बिहारी कॉमेडी और रिलेटेबल लाइफ सिचुएशन्स से आप सभी के चेहरे पर मुस्कान लाना है। सपोर्ट करने के लिए दिल से धन्यवाद! ❤️",
            "avatar_url": "/static/uploads/avatar.jpg",
            "theme": "theme-red",
            "animation_style": "anim-slide-up",
            "custom_css": "",
            "custom_themes": [],
            "adsense_client": "",
            "custom_html": "",
            "enable_badge": True,
            "badge_text": "🔥 100K+ Family",
            "enable_particles": True,
            "enable_music": False,
            "music_url": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3",
            "notice_text": "🔥 New Bihari Comedy Video Out on YouTube! Watch Now!",
            "countdown_title": "🚀 Next Viral Comedy Drop In:",
            "countdown_target": "2026-09-01T18:00",
            "video_url": "https://www.youtube.com/shorts/dQw4w9WgXcQ",
            "video_id": "dQw4w9WgXcQ",
            "whatsapp_num": "919876543210",
            "upi_id": "sahil@upi",
            "upi_name": "Sahil",
            "milestones": [
                {"title": "100K+ Community", "desc": "Fast Growing", "icon": "fa-solid fa-users"},
                {"title": "10M+ Video Views", "desc": "Viral Skits", "icon": "fa-solid fa-fire"},
                {"title": "Top Bihar Creator", "desc": "Desi Comedy", "icon": "fa-solid fa-crown"}
            ],
            "gallery": [
                {"title": "Shooting BTS 🎬", "url": "https://images.unsplash.com/photo-1517604931442-7e0c8ed2963c?w=600&auto=format&fit=crop&q=60"}
            ],
            "poll": {
                "question": "मेरी अगली कॉमेडी वीडियो किस टॉपिक पर देखना चाहते हैं? 🤔",
                "options": [
                    {"text": "😂 स्कूल बंक और मास्टर जी", "votes": 12},
                    {"text": "🔥 बापू वर्सेस बेटा", "votes": 25},
                    {"text": "🛵 बाइक चोरी प्रैंक", "votes": 8}
                ]
            },
            "reviews": [
                {"name": "Aman (Creator Friend)", "rating": "⭐⭐⭐⭐⭐", "text": "भाई की हर एक कॉमेडी वीडियो एक नंबर होती है! देसी वाइब हमेशा ऑन टॉप 🔥"},
                {"name": "Rahul Verma", "rating": "⭐⭐⭐⭐⭐", "text": "Bihari comedy skits are super relatable and funniest!"}
            ],
            "blocks": [
                {"id": "notice", "name": "📢 Live Announcement Notice", "enabled": True},
                {"id": "milestones", "name": "🏆 Milestones & Achievements", "enabled": True},
                {"id": "about", "name": "📖 About Me & Creator Journey", "enabled": True},
                {"id": "gallery", "name": "📸 Photo Gallery & BTS Shots", "enabled": True},
                {"id": "countdown", "name": "⏱️ Next Video Countdown Timer", "enabled": True},
                {"id": "poll", "name": "📊 Live Fan Poll & Voting", "enabled": True},
                {"id": "video", "name": "🎬 Latest YouTube Video/Short", "enabled": True},
                {"id": "subscribe", "name": "🔥 Hot Subscribe Button", "enabled": True},
                {"id": "links", "name": "🔗 Social Links Group", "enabled": True},
                {"id": "gears", "name": "🛍️ My Gear & Shooting Setup", "enabled": True},
                {"id": "reviews", "name": "⭐ Fan Reviews & Testimonials", "enabled": True},
                {"id": "faq", "name": "❓ FAQ / Questions & Answers", "enabled": True},
                {"id": "upi", "name": "💸 UPI QR Support Card", "enabled": True},
                {"id": "whatsapp", "name": "💬 WhatsApp Business Chat", "enabled": True},
                {"id": "contact", "name": "📩 Direct Fan Message Box", "enabled": True}
            ],
            "links": [
                {"name": "YouTube Channel", "url": "https://youtube.com/@sahil.com590_", "type": "youtube", "icon": "fa-brands fa-youtube", "clicks": 0, "highlight": "🔥 VIRAL"},
                {"name": "Join Telegram", "url": "https://t.me", "type": "telegram", "icon": "fa-brands fa-telegram", "clicks": 0, "highlight": "⚡ NEW"},
                {"name": "Moj Videos", "url": "https://mojapp.in", "type": "moj", "icon": "fa-solid fa-video", "clicks": 0, "highlight": ""},
                {"name": "Facebook Page", "url": "https://facebook.com", "type": "facebook", "icon": "fa-brands fa-facebook-f", "clicks": 0, "highlight": ""}
            ],
            "gears": [
                {"name": "Vivo V29 (4K Camera)", "tag": "Shooting Phone", "url": "https://amzn.to", "icon": "fa-solid fa-mobile-screen"},
                {"name": "Wireless Mic K9", "tag": "Audio Recording", "url": "https://amzn.to", "icon": "fa-solid fa-microphone-lines"},
                {"name": "CapCut Pro Editor", "tag": "Video Editing", "url": "https://capcut.com", "icon": "fa-solid fa-film"}
            ],
            "faqs": [
                {"q": "How to collaborate for business/promotions?", "a": "You can click on the WhatsApp Business button or send a message from the message box."},
                {"q": "Where are you from?", "a": "Bihar, India 🇮🇳"}
            ],
            "messages": []
        }
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(default_data, f, ensure_ascii=False, indent=4)
        return default_data
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
        if "total_views" not in data: data["total_views"] = 0
        if "admin_user" not in data: data["admin_user"] = "admin"
        if "admin_pass" not in data: data["admin_pass"] = "SahilPassword@590"
        if "animation_style" not in data: data["animation_style"] = "anim-slide-up"
        if "custom_themes" not in data: data["custom_themes"] = []
        if "custom_css" not in data: data["custom_css"] = ""
        return data

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

@app.route("/")
def home():
    data = load_data()
    data["total_views"] = data.get("total_views", 0) + 1
    save_data(data)
    
    total_votes = sum(opt.get("votes", 0) for opt in data["poll"].get("options", []))
    for opt in data["poll"].get("options", []):
        opt["percent"] = round((opt.get("votes", 0) / total_votes * 100), 1) if total_votes > 0 else 0
    data["poll"]["total_votes"] = total_votes
    return render_template("index.html", data=data)

@app.route("/vote/<int:opt_idx>", methods=["POST"])
def vote(opt_idx):
    data = load_data()
    if "poll" in data and "options" in data["poll"]:
        if 0 <= opt_idx < len(data["poll"]["options"]):
            data["poll"]["options"][opt_idx]["votes"] = data["poll"]["options"][opt_idx].get("votes", 0) + 1
            save_data(data)
    return redirect(url_for("home"))

@app.route("/click/<int:index>")
def track_click(index):
    data = load_data()
    if 0 <= index < len(data["links"]):
        data["links"][index]["clicks"] = data["links"][index].get("clicks", 0) + 1
        save_data(data)
        return redirect(data["links"][index]["url"])
    return redirect(url_for("home"))

@app.route("/send_message", methods=["POST"])
def send_message():
    data = load_data()
    name = request.form.get("fan_name")
    msg = request.form.get("fan_msg")
    contact = request.form.get("fan_contact")
    if name and msg:
        if "messages" not in data: data["messages"] = []
        data["messages"].insert(0, {"name": name, "contact": contact, "msg": msg})
        save_data(data)
    return redirect(url_for("home"))

@app.route("/admin", methods=["GET", "POST"])
def admin():
    data = load_data()
    if session.get("logged_in"): return redirect(url_for("admin_dashboard"))
    if request.method == "POST":
        user = request.form.get("username")
        pwd = request.form.get("password")
        if user == data.get("admin_user", "admin") and pwd == data.get("admin_pass", "SahilPassword@590"):
            session["logged_in"] = True
            return redirect(url_for("admin_dashboard"))
        else:
            return render_template("admin.html", logged_in=False, data=data, error="गलत यूज़रनेम या पासवर्ड!")
    return render_template("admin.html", logged_in=False, data=data)

@app.route("/admin/download_backup")
def download_backup():
    if not session.get("logged_in"): return redirect(url_for("admin"))
    load_data()
    return send_file(DATA_FILE, as_attachment=True, download_name="sahil_site_backup.json")

@app.route("/admin/dashboard", methods=["GET", "POST"])
def admin_dashboard():
    if not session.get("logged_in"): return redirect(url_for("admin"))
    data = load_data()
    msg_status = None
    
    total_link_clicks = sum(l.get("clicks", 0) for l in data.get("links", []))
    
    if request.method == "POST":
        action = request.form.get("action")
        
        if action == "restore_backup":
            if 'backup_file' in request.files:
                file = request.files['backup_file']
                if file and file.filename.endswith('.json'):
                    try:
                        restored_data = json.load(file)
                        save_data(restored_data)
                        data = restored_data
                        msg_status = "✅ बैकअप फाइल लोड हो गई!"
                    except Exception:
                        msg_status = "❌ अमान्य JSON फाइल!"

        elif action == "reset_analytics":
            data["total_views"] = 0
            for l in data.get("links", []):
                l["clicks"] = 0
            save_data(data)
            msg_status = "✅ एनालिटिक्स डेटा रीसेट हो गया!"

        elif action == "change_credentials":
            new_u = request.form.get("new_username", "").strip()
            new_p = request.form.get("new_password", "").strip()
            if new_u and new_p:
                data["admin_user"] = new_u
                data["admin_pass"] = new_p
                save_data(data)
                msg_status = "✅ एडमिन यूजरनेम और पासवर्ड बदल दिया गया!"

        elif action == "create_custom_theme":
            t_name = request.form.get("theme_name", "").strip()
            t_bg = request.form.get("theme_bg", "#000000")
            t_glow1 = request.form.get("theme_glow1", "#ff0055")
            t_glow2 = request.form.get("theme_glow2", "#00ffff")
            t_card = request.form.get("theme_card", "rgba(20,20,30,0.85)")
            t_border = request.form.get("theme_border", "#ff0055")
            
            if t_name:
                slug = "theme-custom-" + re.sub(r'[^a-zA-Z0-9]', '', t_name).lower()
                if "custom_themes" not in data: data["custom_themes"] = []
                data["custom_themes"].append({
                    "id": slug,
                    "name": "🎨 " + t_name,
                    "bg": t_bg,
                    "glow1": t_glow1,
                    "glow2": t_glow2,
                    "card": t_card,
                    "border": t_border
                })
                data["theme"] = slug
                save_data(data)
                msg_status = f"✅ कस्टम थीम '{t_name}' बन गई और लागू हो गई!"

        elif action == "upload_css_file":
            if 'css_file' in request.files:
                f = request.files['css_file']
                if f and f.filename.endswith('.css'):
                    content = f.read().decode('utf-8', errors='ignore')
                    data["custom_css"] = content
                    save_data(data)
                    msg_status = "✅ कस्टम CSS फाइल सफलतापूर्वक अपलोड हो गई!"

        elif action == "delete_custom_theme":
            idx = int(request.form.get("index"))
            if "custom_themes" in data and 0 <= idx < len(data["custom_themes"]):
                del_id = data["custom_themes"][idx]["id"]
                data["custom_themes"].pop(idx)
                if data.get("theme") == del_id:
                    data["theme"] = "theme-red"
                save_data(data)
                msg_status = "✅ कस्टम थीम हटा दी गई!"

        elif action == "move_up":
            idx = int(request.form.get("index"))
            if idx > 0:
                data["blocks"][idx], data["blocks"][idx-1] = data["blocks"][idx-1], data["blocks"][idx]
                save_data(data)
        elif action == "move_down":
            idx = int(request.form.get("index"))
            if idx < len(data["blocks"]) - 1:
                data["blocks"][idx], data["blocks"][idx+1] = data["blocks"][idx+1], data["blocks"][idx]
                save_data(data)
                
        elif action == "toggle_block":
            idx = int(request.form.get("index"))
            data["blocks"][idx]["enabled"] = not data["blocks"][idx]["enabled"]
            save_data(data)

        elif action == "update_profile":
            data["title"] = request.form.get("title")
            data["tagline"] = request.form.get("tagline")
            data["bio"] = request.form.get("bio")
            data["about_story"] = request.form.get("about_story")
            data["theme"] = request.form.get("theme")
            data["animation_style"] = request.form.get("animation_style", "anim-slide-up")
            data["custom_css"] = request.form.get("custom_css", "")
            data["adsense_client"] = request.form.get("adsense_client")
            data["custom_html"] = request.form.get("custom_html")
            data["enable_badge"] = True if request.form.get("enable_badge") == "on" else False
            data["badge_text"] = request.form.get("badge_text")
            data["notice_text"] = request.form.get("notice_text")
            data["enable_particles"] = True if request.form.get("enable_particles") == "on" else False
            data["enable_music"] = True if request.form.get("enable_music") == "on" else False
            data["music_url"] = request.form.get("music_url")
            data["countdown_title"] = request.form.get("countdown_title")
            data["countdown_target"] = request.form.get("countdown_target")
            
            raw_video = request.form.get("video_url", "").strip()
            data["video_url"] = raw_video
            data["video_id"] = extract_video_id(raw_video)
            
            data["whatsapp_num"] = request.form.get("whatsapp_num")
            data["upi_id"] = request.form.get("upi_id")
            data["upi_name"] = request.form.get("upi_name")
            
            if 'avatar_file' in request.files:
                file = request.files['avatar_file']
                if file and file.filename != '':
                    filename = secure_filename(file.filename)
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    data["avatar_url"] = f"/static/uploads/{filename}"
            
            save_data(data)
            msg_status = "✅ सेटिंग्स सुरक्षित हो गईं!"

        elif action == "add_milestone":
            m_title = request.form.get("m_title")
            m_desc = request.form.get("m_desc")
            m_icon = request.form.get("m_icon", "fa-solid fa-award")
            if "milestones" not in data: data["milestones"] = []
            data["milestones"].append({"title": m_title, "desc": m_desc, "icon": m_icon})
            save_data(data)

        elif action == "delete_milestone":
            idx = int(request.form.get("index"))
            if "milestones" in data and 0 <= idx < len(data["milestones"]):
                data["milestones"].pop(idx)
                save_data(data)

        elif action == "add_gallery_photo":
            g_title = request.form.get("g_title")
            photo_url = request.form.get("photo_url", "")
            if 'photo_file' in request.files:
                file = request.files['photo_file']
                if file and file.filename != '':
                    fname = secure_filename(file.filename)
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], fname))
                    photo_url = f"/static/uploads/{fname}"
            if photo_url:
                if "gallery" not in data: data["gallery"] = []
                data["gallery"].append({"title": g_title, "url": photo_url})
                save_data(data)

        elif action == "delete_gallery_photo":
            idx = int(request.form.get("index"))
            if "gallery" in data and 0 <= idx < len(data["gallery"]):
                data["gallery"].pop(idx)
                save_data(data)

        elif action == "update_poll":
            q = request.form.get("poll_question")
            opt1 = request.form.get("poll_opt1")
            opt2 = request.form.get("poll_opt2")
            opt3 = request.form.get("poll_opt3")
            data["poll"] = {
                "question": q,
                "options": [
                    {"text": opt1, "votes": 0},
                    {"text": opt2, "votes": 0}
                ]
            }
            if opt3 and opt3.strip():
                data["poll"]["options"].append({"text": opt3.strip(), "votes": 0})
            save_data(data)
            
        elif action == "add_review":
            r_name = request.form.get("rev_name")
            r_text = request.form.get("rev_text")
            r_star = request.form.get("rev_star", "⭐⭐⭐⭐⭐")
            if "reviews" not in data: data["reviews"] = []
            data["reviews"].append({"name": r_name, "rating": r_star, "text": r_text})
            save_data(data)

        elif action == "delete_review":
            idx = int(request.form.get("index"))
            if "reviews" in data and 0 <= idx < len(data["reviews"]):
                data["reviews"].pop(idx)
                save_data(data)

        elif action == "add_link":
            name = request.form.get("name")
            url = request.form.get("url")
            ltype = request.form.get("type", "other")
            highlight = request.form.get("highlight", "").strip()
            icon = "fa-solid fa-link"
            if "youtube" in ltype: icon = "fa-brands fa-youtube"
            elif "facebook" in ltype: icon = "fa-brands fa-facebook-f"
            elif "telegram" in ltype: icon = "fa-brands fa-telegram"
            elif "instagram" in ltype: icon = "fa-brands fa-instagram"
            elif "moj" in ltype: icon = "fa-solid fa-video"
            data["links"].append({"name": name, "url": url, "type": ltype, "icon": icon, "clicks": 0, "highlight": highlight})
            save_data(data)
            
        elif action == "delete_link":
            idx = int(request.form.get("index"))
            if 0 <= idx < len(data["links"]):
                data["links"].pop(idx)
                save_data(data)

        elif action == "add_gear":
            g_name = request.form.get("gear_name")
            g_tag = request.form.get("gear_tag")
            g_url = request.form.get("gear_url")
            g_icon = request.form.get("gear_icon", "fa-solid fa-bag-shopping")
            if "gears" not in data: data["gears"] = []
            data["gears"].append({"name": g_name, "tag": g_tag, "url": g_url, "icon": g_icon})
            save_data(data)

        elif action == "delete_gear":
            idx = int(request.form.get("index"))
            if "gears" in data and 0 <= idx < len(data["gears"]):
                data["gears"].pop(idx)
                save_data(data)

        elif action == "add_faq":
            q = request.form.get("faq_q")
            a = request.form.get("faq_a")
            if "faqs" not in data: data["faqs"] = []
            data["faqs"].append({"q": q, "a": a})
            save_data(data)

        elif action == "delete_faq":
            idx = int(request.form.get("index"))
            if "faqs" in data and 0 <= idx < len(data["faqs"]):
                data["faqs"].pop(idx)
                save_data(data)

        elif action == "clear_messages":
            data["messages"] = []
            save_data(data)

        return render_template("admin.html", logged_in=True, data=data, total_link_clicks=total_link_clicks, msg_status=msg_status)

    return render_template("admin.html", logged_in=True, data=data, total_link_clicks=total_link_clicks)

@app.route("/logout")
def logout():
    session.pop("logged_in", None)
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True, port=5000)
