import streamlit as st
from collections import Counter

# Sayfa Ayarları
st.set_page_config(page_title="Kelimelik Pro", page_icon="📝")

# --- TAM İŞARETLEDİĞİN YERE (SAĞ ÜST) YERLEŞTİRME ---
st.markdown(
    """
    <style>
    .custom-signature {
        position: absolute;
        top: 45px; /* Deploy butonunun tam altına hizalar */
        right: 10px; /* Sağ kenara yanaştırır */
        z-index: 999999;
        font-weight: bold;
        color: #31333F; /* Streamlit koyu yazı rengi */
        background-color: rgba(255, 255, 255, 0.5); /* Hafif şeffaf arka plan */
        padding: 2px 5px;
        font-size: 13px;
        white-space: nowrap;
    }
    </style>
    <div class="custom-signature">🚀 Made by ÜÇ & AI</div>
    """,
    unsafe_allow_html=True
)

# 1. Şifreleme Mekanizması
def check_password():
    if "password_correct" not in st.session_state:
        st.session_state["password_correct"] = False
    if st.session_state["password_correct"]:
        return True

    st.title("🔐 Erişim Kısıtlı")
    password = st.text_input("Lütfen şifreyi giriniz:", type="password")
    
    if password == "üç":
        st.session_state["password_correct"] = True
        st.rerun()
    elif password:
        st.error("❌ Hatalı şifre!")
    return False

# Şifre doğruysa ana uygulama başlar
if check_password():
    st.title("📝 Kelime Türetici & Puanlayıcı")

    # Kelimelik Resmi Harf Puan Tablosu
    PUAN_TABLOSU = {
        'a': 1, 'b': 3, 'c': 4, 'ç': 4, 'd': 3, 'e': 1, 'f': 7, 'g': 5, 'ğ': 8,
        'h': 5, 'ı': 2, 'i': 1, 'j': 10, 'k': 1, 'l': 1, 'm': 2, 'n': 1, 'o': 2,
        'ö': 7, 'p': 5, 'r': 1, 's': 2, 'ş': 4, 't': 1, 'u': 2, 'ü': 3, 'v': 7,
        'y': 3, 'z': 4
    }

    def puan_hesapla(kelime):
        return sum(PUAN_TABLOSU.get(harf, 0) for harf in kelime.lower())

    def kelime_turet(eldeki_harfler, kelime_listesi_dosyasi):
        harfler_temiz = eldeki_harfler.lower().replace("I", "ı").replace("İ", "i")
        eldeki_harfler_sayimi = Counter(harfler_temiz)
        anlamli_kelimeler = []

        try:
            with open(kelime_listesi_dosyasi, 'r', encoding='utf-8') as dosya:
                for satir in dosya:
                    kelime = satir.strip().lower().replace("I", "ı").replace("İ", "i")
                    if len(kelime) < 3: continue 
                    kelime_sayimi = Counter(kelime)
                    if all(eldeki_harfler_sayimi[harf] >= adet for harf, adet in kelime_sayimi.items()):
                        puan = puan_hesapla(kelime)
                        anlamli_kelimeler.append((kelime, puan))
            return sorted(anlamli_kelimeler, key=lambda x: (x[1], len(x[0])), reverse=True)
        except Exception as e:
            st.error(f"Hata: {e}")
            return []

    # Harf Giriş Alanı
    harfler = st.text_input("Elinizdeki Harfleri Girin:", placeholder="Örn: rtsıaka")

    if harfler:
        sonuclar = kelime_turet(harfler, "kelimeler.txt")
        if sonuclar:
            st.success(f"{len(sonuclar)} adet kelime bulundu!")
            for kelime, puan in sonuclar[:30]:
                c1, c2 = st.columns([3, 1])
                with c1: st.write(f"**{kelime.upper()}**")
                with c2: st.write(f"🏆 {puan}")
        else:
            st.warning("Uygun kelime bulunamadı.")