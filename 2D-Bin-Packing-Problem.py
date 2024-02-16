import random
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import tkinter as tk
from tkinter import scrolledtext, messagebox
import numpy as np


def input_giris():
    genislik = genislik_giris.get().strip()
    yukseklik = yukseklik_giris.get().strip()

    if genislik.isdigit() and yukseklik.isdigit():
        genislik = int(genislik)
        yukseklik = int(yukseklik)

        if genislik > 20 or yukseklik > 20:
            messagebox.showerror("Hata", "Genişlik ve yükseklik 20'den büyük olamaz.")
        else:
            input_list.append((genislik, yukseklik))
            output_text.insert(tk.END, f"{genislik}, {yukseklik}\n")
    else:
        messagebox.showerror("Hata", "Lütfen sayısal bir değer girin.")

    genislik_giris.delete(0, tk.END)
    yukseklik_giris.delete(0, tk.END)


def alan_hesaplama(yerlestirme):
    toplam_alan = 20 * 20
    kullanilan_alan = 0
    for parca, kordinatlar in yerlestirme.items():
        if isinstance(parca, int):
            kullanilan_alan += yerlestirme[parca]['width'] * yerlestirme[parca]['height']
        else:
            kullanilan_alan += parca[0] * parca[1]
    return toplam_alan - kullanilan_alan

def en_uygun_yerlesim(parcalar):
    plaka_boyutu = (20, 20)
    sirali_dikdortgenler = sorted(parcalar, key=lambda x: x[0] * x[1], reverse=True)
    yerlestirilmis_dikdortgenler={}

    for rect_id, rect_size in enumerate(sirali_dikdortgenler):
        width, height = rect_size

        # Dikdörtgenin en iyi uyduğu konumu ara
        eniyi_yerlesim = None
        min_artakalan = float('inf')

        for x in range(plaka_boyutu[0] - width + 1):
            for y in range(plaka_boyutu[1] - height + 1):
                # Dikdörtgenin bu konumda uygun olup olmadığını kontrol et
                overlap = False
                for a in yerlestirilmis_dikdortgenler.values():
                    if (
                            x < a['x'] + a['width'] and
                            x + width > a['x'] and
                            y < a['y'] + a['height'] and
                            y + height > a['y']
                    ):
                        overlap = True
                        break

                # Eğer çakışma yoksa, skoru güncelle
                if not overlap:
                    skor = max(plaka_boyutu[0] - (x + width), plaka_boyutu[1] - (y + height))

                    # Eğer skor daha iyiyse, en iyi uygun yerlesim güncelle
                    if skor < min_artakalan:
                        min_artakalan = skor
                        eniyi_yerlesim = {'x': x, 'y': y}

        # En iyi uygun konumu bulduysak, dikdörtgeni yerleştir
        if eniyi_yerlesim is not None:
            yerlestirilmis_dikdortgenler[rect_id] = {'x': eniyi_yerlesim['x'], 'y': eniyi_yerlesim['y'], 'width': width, 'height': height}

    result = []
    for item in yerlestirilmis_dikdortgenler:
        parcalar = yerlestirilmis_dikdortgenler[item]
        result.append((parcalar["width"], parcalar["height"], parcalar["x"], parcalar["y"]))

    return result

#calıştır buttonuna bastıktan sonra cıkan cıktılar hakkında bilgiveren kısım
def sonuc(input_list):
    result_window = tk.Toplevel(root)
    result_window.title("Sonuçlar")
    result_text = scrolledtext.ScrolledText(result_window, wrap=tk.WORD, width=60, height=32)
    result_text.pack(pady=10)

    for i, (g, y) in enumerate(input_list, start=1):
        result_text.insert(tk.END, f"{i}. Parça: {g}, {y}\n")

    # Get the output from yerlestirme function
    eniyi_yerlesim = en_uygun_yerlesim(input_list)

    result_text.insert(tk.END, f"\nOptimum Yerleşim:\n")
    for i, (width, height, x, y) in enumerate(eniyi_yerlesim, start=1):
        result_text.insert(tk.END, f"Parça {i}, Boyutlar: {width},{height}, Koordinatlar: ({x}, {y})\n")

    min_artakalan = alan_hesaplama(
        {i: {'x': x, 'y': y, 'width': width, 'height': height} for i, (width, height, x, y) in
         enumerate(eniyi_yerlesim, start=1)})

    result_text.insert(tk.END, f"\nArta Kalan Alan: {min_artakalan}\n")

#calıştır buttonuna bastıktan sonra cıkan cıktıların kordınat verısıne gore gorsellestırme
def cizdir(dikdortgen):
    fig, ax = plt.subplots(figsize=(5, 5))

    for rect_params in dikdortgen:
        length, width, x, y = rect_params
        dikdortgen = patches.Rectangle((x, y), length, width, edgecolor='black',
                                      facecolor=(random.random(), random.random(), random.random()))
        ax.add_patch(dikdortgen)

    ax.set(xlim=(0, 20), xticks=np.arange(0, 21),
           ylim=(0, 20), yticks=np.arange(0, 21))
    ax.set_aspect('equal', 'box')
    ax.grid(True, linestyle='--', alpha=0.5)  # Add grid lines

    plt.show()

#iki fonksiyonu cagırdıgımız fonksıyon
def sonuc_cizdir():
    sonuc(input_list)
    result = en_uygun_yerlesim(input_list)
    cizdir(result)



# Ana pencereyi oluşturur
root = tk.Tk()
root.title("2D Düzgün Dikdörtgensel Paketleme")
# Pencere boyutunu ayarlama
root.geometry("500x500")
root.configure(bg='lightgray')
# genislik inputu
genislik = tk.Label(root, text="Genişlik (Sayı):", font=("Arial", 15, "bold"), fg="black")
genislik.pack(pady=5)

genislik_giris = tk.Entry(root, font=("Arial", 12))
genislik_giris.pack(pady=10)

# yukseklik inputu
yukseklik = tk.Label(root, text="Yükseklik (Sayı):", font=("Arial", 15, "bold"), fg="black")
yukseklik.pack(pady=5)

yukseklik_giris = tk.Entry(root, font=("Arial", 12))
yukseklik_giris.pack(pady=10)

# Buttonları yan yana al
button_frame = tk.Frame(root)
button_frame.pack(pady=10)

ekle_button = tk.Button(button_frame, text="Ekle", command=input_giris, font=("Arial", 12), bg="red", fg="white")
ekle_button.pack(side=tk.LEFT, padx=10)

calistir_button = tk.Button(button_frame, text="Çalıştır", command=sonuc_cizdir, font=("Arial", 12), bg="green", fg="white")
calistir_button.pack(side=tk.LEFT, padx=10)

# Çıkış alanını oluştur
ciktialan = tk.Label(root, text="Girilen Değerler:", font=("Arial", 15, "bold"), fg="black")
ciktialan.pack(pady=5)

output_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=40, height=10, font=("Arial", 10))
output_text.pack(pady=10)

# Inputları tuttuğumuz liste
input_list = []

# Pencereyi çalıştırır
root.mainloop()

