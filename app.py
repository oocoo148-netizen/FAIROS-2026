from flask import Flask, request, render_template_string
import requests
import re
import os

app = Flask(__name__)

# القالب الكامل (نفس الكود اللي عندك)
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>FAIROS~2026 | Facebook ID Lookup</title>
    <meta name="description" content="أداة احترافية لاستخراج المعرف الرقمي لحسابات فيسبوك">
    <meta name="author" content="FAIROS~2026">
    <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;800&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&display=swap');
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Cairo', 'Share Tech Mono', monospace; background: #0a0a0f; min-height: 100vh; overflow-x: hidden; }
        .cyber-bg { position: fixed; top: 0; left: 0; width: 100%; height: 100%; z-index: -2; background: linear-gradient(135deg, #0a0a0f 0%, #0a1a1a 50%, #0a0a0f 100%); }
        .matrix-rain { position: fixed; top: 0; left: 0; width: 100%; height: 100%; z-index: -1; opacity: 0.15; }
        .glow { position: fixed; top: 50%; left: 50%; width: 500px; height: 500px; background: radial-gradient(circle, rgba(0,255,0,0.1) 0%, transparent 70%); transform: translate(-50%, -50%); z-index: -1; animation: pulse 4s ease infinite; }
        @keyframes pulse { 0%, 100% { opacity: 0.3; transform: translate(-50%, -50%) scale(1); } 50% { opacity: 0.6; transform: translate(-50%, -50%) scale(1.2); } }
        .preloader { position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: #0a0a0f; display: flex; align-items: center; justify-content: center; z-index: 9999; transition: 0.5s; }
        .preloader.fade-out { opacity: 0; visibility: hidden; }
        .loader { text-align: center; }
        .loader .cyber-text { font-size: 2rem; font-weight: 800; background: linear-gradient(135deg, #00ff88, #00cc66); -webkit-background-clip: text; background-clip: text; color: transparent; letter-spacing: 5px; animation: blink 1.5s ease infinite; }
        @keyframes blink { 0%, 100% { opacity: 1; text-shadow: 0 0 10px #00ff88; } 50% { opacity: 0.7; text-shadow: 0 0 20px #00ff88; } }
        .loader-dots { display: flex; justify-content: center; gap: 10px; margin-top: 20px; }
        .loader-dots span { width: 12px; height: 12px; background: #00ff88; border-radius: 50%; animation: bounce 0.8s ease infinite; }
        .loader-dots span:nth-child(2) { animation-delay: 0.2s; }
        .loader-dots span:nth-child(3) { animation-delay: 0.4s; }
        @keyframes bounce { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(-15px); } }
        .container { max-width: 750px; margin: 0 auto; padding: 20px; min-height: 100vh; display: flex; align-items: center; justify-content: center; position: relative; z-index: 1; }
        .cyber-card { background: rgba(10, 20, 20, 0.85); backdrop-filter: blur(12px); border: 1px solid rgba(0, 255, 136, 0.3); border-radius: 24px; padding: 40px 35px; width: 100%; box-shadow: 0 0 40px rgba(0, 255, 136, 0.1), inset 0 0 20px rgba(0, 255, 136, 0.05); transition: 0.3s; }
        .cyber-card:hover { border-color: rgba(0, 255, 136, 0.6); box-shadow: 0 0 60px rgba(0, 255, 136, 0.2); }
        .logo { text-align: center; margin-bottom: 25px; }
        .logo h1 { font-size: 2.5rem; font-weight: 800; background: linear-gradient(135deg, #00ff88, #00cc66, #009944); -webkit-background-clip: text; background-clip: text; color: transparent; letter-spacing: 3px; }
        .logo .tag { color: #00ff88; font-size: 0.8rem; font-family: 'Share Tech Mono', monospace; letter-spacing: 2px; margin-top: 5px; }
        .subtitle { text-align: center; color: #88ffaa; margin-bottom: 35px; font-size: 0.9rem; border-bottom: 1px solid rgba(0, 255, 136, 0.2); padding-bottom: 15px; }
        .input-group { margin-bottom: 25px; }
        .input-group label { display: block; margin-bottom: 12px; color: #00ff88; font-weight: 600; letter-spacing: 1px; }
        .input-wrapper { display: flex; align-items: center; background: rgba(0, 20, 20, 0.9); border: 1px solid rgba(0, 255, 136, 0.3); border-radius: 16px; padding: 5px 18px; transition: 0.3s; }
        .input-wrapper:focus-within { border-color: #00ff88; box-shadow: 0 0 15px rgba(0, 255, 136, 0.2); }
        .input-wrapper i { color: #00ff88; font-size: 18px; margin-left: 12px; }
        input { flex: 1; padding: 16px 0; border: none; background: transparent; font-size: 15px; font-family: 'Share Tech Mono', monospace; outline: none; color: #ccffdd; }
        input::placeholder { color: #338855; }
        .cyber-btn { width: 100%; padding: 16px; background: linear-gradient(135deg, #00aa55, #008844); border: none; border-radius: 16px; color: white; font-size: 18px; font-weight: 700; font-family: 'Cairo', sans-serif; cursor: pointer; transition: 0.3s; display: flex; align-items: center; justify-content: center; gap: 12px; position: relative; overflow: hidden; }
        .cyber-btn:before { content: ''; position: absolute; top: 0; left: -100%; width: 100%; height: 100%; background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent); transition: 0.5s; }
        .cyber-btn:hover:before { left: 100%; }
        .cyber-btn:hover { transform: translateY(-2px); box-shadow: 0 10px 25px -5px rgba(0, 255, 136, 0.4); }
        .cyber-btn:disabled { opacity: 0.6; cursor: not-allowed; transform: none; }
        .result-area { margin-top: 35px; display: none; }
        .result-area.show { display: block; animation: fadeInUp 0.5s ease; }
        @keyframes fadeInUp { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }
        .result-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px; padding-bottom: 10px; border-bottom: 1px solid rgba(0, 255, 136, 0.3); }
        .result-header span { color: #00ff88; font-weight: 700; }
        .copy-btn { background: rgba(0, 255, 136, 0.1); border: 1px solid rgba(0, 255, 136, 0.3); border-radius: 12px; padding: 8px 16px; color: #00ff88; cursor: pointer; transition: 0.3s; font-size: 13px; }
        .copy-btn:hover { background: rgba(0, 255, 136, 0.2); border-color: #00ff88; }
        .id-box { background: rgba(0, 20, 20, 0.9); border-radius: 16px; padding: 20px; text-align: center; border: 1px solid rgba(0, 255, 136, 0.2); }
        .id-value { font-size: 28px; font-weight: bold; font-family: 'Share Tech Mono', monospace; color: #00ff88; word-break: break-all; letter-spacing: 2px; }
        .error-box { border-color: rgba(255, 68, 68, 0.3); }
        .error-box .id-value { color: #ff6666; }
        .loading { text-align: center; margin-top: 30px; padding: 20px; display: none; }
        .loading.show { display: block; }
        .cyber-spinner { width: 50px; height: 50px; border: 3px solid rgba(0, 255, 136, 0.2); border-top: 3px solid #00ff88; border-radius: 50%; animation: spin 0.8s linear infinite; margin: 0 auto 15px; }
        @keyframes spin { to { transform: rotate(360deg); } }
        .dev-section { margin-top: 35px; padding-top: 20px; border-top: 1px solid rgba(0, 255, 136, 0.2); text-align: center; display: flex; justify-content: center; gap: 15px; flex-wrap: wrap; }
        .dev-btn { display: inline-flex; align-items: center; gap: 10px; background: #1a2a2a; color: #00ff88; padding: 12px 28px; border-radius: 40px; text-decoration: none; font-weight: 600; border: 1px solid rgba(0, 255, 136, 0.3); transition: 0.3s; }
        .dev-btn.telegram:hover { background: #0088cc; color: white; }
        .dev-btn.instagram:hover { background: linear-gradient(45deg, #f09433, #d62976, #962fbf); color: white; }
        .dev-btn:hover { transform: translateY(-2px); }
        .footer { text-align: center; margin-top: 25px; font-size: 11px; color: #338855; font-family: 'Share Tech Mono', monospace; }
        .toast-msg { position: fixed; bottom: 30px; left: 50%; transform: translateX(-50%) translateY(100px); background: #1a2a1a; border: 1px solid #00ff88; color: #00ff88; padding: 12px 25px; border-radius: 50px; font-size: 14px; z-index: 2000; transition: 0.3s; opacity: 0; }
        .toast-msg.show { transform: translateX(-50%) translateY(0); opacity: 1; }
        @media (max-width: 600px) { .cyber-card { padding: 25px 20px; } .id-value { font-size: 20px; } .logo h1 { font-size: 1.8rem; } .dev-section { flex-direction: column; align-items: center; } .dev-btn { width: 80%; justify-content: center; } }
    </style>
</head>
<body>
    <div class="cyber-bg"></div>
    <canvas class="matrix-rain" id="matrixCanvas"></canvas>
    <div class="glow"></div>
    
    <div class="preloader" id="preloader">
        <div class="loader">
            <div class="cyber-text">FAIROS~2026</div>
            <div class="loader-dots"><span></span><span></span><span></span></div>
            <div style="color:#338855; margin-top:15px; font-size:12px;">تحميل البيئة...</div>
        </div>
    </div>
    
    <div class="container">
        <div class="cyber-card">
            <div class="logo">
                <h1>FAIROS~2026</h1>
                <div class="tag">{ Facebook ID Lookup }</div>
            </div>
            <div class="subtitle">
                <i class="fas fa-terminal"></i> استخرج المعرف الرقمي لأي حساب فيسبوك
            </div>
            
            <form method="POST" id="lookupForm">
                <div class="input-group">
                    <label><i class="fas fa-link"></i> رابط البروفايل</label>
                    <div class="input-wrapper">
                        <i class="fab fa-facebook-f"></i>
                        <input type="text" name="facebook_url" placeholder="https://www.facebook.com/username" required>
                    </div>
                </div>
                <button type="submit" class="cyber-btn" id="submitBtn">
                    <i class="fas fa-user-secret"></i> استخراج الـ ID
                </button>
            </form>
            
            <div class="loading" id="loading">
                <div class="cyber-spinner"></div>
                <div style="color:#00ff88;">جاري الاختراق...</div>
                <div style="color:#338855; font-size:12px; margin-top:8px;">معالجة الطلب</div>
            </div>
            
            <div class="result-area" id="resultArea">
                <div class="result-header">
                    <span><i class="fab fa-facebook-f"></i> FACEBOOK ID</span>
                    <button class="copy-btn" onclick="copyToClipboard()"><i class="far fa-copy"></i> نسخ</button>
                </div>
                <div class="id-box" id="resultBox">
                    <div class="id-value" id="resultValue"></div>
                </div>
            </div>
            
            <div class="dev-section">
                <a href="https://t.me/F_O_70" target="_blank" class="dev-btn telegram"><i class="fab fa-telegram-plane"></i> تواصل عبر تيليجرام</a>
                <a href="https://instagram.com/5k._ti" target="_blank" class="dev-btn instagram"><i class="fab fa-instagram"></i> تابعنا على إنستغرام</a>
            </div>
            
            <div class="footer">
                <i class="fas fa-shield-haltered"></i> FAIROS~2026 | جميع الحقوق محفوظة
            </div>
        </div>
    </div>
    
    <div class="toast-msg" id="toastMsg"><i class="fas fa-check-circle"></i> تم نسخ المعرف</div>
    
    <script>
        const canvas = document.getElementById('matrixCanvas');
        const ctx = canvas.getContext('2d');
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
        const chars = "アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワヲン01";
        const fontSize = 14;
        const columns = canvas.width / fontSize;
        const drops = [];
        for(let i = 0; i < columns; i++) drops[i] = Math.random() * -100;
        function drawMatrix() {
            ctx.fillStyle = 'rgba(10, 20, 20, 0.05)';
            ctx.fillRect(0, 0, canvas.width, canvas.height);
            ctx.fillStyle = '#0f8';
            ctx.font = fontSize + 'px monospace';
            for(let i = 0; i < drops.length; i++) {
                const text = chars.charAt(Math.floor(Math.random() * chars.length));
                ctx.fillText(text, i * fontSize, drops[i] * fontSize);
                if(drops[i] * fontSize > canvas.height && Math.random() > 0.975) drops[i] = 0;
                drops[i]++;
            }
        }
        setInterval(drawMatrix, 50);
        window.addEventListener('resize', () => { canvas.width = window.innerWidth; canvas.height = window.innerHeight; });
        
        window.addEventListener('load', () => {
            setTimeout(() => {
                const preloader = document.getElementById('preloader');
                preloader.classList.add('fade-out');
                setTimeout(() => preloader.style.display = 'none', 500);
            }, 1500);
        });
        
        function copyToClipboard() {
            const text = document.getElementById('resultValue').innerText;
            navigator.clipboard.writeText(text).then(() => {
                const toast = document.getElementById('toastMsg');
                toast.classList.add('show');
                setTimeout(() => toast.classList.remove('show'), 2000);
            });
        }
        
        const form = document.getElementById('lookupForm');
        const submitBtn = document.getElementById('submitBtn');
        const loading = document.getElementById('loading');
        const resultArea = document.getElementById('resultArea');
        const resultValue = document.getElementById('resultValue');
        const resultBox = document.getElementById('resultBox');
        
        form.addEventListener('submit', function() {
            submitBtn.disabled = true;
            loading.classList.add('show');
            resultArea.classList.remove('show');
        });
        
        {% if result %}
        resultValue.innerText = "{{ result }}";
        resultArea.classList.add('show');
        {% if error %}
        resultBox.classList.add('error-box');
        {% else %}
        resultBox.classList.remove('error-box');
        {% endif %}
        submitBtn.disabled = false;
        loading.classList.remove('show');
        {% endif %}
    </script>
</body>
</html>
'''

def extract_facebook_id(profile_url):
    profile_url = profile_url.strip()
    if 'facebook.com' not in profile_url:
        return None, "الرابط غير صالح"
    import re
    id_match = re.search(r'id[=:]([0-9]+)', profile_url)
    if id_match:
        return id_match.group(1), None
    username_match = re.search(r'facebook\.com/([^/?]+)', profile_url)
    if username_match:
        username = username_match.group(1)
        if username and username not in ['share', 'photo', 'video', 'story']:
            try:
                headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
                response = requests.get(f'https://www.facebook.com/{username}', headers=headers, timeout=10)
                if response.status_code == 200:
                    content = response.text
                    id_find = re.search(r'\"userID\"\s*:\s*\"(\d+)\"', content)
                    if id_find:
                        return id_find.group(1), None
                    id_find2 = re.search(r'\"profile_id\"\s*:\s*(\d+)', content)
                    if id_find2:
                        return id_find2.group(1), None
                    id_find3 = re.search(r'entidentifier=(\d+)', content)
                    if id_find3:
                        return id_find3.group(1), None
            except:
                pass
    return None, "لم نتمكن من استخراج الـ ID"

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    error = False
    if request.method == 'POST':
        facebook_url = request.form.get('facebook_url', '').strip()
        if facebook_url:
            id_result, err_msg = extract_facebook_id(facebook_url)
            if err_msg:
                result = err_msg
                error = True
            else:
                result = id_result
                error = False
        else:
            result = "الرجاء إدخال رابط الحساب"
            error = True
    return render_template_string(HTML_TEMPLATE, result=result, error=error)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print("""
    ╔════════════════════════════════════════════════════════════════╗
    ║                   FAIROS~2026 - Cyber Tool                     ║
    ╠════════════════════════════════════════════════════════════════╣
    ║  🔥 تم التطوير بواسطة: @F_O_70                                 ║
    ║  📱 شغّل المتصفح على: http://127.0.0.1:5000                    ║
    ║  🌐 للمشاركة على الشبكة: http://[IP]:5000                      ║
    ║  ⚡ النظام جاهز للعمل 24/7                                     ║
    ╚════════════════════════════════════════════════════════════════╝
    """)
    app.run(host='0.0.0.0', port=port)