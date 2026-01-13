import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title="Excel → Viber Kontakti", layout="centered")

st.title("📱 Excel → Viber Kontakti")
st.write("Učitaj Excel fajl ili prosljeđi redove direktno.")

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
    st.write("**Korak 1:** Prosljeđi redove - svaki red je jedan kontakt")
    st.write("**Format:** Email | Ime | Prezime | Telefon | Grad")
    st.write("*Primjer:*")
    st.code("""zeljka@example.com	Željka	Kurešević	38763757296	Sarajevo
biljana@example.com	Biljana	Mitrović	38761234567	Zagreb""")
    
    text_input = st.text_area("Upiši redove (lijepi direktno iz Excela ili obični tekst):", 
                               height=150,
                               placeholder="Jedan red po liniji...")
    
    if st.button("Procesiraj redove"):
        if text_input.strip():
            try:
                # Prosljeđi redove u CSV
                csv_data = io.StringIO(text_input)
                df = pd.read_csv(csv_data, sep="\t", on_bad_lines='skip')
                st.success(f"✅ Učitano **{len(df)} redaka**")
            except:
                # Pokušaj sa zarezom
                try:
                    csv_data = io.StringIO(text_input)
                    df = pd.read_csv(csv_data, sep=",", on_bad_lines='skip')
                    st.success(f"✅ Učitano **{len(df)} redaka**")
                except Exception as e:
                    st.error(f"❌ Greška pri obradi: {str(e)}")

# Ako imamo podatke, prikaži provjeru i generiraj VCF
if df is not None and not df.empty:
    st.write("**Provjera podataka:**")
    st.dataframe(df.head(3))
    
    # Generiraj vCard
    vcf_content = ""
    success_count = 0
    error_count = 0
    
    for idx, row in df.iterrows():
        try:
            # Pronađi stupce (fleksibilno, različita imena)
            first_name = str(row.get('Ime', row.get('First Name', ''))).strip()
            last_name = str(row.get('Prezime', row.get('Last Name', ''))).strip()
            email = str(row.get('Email', row.get('email', ''))).strip()
            phone = str(row.get('Telefon', row.get('Phone', row.get('TEL', '')))).strip()
            city = str(row.get('Grad', row.get('City', ''))).strip()
            
            # Očisti podatke
            first_name = first_name if first_name and first_name.lower() != 'nan' else ''
            last_name = last_name if last_name and last_name.lower() != 'nan' else ''
            email = email if email and email.lower() != 'nan' and '@' in email else ''
            phone = phone if phone and phone.lower() != 'nan' and len(phone) > 5 else ''
            city = city if city and city.lower() != 'nan' else ''
            
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
                if city:
                    vcf_content += f"ADR:;;{city};;;LOCALITY:{city}\n"
                
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
            st.warning(f"⚠️ {error_count} redaka preskočeno (nedostaju podaci)")
        
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
        st.error("❌ Nema validnih kontakata. Provjeri da li redovi imaju:\n- **Ime** (obavezno)\n- **Email** ili **Telefon** (trebam bar jedno)")

