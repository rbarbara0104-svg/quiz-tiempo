import os

# Carpeta donde están las imágenes
image_folder = 'static/images'

# Contadores
missing_files = []

# Revisar cada pregunta
for i in range(1, 31):
    expected_files = [
        f"intro{i}a.jpeg",
        f"intro{i}b.jpeg",
        f"option{i}a.jpeg",
        f"option{i}b.jpeg"
    ]
    for filename in expected_files:
        path = os.path.join(image_folder, filename)
        if not os.path.isfile(path):
            missing_files.append(filename)

# Resultado
if missing_files:
    print("⚠️ Faltan estas imágenes o están mal nombradas:")
    for f in missing_files:
        print(f"  - {f}")
else:
    print("✅ Todas las imágenes existen y están correctamente nombradas.")
