import os
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from PIL import Image

# Configuración de estilo
sns.set_theme(style="darkgrid")

# 1. Definición de rutas (adaptadas a tu entorno macOS)
init_dir = "/Users/vic/Library/CloudStorage/OneDrive-InstitutoPolitecnicoNacional/Investigacion/MagneticNanoParticles/V2026/SW1P"
file_base = "SW1P_ThF90A90"

eps_path = os.path.join(init_dir, "eps", f"{file_base}.eps")
pdf_path = os.path.join(init_dir, "eps", f"{file_base}.pdf")
txt_path = os.path.join(init_dir, "txt", f"{file_base}.txt")
out_fig_path = os.path.join(init_dir, "res", f"{file_base}_combinado.png")

print("Directorio de trabajo:", init_dir)

# 2. Conversión de EPS a PDF y preparación de la imagen para matplotlib
print(f"Convirtiendo {file_base}.eps en {file_base}.pdf ...")
with Image.open(eps_path) as img:
    # Convertimos a RGB para poder guardarlo correctamente y visualizarlo
    img_rgb = img.convert('RGB')
    
    # Guardamos como PDF
    img_rgb.save(pdf_path, "PDF", resolution=100.0)
    print("✅ EPS convertido a PDF exitosamente.")
    
    # Redimensionamos la imagen para el subplot (al 65% como en tu script original)
    new_width = int(img_rgb.size[0] * 0.65)
    new_height = int(img_rgb.size[1] * 0.65)
    resized_img = img_rgb.resize((new_width, new_height))

# 3. Lectura de datos de histéresis
print(f"Leyendo datos de {file_base}.txt ...")
# Leemos el archivo y asignamos los nombres de las columnas que arroja tu modelo
df = pd.read_table(txt_path, sep='\t', header=None)
df = df.set_axis(['hx', 'hy', 'E', 'mx', 'my'], axis=1)

# 4. Creación de la figura combinada
fig, axes = plt.subplots(2, 1, figsize=(6, 10))

# --- Subplot 0: Curva de Histéresis ---
axes[0].plot(df['hy'], df['my'], linestyle="-", alpha=1, color="#4C72B0", label="$\phi=90$")
axes[0].set_xlabel('$h_y$')
axes[0].set_ylabel('$M/M_s$ (Componente $m_y$)')
axes[0].set_xlim((-1, 1))
axes[0].set_title("Curva de Histéresis (A=90)")
axes[0].legend(loc='lower right')

# --- Subplot 1: Visualización del estado magnético (EPS convertido) ---
axes[1].imshow(resized_img)
axes[1].set_xticks([])
axes[1].set_yticks([])
axes[1].set_title("Potencial Magnetostático")

# Ajustamos el espaciado para que no se empalmen los títulos
plt.tight_layout()

# 5. Guardar y mostrar
plt.savefig(out_fig_path, dpi=300)
print(f"✅ Figura combinada guardada en: {out_fig_path}")

plt.show()
plt.close(fig)

print("Proceso finalizado con éxito.")