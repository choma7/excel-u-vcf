# 📱 Excel → Viber Kontakti

Jednostavna i besplatna aplikacija koja pretvara Excel fajlove s kontaktima u `.vcf` format - spreman za direktan import u Android i iPhone!

## 🎯 Za što?

Ako imaš Excel fajl s kontaktima (ima ih imena, prezimena, brojeva telefona i email-a), ova aplikacija će:
1. Učitati tvoj Excel fajl
2. Pretvoriti sve kontakte u format koji čitaju mobilni telefoni
3. Dati ti fajl koji možeš direktno prebaciti na mobitel
4. Svi kontakti se automatski dodaju u Kontakte aplikaciju

**Idealno za:**
- Prebacivanje popisа s računala na mobitel
- Brzo dodavanje više kontakata odjednom
- Sigurnosnu kopiju podataka

---

## 🚀 Kako koristiti? (Bez instalacije!)

### ✅ Najjednostavnije - Online verzija:

1. Otvori link: **[Excel-u-VCF na Streamlit Cloud](https://excel-u-vcf.streamlit.app)** ⚡
2. **Klikni "Browse files"** i odaberi tvoj Excel
3. **Klikni "Preuzmi kontakte.vcf"**
4. **Prebaci na mobitel** (Email, Viber, WhatsApp, Bluetooth...)
5. **Otvori na mobitelu** - sve će se auto-importati!

### 💻 Ako želiš lokalno na računalu:

```bash
# 1. Preuzmi kod
git clone https://github.com/Choma7/excel-u-vcf.git
cd excel-u-vcf

# 2. Instaliraj (prvi put samo)
pip install -r requirements.txt

# 3. Pokreni
streamlit run app.py

# 4. Otvori u browser-u što se pojavi
```

---

## 📋 Format Excel fajla

Fajl trebam imati stupce (po preferenci naziv):

| Obavezno | Opcionalno |
|----------|-----------|
| **Ime** | Prezime |
| **Email** ili **Telefon** | Grad |

### Primjer:

| Ime | Prezime | Email | Telefon | Grad |
|-----|---------|-------|---------|------|
| Željka | Kurešević | zeljka@example.com | 38763757296 | Sarajevo |
| Biljana | Mitrović | biljana@example.com | 38761234567 | Zagreb |

---

## 📱 Što se dešava s mojim podacima?

✅ **Tvoji podaci su SIGURNI!**
- Podaci ostaju samo na tebi - ništa se ne sprema na server
- Aplikacija samo pretvara format
- Obriši fajl s računala kad završiš - gotovo!

---

## 🔧 Tehnički detalji

- **Tehnologija:** Python + Streamlit
- **Besplatno:** Bez skrivenih troškova
- **Open Source:** Kod je javno dostupan
- **Mobilno optimizirano:** Radi i na tabletima

---

## 💡 Česti problemi

### "Greška pri učitavanju fajla"
→ Provjerim je li fajl u Excel (.xlsx) ili CSV formatu

### "Nema validnih kontakata"
→ Provjerim da fajl ima bar stupac "Ime" i jedno od: "Email" ili "Telefon"

### "Na mobitelu se ne uvozi"
→ Pokušaj kopirati `.vcf` fajl preko USB-a ili email-a, pa otvori ga direktno

---

## 📧 Pitanja ili probleme?

[Kontaktiraj na GitHub Issues](https://github.com/Choma7/excel-u-vcf/issues)

---

**Made with ❤️ for easy contact management**
