# PYNQ Z2 YÜZ TANIMA

Proje geliştirilirken ageitgey/face_recognition kütüphanesi ve bu kütüphane ile
birlikte yardımcı olarak opencv-python kütüphanesi kullanılmıştır.
Geliştirme gömülü sistemler üzerinden devam edeceğinden burada Pynq Z2 kartı
kullanılmış olup, bu kartın HDMI çıkışını ve buttonlarını kullanabilmek için ek olarak pynq
kütüphanesi de kullanılmıştır. <br/>

Bu kütüphane ilk olarak tanınması istenen yüzlerin kaş, göz, burun, ağız ve yüz
çevresininin konumlarını tespit eder ve bu konumlar ile her yüzü ayrı ayrı şifrelemiş olur.
Tespit edilmesi istenen yüz sisteme girdi olarak verildiğinde, verilen yüz ayrıca
şifrelenir ve önceden şifrelenmiş olan yüzler ile karşılaştırılarak en yüksek uyum oranına
sahip yüzü seçer.