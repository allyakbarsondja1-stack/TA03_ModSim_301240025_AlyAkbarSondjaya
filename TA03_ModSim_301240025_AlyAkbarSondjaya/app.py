import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="TA-03 Simulasi Risiko Klaim Asuransi", layout="centered"
)
st.title("📊 Simulasi Monte Carlo: Estimasi Risiko Klaim Asuransi")
st.caption("NIM: 301240025 | Nama: Aly Akbar Sondjaya")

# 1. Load & bersihkan data
df = pd.read_csv("insurance.csv").dropna(subset=["charges"]).copy()
charges = df["charges"]
mean_charge = charges.mean()
std_charge = charges.std()

with st.expander("Lihat Statistik Historis Dataset (insurance.csv)"):
  st.write(f"- Jumlah data valid: **{len(charges)}** baris")
  st.write(f"- Rata-rata klaim (**Mean / μ**): **${mean_charge:,.2f}**")
  st.write(f"- Standar deviasi (**Std Dev / σ**): **${std_charge:,.2f}**")

# 2. Input parameter simulasi
st.subheader("Pengaturan Parameter Simulasi")
num_patients = st.number_input(
    "Jumlah Pasien Baru", min_value=1, max_value=1000, value=100, step=10
)
num_simulations = st.number_input(
    "Jumlah Skenario (Minimal 5.000)",
    min_value=5000,
    max_value=50000,
    value=10000,
    step=1000,
)
budget_threshold = st.number_input(
    "Batas Anggaran Klaim / Threshold (USD)",
    min_value=100000,
    max_value=10000000,
    value=1400000,
    step=50000,
)

# 3. Jalankan simulasi Monte Carlo
np.random.seed(301240025)
total_claims = []
for _ in range(int(num_simulations)):
  sim_charges = np.random.normal(
      loc=mean_charge, scale=std_charge, size=int(num_patients)
  )
  sim_charges = np.maximum(sim_charges, 0)
  total_claims.append(np.sum(sim_charges))

total_claims = np.array(total_claims)
exceed_budget = np.sum(total_claims > budget_threshold)
prob_exceed = (exceed_budget / num_simulations) * 100
mean_total_sim = np.mean(total_claims)

# 4. Ringkasan hasil
st.subheader("Hasil Analisis Risiko")
col1, col2, col3 = st.columns(3)
col1.metric("Rata-rata Total Klaim", f"${mean_total_sim:,.2f}")
col2.metric("Skenario Over-Budget", f"{exceed_budget:,} / {int(num_simulations):,}")
col3.metric("Probabilitas Melebihi Anggaran", f"{prob_exceed:.2f}%")

# 5. Histogram hasil simulasi & garis batas (threshold)
fig, ax = plt.subplots(figsize=(8, 4.5))
ax.hist(
    total_claims,
    bins=40,
    color="lightgreen",
    edgecolor="black",
    alpha=0.85,
    label="Hasil Simulasi Total Klaim",
)
ax.axvline(
    budget_threshold,
    color="red",
    linestyle="--",
    linewidth=2,
    label=f"Threshold Anggaran: {budget_threshold:,.0f}",
)
ax.axvline(
    mean_total_sim,
    color="blue",
    linestyle="-.",
    linewidth=2,
    label=f"Rata-rata Simulasi: {mean_total_sim:,.2f}",
)
ax.set_title(
    f"Distribusi Hasil Simulasi Monte Carlo Total Klaim ({int(num_patients)} Pasien)"
)
ax.set_xlabel("Total Klaim (USD)")
ax.set_ylabel("Frekuensi Skenario")
ax.legend()
ax.grid(axis="y", alpha=0.3)
st.pyplot(fig)