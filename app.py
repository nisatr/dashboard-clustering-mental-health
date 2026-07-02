import streamlit as st
import pandas as pd
from pathlib import Path
import plotly.express as px

# --- 1. KONFIGURASI HALAMAN DASHBOARD ---
st.set_page_config(page_title="Dashboard Faktor Penyebab Gangguan Kesehatan Mental", layout="wide", initial_sidebar_state="expanded")

# --- 2. DATA RINGKASAN HASIL PENELITIAN ---
TOTAL_DOKUMEN = 3447
JUMLAH_CLUSTER = 5
SILHOUETTE_FINAL = 0.4213
CALINSKI_FINAL = 6538.24

info_klaster = {
    0: {
        "label": "Kecemasan Pengasuhan & Beban Peran Keluarga",
        "deskripsi": (
            "Cluster ini menggambarkan pola permasalahan yang berfokus pada kecemasan, "
            "kelelahan mental, dan tekanan dalam menjalankan peran sehari-hari, terutama "
            "dalam konteks keluarga dan pengasuhan. Mimpi buruk mengindikasikan tekanan "
            "emosional yang cukup kuat, sedangkan penggunaan media digital dapat menjadi "
            "sarana distraksi atau justru memicu kecemasan pengasuhan."
        ),
    },
    1: {
        "label": "Kebutuhan Kasih Sayang, Krisis Relasi Interpersonal & Pencarian Makna Hidup",
        "deskripsi": (
            "Cluster ini menggambarkan permasalahan yang berakar pada dinamika hubungan "
            "keluarga dan pasangan, kebutuhan kasih sayang, serta kebutuhan emosional "
            "yang belum terpenuhi secara optimal. Kondisi ini dapat memicu evaluasi diri, "
            "perbandingan sosial, pencarian arah hidup, keraguan diri, dan ketidakpuasan "
            "terhadap kondisi yang sedang dijalani."
        ),
    },
    2: {
        "label": "Konflik Keluarga & Keputusasaan",
        "deskripsi": (
            "Cluster ini menunjukkan distres emosional yang cukup mendalam dan berakar "
            "pada relasi keluarga serta pengalaman interpersonal yang menimbulkan rasa "
            "tidak aman dan kehilangan harapan. Mimpi buruk dan putus asa menunjukkan "
            "bahwa tekanan psikologis tidak hanya muncul pada pikiran dan emosi, tetapi "
            "juga memengaruhi kualitas tidur dan kesejahteraan psikologis secara umum."
        ),
    },
    3: {
        "label": "Kerentanan Ekonomi & Perubahan Struktur Keluarga",
        "deskripsi": (
            "Cluster ini menunjukkan bahwa sumber utama permasalahan kesehatan mental "
            "berkaitan dengan tekanan ekonomi dalam konteks relasi keluarga dan rumah "
            "tangga yang penuh ketegangan. Pola komunikasi keras, kritis, atau mengontrol "
            "dapat menimbulkan perasaan tertekan, tidak dihargai, dan kelelahan emosional. "
            "Kemunculan kata mantan suami juga menunjukkan adanya isu perubahan struktur "
            "keluarga atau dampak perceraian."
        ),
        "fokus_prev": (
            "Intervensi berbasis komunitas terkait literasi finansial keluarga, rujukan "
            "bantuan sosial, konseling keluarga, dan dukungan untuk keluarga pascaperubahan struktur."
        )
    },
    4: {
        "label": "Kekerasan Verbal dan Emosional dalam Keluarga",
        "deskripsi": (
            "Cluster ini menunjukkan akar permasalahan yang berasal dari relasi keluarga "
            "yang diwarnai komunikasi negatif, kritik berulang, kemarahan, penolakan emosional, "
            "dan bentuk kekerasan verbal. Pola pasif-agresif seperti diam treatment dapat "
            "membuat individu merasa tidak dihargai, ditolak, atau tidak memiliki ruang "
            "untuk menyelesaikan konflik secara sehat."
        ),
        "fokus_prev": (
            "Edukasi komunikasi keluarga tanpa kekerasan, peningkatan kesadaran terhadap "
            "kekerasan emosional, dukungan psikososial, dan rujukan bila terdapat risiko kekerasan."
        )
    }
}

cluster_summary_data = pd.DataFrame({
    "Cluster": [0, 1, 2, 3, 4],
    "Jumlah Dokumen": [580, 729, 655, 931, 552],
    "Silhouette Cluster": [0.5668, 0.3495, 0.3929, 0.4365, 0.3711]
})

cluster_summary_data["Persentase"] = (
    cluster_summary_data["Jumlah Dokumen"] / cluster_summary_data["Jumlah Dokumen"].sum() * 100
).round(2)

cluster_bigram_data = {
    0: [
        ("Mimpi Buruk", 9),
        ("Lahir Caesar", 5),
        ("Main Handphone", 3),
        ("Dengar Berita", 2),
        ("Adik Ipar", 1),
        ("Serba Salah", 1),
        ("Salah Satu", 1),
        ("Anak Bungsu", 1),
        ("Anak Rewel", 1),
        ("Main Game", 1)
    ],
    1: [
        ("Orang Tua", 178),
        ("Rumah Tangga", 44),
        ("Jalin Hubung", 29),
        ("Marah Marah", 29),
        ("Janda Anak", 17),
        ("Kasih Sayang", 14),
        ("Jatuh Cinta", 14),
        ("Banding Banding", 11),
        ("Tuju Hidup", 10),
        ("Duda Anak", 10)
    ],
    2: [
        ("Mimpi Buruk", 18),
        ("Orang Tua", 16),
        ("Putus Asa", 15),
        ("Main Handphone", 8),
        ("Adik Angkat", 6),
        ("Marah Marah", 5),
        ("Teriak Teriak", 5),
        ("Berangkat Kerja", 5),
        ("Dengar Berita", 4),
        ("Rumah Tangga", 4)
    ],
    3: [
        ("Orang Tua", 548),
        ("Rumah Tangga", 71),
        ("Marah Marah", 60),
        ("Cari Uang", 39),
        ("Pinjam Uang", 38),
        ("Mantan Suami", 26),
        ("Bayar Utang", 22),
        ("Maki Maki", 22),
        ("Suruh Suruh", 19),
        ("Pegang Uang", 19)
    ],
    4: [
        ("Orang Tua", 65),
        ("Maki Maki", 16),
        ("Marah Marah", 15),
        ("Rumah Tangga", 8),
        ("Pulang Kampung", 6),
        ("Omel Omel", 6),
        ("Putus Asa", 5),
        ("Diam Treatment", 4),
        ("Tuju Hidup", 4),
        ("Teriak Teriak", 4)
    ]
}

evaluasi_k = pd.DataFrame({
    "Jumlah Cluster (K)": [2, 3, 4, 5],
    "Silhouette Score": [0.5832, 0.4544, 0.4265, 0.4213],
    "Calinski-Harabasz Index": [7641.42, 6153.54, 6642.42, 6538.24],
})

dist_data = cluster_summary_data.copy()
dist_data["Cluster Label"] = dist_data["Cluster"].apply(lambda x: f"Cluster {x}")

# --- 3. CUSTOM CSS DASHBOARD FORMAL SOFT COLOR ---
st.markdown("""
<style>
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1200px;
    }

    body {
        background-color: #f8fafc;
    }

    [data-testid="stSidebar"] {
        background-color: #eef6f8;
        border-right: 1px solid #d7e5ea;
    }

    [data-testid="stSidebar"] * {
        color: #1e293b !important;
    }

    .dashboard-hero {
        background-color: #f0f7fb;
        border: 1px solid #cfe3ec;
        padding: 30px 34px;
        border-radius: 18px;
        color: #0f172a;
        margin-bottom: 24px;
        box-shadow: 0 4px 16px rgba(15, 23, 42, 0.06);
    }

    .dashboard-hero h1 {
        font-size: 32px;
        margin-bottom: 10px;
        font-weight: 750;
        letter-spacing: -0.3px;
        color: #123047;
    }

    .dashboard-hero p {
        font-size: 15.5px;
        line-height: 1.7;
        margin: 0;
        max-width: 900px;
        color: #475569;
    }

    .section-title {
        font-size: 19px;
        font-weight: 750;
        color: #123047;
        margin-bottom: 8px;
    }

    .section-caption {
        font-size: 14px;
        color: #64748b;
        margin-bottom: 18px;
        line-height: 1.6;
    }

    .summary-card {
        background-color: #ffffff;
        border: 1px solid #dbe7ee;
        border-radius: 16px;
        padding: 22px 24px;
        min-height: 150px;
        box-shadow: 0 4px 14px rgba(15, 23, 42, 0.045);
    }

    .summary-card:nth-of-type(1) {
        background-color: #f7fbfd;
    }

    .summary-card h3 {
        font-size: 14px;
        color: #5b7180;
        margin-bottom: 8px;
        font-weight: 650;
    }

    .summary-card h2 {
        font-size: 26px;
        color: #123047;
        margin-bottom: 8px;
        font-weight: 750;
    }

    .summary-card p {
        color: #475569;
        font-size: 14px;
        line-height: 1.6;
        margin: 0;
    }

    .result-card {
        background-color: #f4f9fb;
        border: 1px solid #bfd7e3;
        border-left: 5px solid #3b82a0;
        border-radius: 16px;
        padding: 24px;
        box-shadow: 0 4px 14px rgba(59, 130, 160, 0.08);
        margin-top: 10px;
    }

    .result-card h2 {
        color: #123047;
        font-size: 24px;
        margin-bottom: 8px;
        font-weight: 750;
    }

    .result-card h4 {
        color: #24566b;
        font-size: 16px;
        margin-bottom: 12px;
        font-weight: 700;
    }

    .result-card p {
        color: #475569;
        line-height: 1.65;
        margin: 0;
    }

    .cluster-chip {
        display: inline-block;
        padding: 7px 12px;
        border-radius: 999px;
        background-color: #edf7f2;
        color: #2f6b55;
        font-size: 13px;
        font-weight: 650;
        margin: 4px 4px 4px 0;
        border: 1px solid #cce5da;
    }

    .small-note {
        background-color: #fffaf0;
        border: 1px solid #f1dfb8;
        border-radius: 14px;
        padding: 16px 18px;
        color: #5b5140;
        font-size: 14px;
        line-height: 1.65;
    }

    .footer-note {
        color: #94a3b8;
        font-size: 12px;
        margin-top: 28px;
        line-height: 1.5;
    }

    div[data-testid="stMetric"] {
        background-color: #ffffff;
        border: 1px solid #dbe7ee;
        padding: 18px 20px;
        border-radius: 16px;
        box-shadow: 0 4px 14px rgba(15, 23, 42, 0.045);
    }

    div[data-testid="stMetric"]:hover {
        border-color: #a8c7d5;
        box-shadow: 0 6px 18px rgba(59, 130, 160, 0.10);
    }

    div[data-testid="stMetric"] label {
        color: #64748b !important;
        font-weight: 600;
    }

    div[data-testid="stMetricValue"] {
        color: #123047;
        font-weight: 750;
    }

    .stButton > button {
        border-radius: 12px;
        height: 46px;
        font-weight: 650;
        border: 1px solid #b7cbd4;
        background-color: #ffffff;
        color: #123047;
    }

    .stButton > button:hover {
        border-color: #3b82a0;
        color: #123047;
        background-color: #f0f7fb;
    }

    .stButton > button[kind="primary"] {
        background-color: #3b82a0;
        color: #ffffff;
        border: 1px solid #3b82a0;
    }

    .stButton > button[kind="primary"]:hover {
        background-color: #2f6f89;
        border: 1px solid #2f6f89;
        color: #ffffff;
    }

    textarea {
        border-radius: 14px !important;
        border: 1px solid #cbd5e1 !important;
        background-color: #ffffff !important;
    }

    textarea:focus {
        border-color: #3b82a0 !important;
        box-shadow: 0 0 0 1px #3b82a0 !important;
    }

    div[data-testid="stVerticalBlockBorderWrapper"] {
        border-color: #dbe7ee !important;
        border-radius: 16px !important;
        box-shadow: 0 4px 14px rgba(15, 23, 42, 0.035);
        background-color: #ffffff;
    }

    hr {
        border: none;
        border-top: 1px solid #e2e8f0;
        margin: 28px 0;
    }

    div[data-testid="stExpander"] {
        border: 1px solid #dbe7ee;
        border-radius: 14px;
        background-color: #ffffff;
    }

    div[data-testid="stAlert"] {
        border-radius: 14px;
    }
</style>
""", unsafe_allow_html=True)

# --- 4. FUNGSI TAMPILAN TAMBAHAN ---
def render_hero(title, description):
    st.markdown(f"""
    <div class="dashboard-hero">
        <h1>{title}</h1>
        <p>{description}</p>
    </div>
    """, unsafe_allow_html=True)


def tampilkan_referensi_cluster(compact=False):
    st.markdown('<div class="section-title">Cluster yang terbentuk</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-caption">Daftar berikut merangkum label dan makna setiap cluster.</div>',
        unsafe_allow_html=True
    )

    cols = st.columns(2)

    for idx, (k, v) in enumerate(info_klaster.items()):
        jumlah_dokumen = int(
            cluster_summary_data.loc[
                cluster_summary_data["Cluster"] == k,
                "Jumlah Dokumen"
            ].iloc[0]
        )

        persentase = float(
            cluster_summary_data.loc[
                cluster_summary_data["Cluster"] == k,
                "Persentase"
            ].iloc[0]
        )

        with cols[idx % 2]:
            with st.container(border=True):
                st.markdown(f"#### Cluster {k}")
                st.markdown(f"**{v['label']}**")

                if not compact:
                    st.write(v["deskripsi"])

                st.markdown(
                    f"**Jumlah dokumen:** {jumlah_dokumen:,}".replace(",", ".")
                )
                st.markdown(
                    f"**Persentase:** {persentase:.2f}%"
                )


def tampilkan_chip_terms(terms):
    for term in terms:
        st.markdown(f'<span class="cluster-chip">{term}</span>', unsafe_allow_html=True)


def load_scatter_data():
    scatter_path = Path("data_scatter_umap.csv")
    if not scatter_path.exists():
        return None

    df_plot = pd.read_csv(scatter_path)

    rename_map = {}
    if "umap_2d_x" in df_plot.columns and "X" not in df_plot.columns:
        rename_map["umap_2d_x"] = "X"
    if "umap_2d_y" in df_plot.columns and "Y" not in df_plot.columns:
        rename_map["umap_2d_y"] = "Y"
    if "cluster_k5" in df_plot.columns and "Cluster" not in df_plot.columns:
        rename_map["cluster_k5"] = "Cluster"

    if rename_map:
        df_plot = df_plot.rename(columns=rename_map)

    required_cols = {"X", "Y", "Cluster"}
    if not required_cols.issubset(set(df_plot.columns)):
        st.warning("File data_scatter_umap.csv ditemukan, tetapi kolom wajib X, Y, dan Cluster belum tersedia.")
        return None

    df_plot = df_plot[(df_plot["X"] >= -15) & (df_plot["X"] <= 22)]
    df_plot = df_plot[(df_plot["Y"] >= -6) & (df_plot["Y"] <= 3)]
    df_plot["Cluster"] = df_plot["Cluster"].astype(str)
    df_plot["Cluster"] = df_plot["Cluster"].apply(lambda x: x if x.startswith("Cluster") else f"Cluster {x}")
    df_plot = df_plot.sort_values("Cluster")
    return df_plot

def get_bigram_df(cluster_id):
    df_bigram = pd.DataFrame(
        cluster_bigram_data[cluster_id],
        columns=["Bigram", "Frekuensi"]
    )

    df_bigram = df_bigram.sort_values("Frekuensi", ascending=True)
    return df_bigram


def tampilkan_chart_bigram_streamlit(cluster_id):
    df_bigram = get_bigram_df(cluster_id)

    chart_data = df_bigram.set_index("Bigram")

    try:
        st.bar_chart(
            chart_data,
            horizontal=True,
            height=320,
            use_container_width=True
        )
    except TypeError:
        st.bar_chart(
            chart_data,
            height=320,
            use_container_width=True
        )

    st.dataframe(
        df_bigram.sort_values("Frekuensi", ascending=False),
        use_container_width=True,
        hide_index=True
    )


def get_cluster_summary():
    df = cluster_summary_data.copy()
    df["Nama Cluster"] = df["Cluster"].apply(lambda x: info_klaster[x]["label"])
    df["Cluster Label"] = df["Cluster"].apply(lambda x: f"Cluster {x}")
    return df

# --- 5. SIDEBAR NAVIGATION ---
with st.sidebar:
    logo_path = Path("logo_telkom.png")

    if logo_path.exists():
        st.image(str(logo_path), width=145)
    else:
        st.caption("Logo belum tersedia")

    st.markdown("### Dashboard Penelitian")
    st.caption("Klastering faktor penyebab gangguan kesehatan mental berbasis NLP")

    menu = st.radio(
        "Navigasi",
        [
            "📌 Ringkasan Penelitian",
            "🧩 Profil Cluster",
            "📊 Evaluasi & Visualisasi"
        ]
    )

    st.markdown("---")
    st.markdown("**Identitas Penelitian**")
    st.write("Peneliti: Nisa Trinanda Utami")
    st.write("Program Studi: Sistem Informasi")
    st.write("Metode: Word2Vec, TF-IDF, UMAP, K-Means")
    st.write("Jumlah cluster: K=5")

# --- 6. KONTEN DASHBOARD ---

# SECTION 1: RINGKASAN PENELITIAN
if menu == "📌 Ringkasan Penelitian":
    render_hero(
        "Ringkasan Penelitian",
        "Dashboard ini dikembangkan untuk menyajikan hasil klastering teks curhatan terkait kesehatan mental. Model digunakan untuk menemukan pola faktor penyebab gangguan kesehatan mental berdasarkan kedekatan semantik antar dokumen, bukan untuk melakukan diagnosis klinis."
    )

    st.markdown('<div class="section-title">Gambaran Umum Penelitian</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-caption">Bagian ini menjelaskan fokus penelitian, pendekatan model, dan keluaran utama yang dihasilkan.</div>',
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="summary-card">
            <h3>Fokus Penelitian</h3>
            <h2>Faktor Penyebab</h2>
            <p>Penelitian berfokus pada pemetaan pola curhatan kesehatan mental untuk menemukan kelompok isu yang memiliki kedekatan makna.</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="summary-card">
            <h3>Pendekatan Analisis</h3>
            <h2>Klastering Teks</h2>
            <p>Data teks diproses menggunakan Word2Vec berbobot TF-IDF, kemudian direduksi dengan UMAP dan dikelompokkan menggunakan K-Means.</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="summary-card">
            <h3>Keluaran Model</h3>
            <h2>5 Cluster</h2>
            <p>Model menghasilkan lima cluster utama yang merepresentasikan variasi faktor psikososial dalam data curhatan.</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    metrik1, metrik2, metrik3, metrik4 = st.columns(4)

    metrik1.metric(
        label="Total Dokumen Valid",
        value="3.447"
    )

    metrik2.metric(
        label="Jumlah Cluster",
        value="K=5"
    )

    metrik3.metric(
        label="Silhouette Score",
        value="0.4213"
    )

    metrik4.metric(
        label="Calinski-Harabasz",
        value="6538.24"
    )

    st.markdown("---")

    col_a, col_b = st.columns([1, 1], gap="large")

    with col_a:
        with st.container(border=True):
            st.markdown('<div class="section-title">Alur Pemodelan</div>', unsafe_allow_html=True)
            st.markdown("""
            <div class="small-note">
                <b>1. Preprocessing teks</b><br>
                Teks dibersihkan, dinormalisasi, diubah menjadi token, diproses dengan bigram, dan dibersihkan dari daftar noise.
                <br><br>
                <b>2. Pembentukan vektor</b><br>
                Token yang valid direpresentasikan menggunakan Word2Vec dan diberi bobot berdasarkan nilai IDF.
                <br><br>
                <b>3. Reduksi dimensi</b><br>
                Vektor teks direduksi menggunakan UMAP agar struktur semantik lebih mudah dipetakan.
                <br><br>
                <b>4. Klastering</b><br>
                Data dikelompokkan menggunakan K-Means dengan jumlah cluster sebanyak lima.
            </div>
            """, unsafe_allow_html=True)

    with col_b:
        with st.container(border=True):
            st.markdown('<div class="section-title">Catatan Penggunaan Dashboard</div>', unsafe_allow_html=True)
            st.markdown("""
            <div class="small-note">
                Dashboard ini tidak memberikan diagnosis psikologis dan tidak menerima input data baru untuk menentukan kondisi mental seseorang.
                <br><br>
                Dashboard hanya menyajikan hasil eksplorasi dari data historis yang telah dianalisis. Seluruh interpretasi perlu dibaca sebagai pola agregat hasil penelitian, bukan sebagai penilaian klinis terhadap individu.
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")
    tampilkan_referensi_cluster(compact=True)

    st.markdown("""
    <div class="footer-note">
        Catatan: Deployment pada dashboard ini berfungsi sebagai media presentasi hasil klastering dan interpretasi pola, bukan sebagai sistem prediksi data baru.
    </div>
    """, unsafe_allow_html=True)


# SECTION 2: PROFIL CLUSTER
elif menu == "🧩 Profil Cluster":

    st.markdown("""
    <div class="dashboard-hero">
        <h1>Profil Cluster</h1>
        <p>
            Halaman ini menampilkan karakteristik lima cluster hasil pemodelan berdasarkan
            ukuran cluster, bigram dominan, dan interpretasi psikolog.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # --- Menyiapkan data ringkasan cluster ---
    df_summary = cluster_summary_data.copy()
    df_summary["Nama Cluster"] = df_summary["Cluster"].apply(
        lambda x: info_klaster[int(x)]["label"]
    )
    df_summary["Cluster Label"] = df_summary["Cluster"].apply(
        lambda x: f"Cluster {int(x)}"
    )

    # --- Panel pemilihan cluster ---
    st.markdown('<div class="section-title">Pilih Cluster untuk Ditinjau</div>', unsafe_allow_html=True)

    cluster_options = [
        f"Cluster {int(row['Cluster'])} - {row['Nama Cluster']}"
        for _, row in df_summary.iterrows()
    ]

    selected_cluster_text = st.selectbox(
        "Cluster",
        cluster_options
    )

    selected_cluster = int(selected_cluster_text.split(" ")[1])
    selected_info = info_klaster[selected_cluster]
    selected_row = df_summary[df_summary["Cluster"] == selected_cluster].iloc[0]

    # --- Layout utama: interpretasi dan chart bigram ---
    col_info, col_chart = st.columns([0.92, 1.08], gap="large")

    with col_info:
        with st.container(border=True):
            st.markdown(f"""
            <div class="result-card">
                <h2>Cluster {selected_cluster}</h2>
                <h4>{selected_info["label"]}</h4>
                <p>{selected_info["deskripsi"]}</p>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("#### Ukuran Cluster")

            m1, m2 = st.columns(2)

            with m1:
                st.metric(
                    label="Jumlah Dokumen",
                    value=f"{int(selected_row['Jumlah Dokumen']):,}".replace(",", ".")
                )

            with m2:
                st.metric(
                    label="Proporsi Data",
                    value=f"{float(selected_row['Persentase']):.2f}%"
                )

            st.markdown("#### Catatan Interpretasi")
            st.markdown("""
            <div class="small-note">
                Interpretasi cluster dibaca sebagai gambaran tema dominan pada kumpulan data.
                Hasil ini tidak menunjukkan diagnosis klinis, tidak menilai kondisi individu,
                dan tidak menyatakan hubungan sebab-akibat secara langsung.
            </div>
            """, unsafe_allow_html=True)

    with col_chart:
        with st.container(border=True):
            st.markdown('<div class="section-title">Bigram Dominan</div>', unsafe_allow_html=True)
            st.markdown(
                '<div class="section-caption">Diagram batang horizontal berikut menunjukkan bigram atau frasa yang paling sering muncul pada cluster terpilih.</div>',
                unsafe_allow_html=True
            )

            # --- Data bigram cluster terpilih ---
            df_bigram = pd.DataFrame(
                cluster_bigram_data[selected_cluster],
                columns=["Bigram", "Frekuensi"]
            )

            df_bigram = df_bigram.sort_values("Frekuensi", ascending=True)

            # --- Chart horizontal menggunakan Streamlit ---
            try:
                st.bar_chart(
                    df_bigram.set_index("Bigram"),
                    horizontal=True,
                    height=320,
                    use_container_width=True
                )
            except TypeError:
                # Fallback jika versi Streamlit belum mendukung horizontal=True
                st.bar_chart(
                    df_bigram.set_index("Bigram"),
                    height=320,
                    use_container_width=True
                )

            st.dataframe(
                df_bigram.sort_values("Frekuensi", ascending=False),
                use_container_width=True,
                hide_index=True
            )

    st.markdown("---")

    # --- Ringkasan seluruh cluster ---
    st.markdown('<div class="section-title">Ringkasan Seluruh Cluster</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-caption">Tabel ini membantu pembaca membandingkan tema utama tiap cluster tanpa membuka satu per satu.</div>',
        unsafe_allow_html=True
    )

    df_ringkasan_cluster = df_summary.copy()

    df_ringkasan_cluster["Cluster"] = df_ringkasan_cluster["Cluster"].apply(
        lambda x: f"Cluster {int(x)}"
    )

    df_ringkasan_cluster = df_ringkasan_cluster.rename(columns={
        "Nama Cluster": "Interpretasi Psikolog",
        "Jumlah Dokumen": "Jumlah Dokumen",
        "Persentase": "Persentase (%)"
    })

    df_ringkasan_cluster = df_ringkasan_cluster[
        [
            "Cluster",
            "Interpretasi Psikolog",
            "Jumlah Dokumen",
            "Persentase (%)"
        ]
    ]

    st.dataframe(
        df_ringkasan_cluster,
        use_container_width=True,
        hide_index=True
    )

    st.markdown("""
    <div class="footer-note">
        Catatan: Ringkasan cluster disusun berdasarkan kemunculan bigram dominan dan interpretasi ahli sebagai gambaran tematik dari data penelitian.
    </div>
    """, unsafe_allow_html=True)

## SECTION 3: EVALUASI DAN VISUALISASI MODEL
elif menu == "📊 Evaluasi & Visualisasi":

    st.markdown("""
    <div class="dashboard-hero">
        <h1>Evaluasi & Visualisasi</h1>
        <p>
            Halaman ini menampilkan kualitas struktur cluster dan sebaran dokumen
            dalam ruang representasi dua dimensi. Fokus halaman ini adalah membaca
            keterpisahan, kerapatan, dan pola posisi antarcluster.
        </p>
    </div>
    """, unsafe_allow_html=True)

    df_summary = get_cluster_summary()

    # --- KPI RINGKAS ---
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)

    with kpi1:
        st.metric(
            label="Total Dokumen Valid",
            value=f"{df_summary['Jumlah Dokumen'].sum():,}".replace(",", ".")
        )

    with kpi2:
        st.metric(
            label="Jumlah Cluster",
            value="K=5"
        )

    with kpi3:
        st.metric(
            label="Silhouette Score",
            value="0.4213"
        )

    with kpi4:
        st.metric(
            label="Calinski-Harabasz",
            value="6538.24"
        )

    st.markdown("---")

    # --- DATA KUALITAS CLUSTER ---
    # Jika sudah punya cluster_quality.csv dari notebook, dashboard akan memakai file itu.
    # Jika belum ada, dashboard memakai cluster_summary_data.
    quality_path = Path("cluster_quality.csv")

    if quality_path.exists():
        df_quality = pd.read_csv(quality_path)
        df_quality["Cluster"] = df_quality["Cluster"].astype(int)
        df_quality["Cluster Label"] = df_quality["Cluster"].apply(lambda x: f"Cluster {x}")
    else:
        df_quality = df_summary.copy()

    # --- LAYOUT UTAMA ---
    col_umap, col_quality = st.columns([1.45, 0.55], gap="large")

    with col_umap:
        with st.container(border=True):
            st.markdown('<div class="section-title">Sebaran UMAP 2D dengan Centroid Cluster</div>', unsafe_allow_html=True)
            st.markdown(
                '<div class="section-caption">Visualisasi ini menunjukkan posisi dokumen berdasarkan kedekatan semantik. Titik centroid digunakan sebagai pusat representasi tiap cluster.</div>',
                unsafe_allow_html=True
            )

            scatter_path = Path("data_scatter_umap.csv")

            if scatter_path.exists():
                df_plot = pd.read_csv(scatter_path)

                # Pastikan nama kolom sesuai
                df_plot["Cluster"] = df_plot["Cluster"].astype(int)
                df_plot["Cluster Label"] = df_plot["Cluster"].apply(lambda x: f"Cluster {x}")

                # Filter outlier agar tampilan lebih bersih
                df_plot = df_plot[(df_plot["X"] >= -15) & (df_plot["X"] <= 22)]
                df_plot = df_plot[(df_plot["Y"] >= -6) & (df_plot["Y"] <= 3)]

                # Scatter dokumen
                st.scatter_chart(
                    df_plot,
                    x="X",
                    y="Y",
                    color="Cluster Label",
                    height=460,
                    use_container_width=True
                )

                # Tabel centroid sebagai pelengkap, karena st.scatter_chart tidak mendukung marker X centroid
                centroid_df = (
                    df_plot
                    .groupby("Cluster Label", as_index=False)
                    .agg(
                        Centroid_X=("X", "mean"),
                        Centroid_Y=("Y", "mean"),
                        Jumlah_Titik=("Cluster", "count")
                    )
                )

                with st.expander("Lihat titik centroid tiap cluster"):
                    st.dataframe(
                        centroid_df,
                        use_container_width=True,
                        hide_index=True
                    )

            else:
                st.warning(
                    "File data_scatter_umap.csv belum ditemukan. Ekspor koordinat UMAP 2D dari notebook agar visualisasi sebaran cluster dapat ditampilkan."
                )

    with col_quality:
        with st.container(border=True):
            st.markdown('<div class="section-title">Kerapatan Cluster</div>', unsafe_allow_html=True)
            st.markdown(
                '<div class="section-caption">Nilai silhouette per cluster menunjukkan seberapa kompak anggota cluster terhadap kelompoknya.</div>',
                unsafe_allow_html=True
            )

            chart_quality = df_quality[["Cluster Label", "Silhouette Cluster"]].set_index("Cluster Label")

            try:
                st.bar_chart(
                    chart_quality,
                    horizontal=True,
                    height=300,
                    use_container_width=True
                )
            except TypeError:
                st.bar_chart(
                    chart_quality,
                    height=300,
                    use_container_width=True
                )

            cluster_terkompak = df_quality.sort_values("Silhouette Cluster", ascending=False).iloc[0]
            cluster_tersebar = df_quality.sort_values("Silhouette Cluster", ascending=True).iloc[0]

            st.markdown(f"""
            <div class="small-note">
                <b>Cluster paling kompak:</b><br>
                {cluster_terkompak["Cluster Label"]} dengan silhouette {cluster_terkompak["Silhouette Cluster"]:.4f}
                <br><br>
                <b>Cluster paling menyebar:</b><br>
                {cluster_tersebar["Cluster Label"]} dengan silhouette {cluster_tersebar["Silhouette Cluster"]:.4f}
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")

    # --- TABEL EVALUASI CLUSTER ---
    with st.container(border=True):
        st.markdown('<div class="section-title">Tabel Kualitas Cluster</div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="section-caption">Tabel ini merangkum ukuran dan kerapatan setiap cluster sebagai pelengkap visualisasi UMAP.</div>',
            unsafe_allow_html=True
        )

        df_eval_cluster = df_quality.copy()

        if "Nama Cluster" not in df_eval_cluster.columns:
            df_eval_cluster["Nama Cluster"] = df_eval_cluster["Cluster"].apply(
                lambda x: info_klaster[int(x)]["label"]
            )

        df_eval_cluster = df_eval_cluster[
            [
                "Cluster Label",
                "Nama Cluster",
                "Jumlah Dokumen",
                "Silhouette Cluster"
            ]
        ].rename(columns={
            "Cluster Label": "Cluster",
            "Nama Cluster": "Interpretasi Psikolog",
            "Silhouette Cluster": "Kerapatan Cluster"
        })

        st.dataframe(
            df_eval_cluster,
            use_container_width=True,
            hide_index=True
        )

    st.markdown("""
    <div class="footer-note">
        Catatan metodologis: Visualisasi UMAP memperlihatkan sebaran dokumen dalam ruang dua dimensi,
        sedangkan silhouette per cluster digunakan untuk membaca tingkat kerapatan masing-masing kelompok.
    </div>
    """, unsafe_allow_html=True)