import time
import random
import pandas as pd
import matplotlib.pyplot as plt
import sys
sys.setrecursionlimit(7500) # öz yineleme fonksiyonu sınırını arttırmak için kullandık


# Merge Sort Algoritması
def merge_sort(dizi):
    if len(dizi) > 1:
        orta = len(dizi) // 2
        sol_yarim = dizi[:orta]
        sag_yarim = dizi[orta:]

        merge_sort(sol_yarim)
        merge_sort(sag_yarim)

        i = j = k = 0
        while i < len(sol_yarim) and j < len(sag_yarim):
            if sol_yarim[i] < sag_yarim[j]:
                dizi[k] = sol_yarim[i]
                i += 1
            else:
                dizi[k] = sag_yarim[j]
                j += 1
            k += 1

        while i < len(sol_yarim):
            dizi[k] = sol_yarim[i]
            i += 1
            k += 1

        while j < len(sag_yarim):
            dizi[k] = sag_yarim[j]
            j += 1
            k += 1

# Quick Sort Algoritması
def quick_sort(dizi, baslangic, bitis):
    if baslangic < bitis:
        p = bolme(dizi, baslangic, bitis)
        quick_sort(dizi, baslangic, p - 1)
        quick_sort(dizi, p + 1, bitis)

def bolme(dizi, baslangic, bitis):
    pivot = dizi[bitis]
    i = baslangic - 1
    for j in range(baslangic, bitis):
        if dizi[j] < pivot:
            i += 1
            dizi[i], dizi[j] = dizi[j], dizi[i]
    dizi[i + 1], dizi[bitis] = dizi[bitis], dizi[i + 1]
    return i + 1

# Insertion Sort Algoritması
def insertion_sort(dizi):
    for i in range(1, len(dizi)):
        anahtar = dizi[i]
        j = i - 1
        while j >= 0 and dizi[j] > anahtar:
            dizi[j + 1] = dizi[j]
            j -= 1
        dizi[j + 1] = anahtar

# Çalışma süresini ölçme fonksiyonu
def sure_olc(siralama_fonksiyonu, dizi, *args):
    baslangic = time.time()
    siralama_fonksiyonu(dizi, *args)
    bitis = time.time()
    return bitis - baslangic

# Test için farklı dizi boyutları
dizi_boyutlari = [10, 50, 100, 500, 1100, 1300, 1500, 1700, 1900, 2100, 5000, 7000]
sonuclar = []

# Her sıralama algoritmasını en iyi, en kötü ve ortalama durumda çalıştır
for boyut in dizi_boyutlari:
    en_iyi_dizi = list(range(boyut))
    en_kotu_dizi = list(range(boyut, 0, -1))
    ortalama_dizi = [random.randint(1, boyut) for _ in range(boyut)]
    
    for siralama_fonksiyonu, isim in [(merge_sort, 'Merge Sort'), 
                                      (lambda dizi: quick_sort(dizi, 0, len(dizi) - 1), 'Quick Sort'), 
                                      (insertion_sort, 'Insertion Sort')]:
        
        en_iyi_sure = sure_olc(siralama_fonksiyonu, en_iyi_dizi.copy())
        en_kotu_sure = sure_olc(siralama_fonksiyonu, en_kotu_dizi.copy())
        ortalama_sure = sure_olc(siralama_fonksiyonu, ortalama_dizi.copy())
        
        sonuclar.append((isim, boyut, en_iyi_sure, en_kotu_sure, ortalama_sure))

# Sonuçları DataFrame'e dönüştür
df = pd.DataFrame(sonuclar, columns=['Algoritma', 'Dizi Boyutu', 'En İyi Durum', 'En Kötü Durum', 'Ortalama Durum'])

# DataFrame'i göster
print(df)

# Sonuçları grafikle göster
for isim in df['Algoritma'].unique():
    alt_kume = df[df['Algoritma'] == isim]
    plt.plot(alt_kume['Dizi Boyutu'], alt_kume['En İyi Durum'], label=f'{isim} En İyi Durum', marker='o')
    plt.plot(alt_kume['Dizi Boyutu'], alt_kume['En Kötü Durum'], label=f'{isim} En Kötü Durum', marker='o')
    plt.plot(alt_kume['Dizi Boyutu'], alt_kume['Ortalama Durum'], label=f'{isim} Ortalama Durum', marker='o')

plt.xlabel("Dizi Boyutu")
plt.ylabel("Süre (saniye)")
plt.title("Sıralama Algoritmaları Performans Analizi")
plt.legend()
plt.grid(True)
plt.show()
-------------------------------------------------------------------------------------------------------------------------------------------

import random  # Rastgele sayı üretmek için gerekli modülü içe aktarıyoruz
import time  # Zaman ölçümleri yapmak için gerekli modülü içe aktarıyoruz
import matplotlib.pyplot as plt  # Grafik çizimi için Matplotlib kütüphanesini içe aktarıyoruz
import pandas as pd  # Veri çerçevesi oluşturmak için Pandas kütüphanesini içe aktarıyoruz


# Yinelemeli Quick Sort fonksiyonu - Pivot seçimini duruma göre yapıyoruz
def quick_sort_siralama(arr, pivot_strategy="last"):
    stack = [(0, len(arr) - 1)]  # Quick Sort için başlangıç ve bitiş indekslerini yığına ekliyoruz

    while stack:  # Yığın boş olmadığı sürece döngüyü devam ettiriyoruz
        start, end = stack.pop()  # Yığından bir başlangıç ve bitiş değeri alıyoruz
        if start >= end:  # Eğer dizi tek bir elemansa devam etmiyoruz
            continue

        # Pivot seçimi stratejisine göre pivot belirleme
        if pivot_strategy == "last":  # Pivot stratejisi "last" ise, pivotu son elemana ayarlıyoruz
            pivot_index = end
        elif pivot_strategy == "first":  # Pivot stratejisi "first" ise, pivotu ilk elemana ayarlıyoruz
            pivot_index = start
        elif pivot_strategy == "middle":  # Pivot stratejisi "middle" ise, pivotu ortadaki elemana ayarlıyoruz
            pivot_index = (start + end) // 2

        pivot = arr[pivot_index]  # Seçilen pivot değerini alıyoruz
        arr[pivot_index], arr[end] = arr[end], arr[pivot_index]  # Pivotu sona taşıyoruz

        low = start  # Küçük elemanları işaret eden başlangıç indeksini ayarlıyoruz
        high = end - 1  # Büyük elemanları işaret eden bitiş indeksini ayarlıyoruz

        while True:  # Sonsuz bir döngü ile elemanları karşılaştırarak yer değiştiriyoruz
            while low <= high and arr[low] < pivot:  # Pivot değerinden küçük elemanları arıyoruz
                low += 1
            while low <= high and arr[high] >= pivot:  # Pivot değerine eşit veya büyük elemanları arıyoruz
                high -= 1
            if low <= high:  # Eğer hala karşılaştırılacak eleman varsa takas yapıyoruz
                arr[low], arr[high] = arr[high], arr[low]
            else:  # Karşılaştırma bittiyse döngüden çıkıyoruz
                break

        arr[low], arr[end] = arr[end], arr[low]  # Pivotu doğru konumuna yerleştiriyoruz

        stack.append((start, low - 1))  # Sol alt diziyi yığına ekliyoruz
        stack.append((low + 1, end))  # Sağ alt diziyi yığına ekliyoruz


# Zaman ölçme fonksiyonu
def zaman_olc(arr, pivot_strategy="last"):
    baslangic = time.time()  # İşlem başlangıç zamanını kaydediyoruz
    quick_sort_siralama(arr, pivot_strategy)  # Quick Sort fonksiyonunu çağırıyoruz
    bitis = time.time()  # İşlem bitiş zamanını kaydediyoruz
    return bitis - baslangic  # Çalışma süresini döndürüyoruz


# Farklı büyüklüklerdeki giriş verileri
dizi_boyutlari = [10, 50, 100, 500, 1100, 1300, 1500, 1700, 1900, 2100, 5000, 7000]  # Test edilecek dizi boyutları
zamanlar_en_iyi = []  # En iyi durum çalışma sürelerini saklamak için boş liste
zamanlar_en_kotu = []  # En kötü durum çalışma sürelerini saklamak için boş liste
zamanlar_ortalama = []  # Ortalama durum çalışma sürelerini saklamak için boş liste

# Zaman ölçümleri
for boyut in dizi_boyutlari:  # Her dizi boyutu için zaman ölçümü yapıyoruz
    random_arr = [random.randint(1, boyut) for _ in range(boyut)]  # Rastgele dizi oluşturuyoruz
    zamanlar_ortalama.append(zaman_olc(random_arr.copy(), "middle"))  # Ortalama durumu ölçüyoruz

    sorted_arr = sorted(random_arr)  # Sıralı dizi oluşturuyoruz
    zamanlar_en_iyi.append(zaman_olc(sorted_arr.copy(), "middle"))  # En iyi durumu ölçüyoruz

    reversed_arr = sorted_arr[::-1]  # Ters sıralı dizi oluşturuyoruz
    zamanlar_en_kotu.append(zaman_olc(reversed_arr.copy(), "first"))  # En kötü durumu ölçüyoruz

# Grafik çizimi
plt.figure(figsize=(10, 6))  # Grafik boyutlarını ayarlıyoruz
plt.plot(dizi_boyutlari, zamanlar_en_iyi, label='En İyi Durum (O(n log(n)))', marker='o')  # En iyi durum grafiği
plt.plot(dizi_boyutlari, zamanlar_en_kotu, label='En Kötü Durum (O(n^2))', marker='o')  # En kötü durum grafiği
plt.plot(dizi_boyutlari, zamanlar_ortalama, label='Ortalama Durum (O(n log(n)))', marker='o')  # Ortalama durum grafiği
plt.xlabel('Girdi Boyutu')  # X ekseni etiketini ayarlıyoruz
plt.ylabel('Çalışma Süresi (saniye)')  # Y ekseni etiketini ayarlıyoruz
plt.title('Quick Sort Çalışma Süresi')  # Grafiğe başlık ekliyoruz
plt.legend()  # Grafik açıklamalarını gösteriyoruz
plt.grid(True)  # Grafik ızgarasını açıyoruz
plt.show()  # Grafiği görüntülüyoruz

# Çıktı verilerini bir DataFrame içine alıyoruz
df_sonuclar = pd.DataFrame({
    "Dizi Boyutu": dizi_boyutlari,  # Dizi boyutları sütunu
    "En İyi Durum (saniye)": zamanlar_en_iyi,  # En iyi durum süreleri sütunu
    "En Kötü Durum (saniye)": zamanlar_en_kotu,  # En kötü durum süreleri sütunu
    "Ortalama Durum (saniye)": zamanlar_ortalama  # Ortalama durum süreleri sütunu
})

pd.set_option('display.max_rows', None)  # Tüm satırları gösterme ayarını yapıyoruz
pd.set_option('display.max_columns', None)  # Tüm sütunları gösterme ayarını yapıyoruz
print(df_sonuclar)  # Zaman ölçüm sonuçlarını ekrana yazdırıyoruz
---------------------------------------
def quick_sort(dizi, baslangic, bitis):
    if baslangic < bitis:  # Eğer başlangıç indeksi, bitiş indeksinden küçükse (sıralama yapılacak eleman varsa)
        p = bolme(dizi, baslangic, bitis)  # Diziyi böl ve pivot indeksini al
        quick_sort(dizi, baslangic, p - 1)  # Pivotun sol tarafındaki parçayı sıralamak için quick_sort'u çağır
        quick_sort(dizi, p + 1, bitis)  # Pivotun sağ tarafındaki parçayı sıralamak için quick_sort'u çağır

def bolme(dizi, baslangic, bitis):
    pivot = dizi[bitis]  # Bitiş indeksindeki elemanı pivot olarak seç
    i = baslangic - 1  # `i`'yi, dizi içinde sol tarafı işaret edecek şekilde ayarla
    for j in range(baslangic, bitis):  # Başlangıçtan bitişe kadar tüm elemanları kontrol et
        if dizi[j] < pivot:  # Eğer `dizi[j]` pivot'tan küçükse
            i += 1  # `i`'yi bir arttır
            dizi[i], dizi[j] = dizi[j], dizi[i]  # `dizi[i]` ile `dizi[j]`'yi yer değiştir (küçük elemanları sola kaydır)
    dizi[i + 1], dizi[bitis] = dizi[bitis], dizi[i + 1]  # Pivot elemanını doğru konuma yerleştir
    return i + 1  # Pivot'un yeni indeksini döndür
