import streamlit as st
import pandas as pd
import io
import re

st.set_page_config(page_title="Excel → Viber Kontakti", layout="centered")

st.title("📱 Excel → Viber Kontakti")
st.write("Učitaj Excel fajl ili prosljeđi redove direktno.")

def detect_data_type(value):
    """Detektuj tip podatka (email, telefon, tekst)"""
    if pd.isna(value) or str(value).lower() == 'nan':
        return None
    
    value = str(value).strip()
    
    # Email detekcija
    if '@' in value and '.' in value:
        return 'email'
    
    # Telefon detekcija (samo brojeve, +, -, razmaci)
    phone_pattern = r'^[\d\s\+\-\(\)\.]+$'
    if re.match(phone_pattern, value) and len(value) > 5 and any(c.isdigit() for c in value):
        return 'telefon'
    
    # Tekst
    if any(c.isalpha() for c in value):
        return 'tekst'
    
    return None

def parse_row(row_values):
    """Intelligentno parseuj red sa bilo kakvim redoslijedom stupaca"""
    result = {
        'email': '',
        'telefon': '',
        'imena': []
    }
    
    for value in row_values:
        if pd.isna(value) or str(value).strip() == '':
            continue
        
        data_type = detect_data_type(value)
        
        if data_type == 'email':
            result['email'] = str(value).strip()
        elif data_type == 'telefon':
            result['telefon'] = str(value).strip()
        elif data_type == 'tekst':
            text = str(value).strip()
            # Ako je duži tekst, može biti grad, ako nije - ime/prezime
            if len(text) < 30:  # Vjerojatno ime/prezime/grad
                result['imena'].append(text)
    
    return result

def filter_repeated_mentor(parsed_rows):
    """Filtriraj mentora koji se pojavljuje više puta na kraju"""
    if len(parsed_rows) < 2:
        return parsed_rows
    
    # Broji koliko puta se svako imena pojavljuje kao zadnje u redovima
    last_name_counts = {}
    for pr in parsed_rows:
        if pr['imena']:
            last_name = ' '.join(pr['imena'][-1:])  # Zadnje ime/prezime
            last_name_counts[last_name] = last_name_counts.get(last_name, 0) + 1
    
    # Pronađi mentora - pojavljuje se više puta kao zadnje (većina redaka)
    mentor = None
    if last_name_counts:
        mentor = max(last_name_counts, key=last_name_counts.get)
        # Ako se pojavljuje u manje od 30% redaka, nije mentor
        if last_name_counts[mentor] < len(parsed_rows) * 0.2:
            mentor = None
    
    # Filtriraj - ukloni redove gdje je zadnje ime = mentor
    if mentor:
        filtered = []
        for pr in parsed_rows:
            if pr['imena'] and ' '.join(pr['imena'][-1:]) != mentor:
                filtered.append(pr)
        
        if filtered:
            return filtered
    
    return parsed_rows

def extract_names(imena_lista):
    """Ekstrapoluj imena i prezimena iz liste"""
    if len(imena_lista) == 0:
        return '', ''
    elif len(imena_lista) == 1:
        return imena_lista[0], ''
    elif len(imena_lista) == 2:
        return imena_lista[0], imena_lista[1]
    else:
        # Više od 2 - prvi je ime, drugi prezime, ostatak grad
        return imena_lista[0], imena_lista[1]

# Izbor načina unosa
input_method = st.radio("Odaberi kako ćeš unijeti podatke:", 
                        ["📤 Upload Excel/CSV fajl", "📝 Direktno upiši redove"])

df = None

if input_method == "📤 Upload Excel/CSV fajl":
    uploaded_file = st.file_uploader("Odaberi Excel fajl:", type=["xlsx", "xls", "csv"])
    
    if uploaded_file:
        try:
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)
            st.success(f"✅ Učitan fajl s **{len(df)} redaka**")
        except Exception as e:
            st.error(f"❌ Greška pri učitavanju fajla: {str(e)}")

else:  # Direktan unos
    st.write("**Korak 1:** Prosljeđi redove - redoslijed nije bitan, aplikacija će sami detektovati podatke")
    st.write("**Format:** Email | Ime | Prezime | Telefon | Grad (bilo koji redoslijed)")
    st.write("*Primjer:*")
    st.code("""zeljka@example.com	Željka	Kurešević	38763757296	Sarajevo
biljana@example.com	Biljana	Mitrović	38761234567	Zagreb
iko@example.com	Iko	Skoko	41793905431	Bern""")
    
    text_input = st.text_area("Lijepi redove (direktno iz Excel, Google Sheets, bilo gdje):", 
                               height=150,
                               placeholder="Jedan red po liniji...")
    
    if st.button("Procesiraj redove"):
        if text_input.strip():
            try:
                # Parsiraj redove
                lines = [line.strip() for line in text_input.split('\n') if line.strip()]
                parsed_rows = []
                
                for line in lines:
                    # Pokušaj separatore: tab, višestruki razmaci, zareze
                    if '\t' in line:
                        values = line.split('\t')
                    elif ',' in line:
                        values = line.split(',')
                    else:
                        values = line.split()
                    
                    parsed = parse_row(values)
                    
                    # Trebam bar ime i jedno od email/telefon
                    if parsed['imena'] and (parsed['email'] or parsed['telefon']):
                        parsed_rows.append(parsed)
                
                if parsed_rows:
                    # Filtriraj mentora
                    parsed_rows = filter_repeated_mentor(parsed_rows)
                    st.success(f"✅ Učitano **{len(parsed_rows)} validnih redaka**")
                    
                    # Kreiraj DataFrame za prikaz
                    display_data = []
                    for pr in parsed_rows:
                        first_name, last_name = extract_names(pr['imena'])
                        display_data.append({
                            'Ime': first_name,
                            'Prezime': last_name,
                            'Email': pr['email'],
                            'Telefon': pr['telefon']
                        })
                    df = pd.DataFrame(display_data)
                else:
                    st.error("❌ Nema validnih redaka. Trebam bar ime i jedno od: email ili telefon.")
            except Exception as e:
                st.error(f"❌ Greška pri obradi: {str(e)}")

# Ako imamo podatke, prikaži provjeru i generiraj VCF
if df is not None and not df.empty:
    st.write("**Provjera detektovanih podataka:**")
    st.dataframe(df.head(10), use_container_width=True)
    
    # Generiraj vCard
    vcf_content = ""
    success_count = 0
    error_count = 0
    
    for idx, row in df.iterrows():
        try:
            first_name = str(row.get('Ime', '')).strip()
            last_name = str(row.get('Prezime', '')).strip()
            email = str(row.get('Email', '')).strip()
            phone = str(row.get('Telefon', '')).strip()
            
            # Očisti podatke
            first_name = first_name if first_name and first_name.lower() != 'nan' else ''
            last_name = last_name if last_name and last_name.lower() != 'nan' else ''
            email = email if email and email.lower() != 'nan' and '@' in email else ''
            phone = phone if phone and phone.lower() != 'nan' and len(phone) > 5 else ''
            
            # Trebam bar ime i jedno od email/telefon
            if first_name and (email or phone):
                full_name = f"{first_name} {last_name}".strip()
                
                vcf_content += f"""BEGIN:VCARD
VERSION:3.0
FN:{full_name}
N:{last_name};{first_name};;;
"""
                
                if email:
                    vcf_content += f"EMAIL:{email}\n"
                if phone:
                    vcf_content += f"TEL:{phone}\n"
                
                vcf_content += "END:VCARD\n\n"
                success_count += 1
            else:
                error_count += 1
                
        except Exception as e:
            error_count += 1
            continue
    
    if vcf_content:
        st.success(f"✅ Uspješno generirano **{success_count}** kontakata")
        if error_count > 0:
            st.warning(f"⚠️ {error_count} redaka preskočeno")
        
        # Preuzmi gumb
        st.download_button(
            label="📥 Preuzmi kontakte.vcf",
            data=vcf_content,
            file_name="kontakti.vcf",
            mime="text/vcard"
        )
        
        st.info("""
        ### 💡 Kako dalje:
        1. **Klikni "Preuzmi kontakte.vcf"** - sprema se na tvoj kompjuter
        2. **Preslika na mobitel** - preko USB ili email
        3. **Otvori na mobitelu** - klikni na `.vcf` fajl
        4. **Odaberi "Uvezi u Kontakte"** - Android/iPhone će te pitati
        5. **Dodaj u Viber grupu** - sada imaš sve kontakte!
        """)
    else:
        st.error("❌ Nema validnih kontakata.")


