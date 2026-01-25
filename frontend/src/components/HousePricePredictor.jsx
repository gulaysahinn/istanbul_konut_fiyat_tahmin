import { useState } from "react";
import {
  Home,
  MapPin,
  Ruler,
  DoorOpen,
  Building2,
  Flame,
  CheckCircle,
  Calculator,
  Sparkles,
  Wallet,
  TrendingUp,
  Star,
  ArrowRight,
  MessageCircle,
  Send,
} from "lucide-react";

const ILCELER = [
  "Adalar",
  "Arnavutköy",
  "Ataşehir",
  "Avcılar",
  "Bağcılar",
  "Bahçelievler",
  "Bakırköy",
  "Başakşehir",
  "Bayrampaşa",
  "Beşiktaş",
  "Beykoz",
  "Beylikdüzü",
  "Beyoğlu",
  "Büyükçekmece",
  "Çatalca",
  "Çekmeköy",
  "Esenler",
  "Esenyurt",
  "Eyüpsultan",
  "Fatih",
  "Gaziosmanpaşa",
  "Güngören",
  "Kadıköy",
  "Kağıthane",
  "Kartal",
  "Küçükçekmece",
  "Maltepe",
  "Pendik",
  "Sancaktepe",
  "Sarıyer",
  "Silivri",
  "Sultanbeyli",
  "Sultangazi",
  "Şile",
  "Şişli",
  "Tuzla",
  "Ümraniye",
  "Üsküdar",
  "Zeytinburnu",
];

const ISITMA_TIPLERI = [
  "Doğalgaz (Kombi)",
  "Merkezi",
  "Soba",
  "Klima",
  "Yerden Isıtma",
];

// İlçe verileri - m² fiyatları ve yatırım potansiyeli
const ILCE_VERILERI = {
  Esenyurt: {
    m2Fiyat: 85000,
    potansiyel: "Yüksek",
    aciklama: "Yüksek nüfus artışı, metro projeleri",
    renk: "emerald",
  },
  Arnavutköy: {
    m2Fiyat: 75000,
    potansiyel: "Çok Yüksek",
    aciklama: "Havalimanı yakınlığı, gelişen bölge",
    renk: "blue",
  },
  Silivri: {
    m2Fiyat: 70000,
    potansiyel: "Orta",
    aciklama: "Yazlık bölge, sakin yaşam",
    renk: "purple",
  },
  Sultanbeyli: {
    m2Fiyat: 80000,
    potansiyel: "Yüksek",
    aciklama: "Kentsel dönüşüm projeleri",
    renk: "orange",
  },
  Tuzla: {
    m2Fiyat: 100000,
    potansiyel: "Yüksek",
    aciklama: "Sanayi ve teknoloji yatırımları",
    renk: "cyan",
  },
  Pendik: {
    m2Fiyat: 130000,
    potansiyel: "Çok Yüksek",
    aciklama: "Sabiha Gökçen, marina projeleri",
    renk: "pink",
  },
  Kartal: {
    m2Fiyat: 125000,
    potansiyel: "Yüksek",
    aciklama: "Marmaray bağlantısı, sahil",
    renk: "indigo",
  },
  Ümraniye: {
    m2Fiyat: 140000,
    potansiyel: "Yüksek",
    aciklama: "İş merkezleri, ulaşım ağı",
    renk: "violet",
  },
  Maltepe: {
    m2Fiyat: 150000,
    potansiyel: "Orta",
    aciklama: "Sahil bandı, yerleşik bölge",
    renk: "teal",
  },
  Sancaktepe: {
    m2Fiyat: 110000,
    potansiyel: "Çok Yüksek",
    aciklama: "Metro hatları, yeni projeler",
    renk: "rose",
  },
  Çekmeköy: {
    m2Fiyat: 120000,
    potansiyel: "Yüksek",
    aciklama: "Doğa, metro bağlantısı",
    renk: "amber",
  },
  Başakşehir: {
    m2Fiyat: 145000,
    potansiyel: "Yüksek",
    aciklama: "Şehir hastanesi, Olimpiyat",
    renk: "lime",
  },
  Beylikdüzü: {
    m2Fiyat: 115000,
    potansiyel: "Orta",
    aciklama: "Metrobüs, planlı yapılaşma",
    renk: "sky",
  },
  Büyükçekmece: {
    m2Fiyat: 105000,
    potansiyel: "Orta",
    aciklama: "Sahil, yazlık bölge",
    renk: "fuchsia",
  },
  Küçükçekmece: {
    m2Fiyat: 125000,
    potansiyel: "Yüksek",
    aciklama: "Metro, kentsel dönüşüm",
    renk: "emerald",
  },
  Avcılar: {
    m2Fiyat: 120000,
    potansiyel: "Orta",
    aciklama: "Üniversite, sahil",
    renk: "blue",
  },
  Bağcılar: {
    m2Fiyat: 135000,
    potansiyel: "Orta",
    aciklama: "Merkezi konum, ulaşım",
    renk: "purple",
  },
  Güngören: {
    m2Fiyat: 130000,
    potansiyel: "Orta",
    aciklama: "Metro, merkezi konum",
    renk: "orange",
  },
  Bahçelievler: {
    m2Fiyat: 145000,
    potansiyel: "Orta",
    aciklama: "Yerleşik, metro",
    renk: "cyan",
  },
  Gaziosmanpaşa: {
    m2Fiyat: 125000,
    potansiyel: "Yüksek",
    aciklama: "Kentsel dönüşüm",
    renk: "pink",
  },
  Esenler: {
    m2Fiyat: 115000,
    potansiyel: "Yüksek",
    aciklama: "Metro, dönüşüm",
    renk: "indigo",
  },
  Eyüpsultan: {
    m2Fiyat: 140000,
    potansiyel: "Yüksek",
    aciklama: "Tarihi doku, teleferik",
    renk: "violet",
  },
  Kağıthane: {
    m2Fiyat: 160000,
    potansiyel: "Orta",
    aciklama: "İş merkezleri, metro",
    renk: "teal",
  },
  Sultangazi: {
    m2Fiyat: 110000,
    potansiyel: "Yüksek",
    aciklama: "Gelişen bölge",
    renk: "rose",
  },
  Bayrampaşa: {
    m2Fiyat: 140000,
    potansiyel: "Orta",
    aciklama: "Forum, merkezi",
    renk: "amber",
  },
  Zeytinburnu: {
    m2Fiyat: 155000,
    potansiyel: "Orta",
    aciklama: "Sahil, Marmaray",
    renk: "lime",
  },
  Fatih: {
    m2Fiyat: 165000,
    potansiyel: "Düşük",
    aciklama: "Tarihi yarımada",
    renk: "sky",
  },
  Beyoğlu: {
    m2Fiyat: 180000,
    potansiyel: "Düşük",
    aciklama: "Turistik, tarihi",
    renk: "fuchsia",
  },
  Şişli: {
    m2Fiyat: 200000,
    potansiyel: "Düşük",
    aciklama: "Premium lokasyon",
    renk: "emerald",
  },
  Beşiktaş: {
    m2Fiyat: 300000,
    potansiyel: "Düşük",
    aciklama: "Lüks segment",
    renk: "blue",
  },
  Sarıyer: {
    m2Fiyat: 280000,
    potansiyel: "Düşük",
    aciklama: "Boğaz manzarası",
    renk: "purple",
  },
  Kadıköy: {
    m2Fiyat: 220000,
    potansiyel: "Düşük",
    aciklama: "Premium, kültür merkezi",
    renk: "orange",
  },
  Üsküdar: {
    m2Fiyat: 160000,
    potansiyel: "Orta",
    aciklama: "Tarihi, Marmaray",
    renk: "cyan",
  },
  Ataşehir: {
    m2Fiyat: 170000,
    potansiyel: "Orta",
    aciklama: "Finans merkezi",
    renk: "pink",
  },
  Beykoz: {
    m2Fiyat: 175000,
    potansiyel: "Orta",
    aciklama: "Doğa, Boğaz",
    renk: "indigo",
  },
  Şile: {
    m2Fiyat: 95000,
    potansiyel: "Yüksek",
    aciklama: "Sahil, turizm",
    renk: "violet",
  },
  Çatalca: {
    m2Fiyat: 65000,
    potansiyel: "Yüksek",
    aciklama: "Tarım, doğa",
    renk: "teal",
  },
  Adalar: {
    m2Fiyat: 250000,
    potansiyel: "Düşük",
    aciklama: "Ada yaşamı, kısıtlı arz",
    renk: "rose",
  },
  Bakırköy: {
    m2Fiyat: 180000,
    potansiyel: "Düşük",
    aciklama: "Sahil, yerleşik",
    renk: "amber",
  },
};

function HousePricePredictor() {
  const [activeTab, setActiveTab] = useState("tahmin");
  const [formData, setFormData] = useState({
    ilce: "",
    metrekare: "",
    odaSayisi: "",
    binaYasi: "",
    katSayisi: "",
    bulunduguKat: "",
    isitmaTipi: "",
    siteIcerisinde: false,
  });
  const [tahmin, setTahmin] = useState(null);
  const [loading, setLoading] = useState(false);

  // Bütçe Analizi State
  const [butce, setButce] = useState("");
  const [hedefM2, setHedefM2] = useState("100");
  const [butceAnalizi, setButceAnalizi] = useState(null);

  // Chatbot State
  const [chatMesajlar, setChatMesajlar] = useState([
    {
      rol: "bot",
      mesaj:
        "👋 Merhaba! Ben Konut Asistanın. Size İstanbul konut piyasası hakkında yardımcı olabilirim. İlçeler, fiyatlar, yatırım tavsiyeleri... Ne sormak istersiniz?",
    },
  ]);
  const [chatInput, setChatInput] = useState("");
  const [chatLoading, setChatLoading] = useState(false);

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: type === "checkbox" ? checked : value,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      const response = await fetch("http://localhost:5000/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          ilce: formData.ilce,
          metrekare: parseFloat(formData.metrekare),
          oda_sayisi: parseFloat(formData.odaSayisi),
          bina_yasi: parseFloat(formData.binaYasi),
          kat_sayisi: parseFloat(formData.katSayisi),
          bulundugu_kat: parseFloat(formData.bulunduguKat),
          isitma_tipi: formData.isitmaTipi,
          site_icerisinde: formData.siteIcerisinde,
        }),
      });
      const data = await response.json();
      setTahmin(data.tahmin);
    } catch (error) {
      console.error("Hata:", error);
      setTahmin(hesaplaDemoTahmin());
    } finally {
      setLoading(false);
    }
  };

  const hesaplaDemoTahmin = () => {
    const m2 = parseFloat(formData.metrekare) || 100;
    const yas = parseFloat(formData.binaYasi) || 5;
    const site = formData.siteIcerisinde ? 1.15 : 1;
    const m2Fiyat = ILCE_VERILERI[formData.ilce]?.m2Fiyat || 120000;
    const yasCarpan = Math.max(0.7, 1 - yas * 0.01);
    return Math.round(m2 * m2Fiyat * yasCarpan * site);
  };

  const formatFiyat = (fiyat) => {
    return new Intl.NumberFormat("tr-TR", {
      style: "currency",
      currency: "TRY",
      minimumFractionDigits: 0,
      maximumFractionDigits: 0,
    }).format(fiyat);
  };

  // Bütçe Analizi Fonksiyonu
  const analizButce = () => {
    const butceNum = parseFloat(butce);
    const hedefMetrekare = parseFloat(hedefM2) || 100;

    if (!butceNum || butceNum < 1000000) {
      setButceAnalizi(null);
      return;
    }

    // Bütçe segmentini belirle
    let segment = "ekonomik";
    if (butceNum >= 15000000) segment = "premium";
    else if (butceNum >= 8000000) segment = "lüks";
    else if (butceNum >= 4000000) segment = "orta-üst";
    else if (butceNum >= 2500000) segment = "orta";

    // Her ilçe için skor hesapla
    const skorluIlceler = Object.entries(ILCE_VERILERI)
      .map(([ilce, veri]) => {
        const tahminiM2 = Math.floor(butceNum / veri.m2Fiyat);
        const m2Farki = Math.abs(tahminiM2 - hedefMetrekare);

        // Hedef m²'ye yakınlık skoru (0-100)
        const yakinlikSkoru = Math.max(0, 100 - m2Farki * 2);

        // Potansiyel skoru
        const potansiyelSkor = {
          "Çok Yüksek": 40,
          Yüksek: 30,
          Orta: 20,
          Düşük: 10,
        };

        // Segment uyumu skoru
        let segmentUyumu = 0;
        if (segment === "ekonomik" && veri.m2Fiyat <= 90000) segmentUyumu = 30;
        else if (
          segment === "orta" &&
          veri.m2Fiyat > 90000 &&
          veri.m2Fiyat <= 130000
        )
          segmentUyumu = 30;
        else if (
          segment === "orta-üst" &&
          veri.m2Fiyat > 110000 &&
          veri.m2Fiyat <= 160000
        )
          segmentUyumu = 30;
        else if (
          segment === "lüks" &&
          veri.m2Fiyat > 140000 &&
          veri.m2Fiyat <= 200000
        )
          segmentUyumu = 30;
        else if (segment === "premium" && veri.m2Fiyat > 180000)
          segmentUyumu = 30;
        else segmentUyumu = 10; // Segment dışı ama yine de göster

        // Toplam skor
        const toplamSkor =
          yakinlikSkoru + potansiyelSkor[veri.potansiyel] + segmentUyumu;

        return {
          ilce,
          ...veri,
          tahminiM2,
          m2Farki,
          toplamSkor,
          uygunluk: tahminiM2 >= hedefMetrekare ? "uygun" : "dar",
        };
      })
      .filter((item) => item.tahminiM2 >= 40) // Minimum 40m² alınabilmeli
      .sort((a, b) => b.toplamSkor - a.toplamSkor)
      .slice(0, 3);

    setButceAnalizi(skorluIlceler);
  };

  const getPotansiyelRenk = (potansiyel) => {
    switch (potansiyel) {
      case "Çok Yüksek":
        return "from-emerald-500 to-green-500";
      case "Yüksek":
        return "from-blue-500 to-cyan-500";
      case "Orta":
        return "from-amber-500 to-orange-500";
      case "Düşük":
        return "from-gray-500 to-slate-500";
      default:
        return "from-purple-500 to-pink-500";
    }
  };

  // Chatbot Fonksiyonu
  const chatGonder = async () => {
    if (!chatInput.trim()) return;

    const yeniMesaj = { rol: "user", mesaj: chatInput };
    setChatMesajlar((prev) => [...prev, yeniMesaj]);
    setChatInput("");
    setChatLoading(true);

    try {
      const response = await fetch("http://localhost:5000/chatbot", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ mesaj: chatInput }),
      });
      const data = await response.json();

      setChatMesajlar((prev) => [...prev, { rol: "bot", mesaj: data.yanit }]);
    } catch (error) {
      setChatMesajlar((prev) => [
        ...prev,
        {
          rol: "bot",
          mesaj: "⚠️ Bağlantı hatası. Backend çalışıyor mu kontrol edin.",
        },
      ]);
    } finally {
      setChatLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      chatGonder();
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-900 via-blue-900 to-indigo-900 p-4 md:p-8 relative overflow-hidden">
      {/* Animated Background */}
      <div className="absolute inset-0 overflow-hidden">
        <div className="absolute -top-40 -right-40 w-80 h-80 bg-purple-500 rounded-full mix-blend-multiply filter blur-3xl opacity-30 animate-pulse"></div>
        <div className="absolute -bottom-40 -left-40 w-80 h-80 bg-blue-500 rounded-full mix-blend-multiply filter blur-3xl opacity-30 animate-pulse"></div>
        <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-96 h-96 bg-indigo-500 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-pulse"></div>
      </div>

      <div className="max-w-4xl mx-auto relative z-10">
        {/* Glass Card */}
        <div className="backdrop-blur-xl bg-white/10 border border-white/20 rounded-3xl shadow-2xl p-6 md:p-10">
          {/* Header */}
          <div className="text-center mb-8">
            <div className="inline-flex items-center justify-center w-20 h-20 rounded-2xl bg-gradient-to-br from-purple-500 to-blue-500 mb-4 shadow-lg shadow-purple-500/30">
              <Home className="w-10 h-10 text-white" />
            </div>
            <h1 className="text-3xl md:text-4xl font-bold text-white mb-2">
              İstanbul Konut Fiyat Tahmin Sistemi
            </h1>
            <p className="text-white/60 flex items-center justify-center gap-2">
              <Sparkles className="w-4 h-4" />
              Yapay zeka destekli konut analizi
              <Sparkles className="w-4 h-4" />
            </p>
          </div>

          {/* Tab Buttons - Enhanced Design */}
          <div className="flex gap-3 mb-8 p-2 rounded-2xl bg-white/5 border border-white/10 backdrop-blur-sm">
            {/* Fiyat Tahmini Tab */}
            <button
              onClick={() => setActiveTab("tahmin")}
              className={`group relative flex-1 py-4 px-4 rounded-xl font-medium transition-all duration-500 flex items-center justify-center gap-3 overflow-hidden ${
                activeTab === "tahmin"
                  ? "text-white"
                  : "text-white/50 hover:text-white/80 hover:bg-white/5"
              }`}
            >
              {/* Active Background with Glow */}
              {activeTab === "tahmin" && (
                <>
                  <div className="absolute inset-0 bg-gradient-to-r from-purple-600 via-violet-600 to-blue-600 rounded-xl" />
                  <div className="absolute inset-0 bg-gradient-to-r from-purple-600 via-violet-600 to-blue-600 rounded-xl blur-xl opacity-50" />
                  <div className="absolute inset-0 bg-gradient-to-t from-black/20 to-transparent rounded-xl" />
                </>
              )}
              <Calculator
                size={20}
                className={`relative z-10 transition-transform duration-300 ${activeTab === "tahmin" ? "scale-110" : "group-hover:scale-110"}`}
              />
              <span className="relative z-10 hidden sm:inline font-semibold">
                Fiyat Tahmini
              </span>
              <span className="relative z-10 sm:hidden font-semibold">
                Tahmin
              </span>
              {/* Active Indicator Dot */}
              {activeTab === "tahmin" && (
                <span className="absolute -bottom-0.5 left-1/2 -translate-x-1/2 w-8 h-1 bg-white rounded-full shadow-lg shadow-white/50" />
              )}
            </button>

            {/* Bütçe Analizi Tab */}
            <button
              onClick={() => setActiveTab("butce")}
              className={`group relative flex-1 py-4 px-4 rounded-xl font-medium transition-all duration-500 flex items-center justify-center gap-3 overflow-hidden ${
                activeTab === "butce"
                  ? "text-white"
                  : "text-white/50 hover:text-white/80 hover:bg-white/5"
              }`}
            >
              {/* Active Background with Glow */}
              {activeTab === "butce" && (
                <>
                  <div className="absolute inset-0 bg-gradient-to-r from-emerald-600 via-green-600 to-teal-600 rounded-xl" />
                  <div className="absolute inset-0 bg-gradient-to-r from-emerald-600 via-green-600 to-teal-600 rounded-xl blur-xl opacity-50" />
                  <div className="absolute inset-0 bg-gradient-to-t from-black/20 to-transparent rounded-xl" />
                </>
              )}
              <Wallet
                size={20}
                className={`relative z-10 transition-transform duration-300 ${activeTab === "butce" ? "scale-110" : "group-hover:scale-110"}`}
              />
              <span className="relative z-10 hidden sm:inline font-semibold">
                Bütçe Analizi
              </span>
              <span className="relative z-10 sm:hidden font-semibold">
                Bütçe
              </span>
              {/* Active Indicator Dot */}
              {activeTab === "butce" && (
                <span className="absolute -bottom-0.5 left-1/2 -translate-x-1/2 w-8 h-1 bg-white rounded-full shadow-lg shadow-white/50" />
              )}
            </button>

            {/* Konut Asistan Tab */}
            <button
              onClick={() => setActiveTab("chatbot")}
              className={`group relative flex-1 py-4 px-4 rounded-xl font-medium transition-all duration-500 flex items-center justify-center gap-3 overflow-hidden ${
                activeTab === "chatbot"
                  ? "text-white"
                  : "text-white/50 hover:text-white/80 hover:bg-white/5"
              }`}
            >
              {/* Active Background with Glow */}
              {activeTab === "chatbot" && (
                <>
                  <div className="absolute inset-0 bg-gradient-to-r from-pink-600 via-rose-600 to-red-600 rounded-xl" />
                  <div className="absolute inset-0 bg-gradient-to-r from-pink-600 via-rose-600 to-red-600 rounded-xl blur-xl opacity-50" />
                  <div className="absolute inset-0 bg-gradient-to-t from-black/20 to-transparent rounded-xl" />
                </>
              )}
              <MessageCircle
                size={20}
                className={`relative z-10 transition-transform duration-300 ${activeTab === "chatbot" ? "scale-110 animate-pulse" : "group-hover:scale-110"}`}
              />
              <span className="relative z-10 hidden sm:inline font-semibold">
                Konut Asistan
              </span>
              <span className="relative z-10 sm:hidden font-semibold">
                Asistan
              </span>
              {/* Active Indicator Dot */}
              {activeTab === "chatbot" && (
                <span className="absolute -bottom-0.5 left-1/2 -translate-x-1/2 w-8 h-1 bg-white rounded-full shadow-lg shadow-white/50" />
              )}
            </button>
          </div>

          {/* Tab Content */}
          {activeTab === "tahmin" ? (
            /* Fiyat Tahmini Tab */
            <>
              <form onSubmit={handleSubmit} className="space-y-6">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4 md:gap-6">
                  {/* İlçe */}
                  <div className="group">
                    <label className="flex items-center gap-2 text-white/80 text-sm font-medium mb-2">
                      <MapPin size={16} className="text-purple-400" />
                      İlçe
                    </label>
                    <select
                      name="ilce"
                      value={formData.ilce}
                      onChange={handleChange}
                      required
                      className="w-full px-4 py-3 rounded-xl bg-white/5 border border-white/10 text-white focus:outline-none focus:ring-2 focus:ring-purple-500/50 backdrop-blur-sm transition-all duration-300 hover:bg-white/10"
                    >
                      <option value="" className="bg-gray-900">
                        İlçe Seçin
                      </option>
                      {ILCELER.map((ilce) => (
                        <option key={ilce} value={ilce} className="bg-gray-900">
                          {ilce}
                        </option>
                      ))}
                    </select>
                  </div>

                  {/* Metrekare */}
                  <div className="group">
                    <label className="flex items-center gap-2 text-white/80 text-sm font-medium mb-2">
                      <Ruler size={16} className="text-blue-400" />
                      Brüt Metrekare
                    </label>
                    <input
                      type="number"
                      name="metrekare"
                      value={formData.metrekare}
                      onChange={handleChange}
                      placeholder="Örn: 120"
                      min="30"
                      max="500"
                      required
                      className="w-full px-4 py-3 rounded-xl bg-white/5 border border-white/10 text-white placeholder-white/30 focus:outline-none focus:ring-2 focus:ring-blue-500/50 backdrop-blur-sm transition-all duration-300 hover:bg-white/10"
                    />
                  </div>

                  {/* Oda Sayısı */}
                  <div className="group">
                    <label className="flex items-center gap-2 text-white/80 text-sm font-medium mb-2">
                      <DoorOpen size={16} className="text-green-400" />
                      Oda Sayısı
                    </label>
                    <select
                      name="odaSayisi"
                      value={formData.odaSayisi}
                      onChange={handleChange}
                      required
                      className="w-full px-4 py-3 rounded-xl bg-white/5 border border-white/10 text-white focus:outline-none focus:ring-2 focus:ring-green-500/50 backdrop-blur-sm transition-all duration-300 hover:bg-white/10"
                    >
                      <option value="" className="bg-gray-900">
                        Seçin
                      </option>
                      {[
                        "1+0 (Stüdyo)",
                        "1+1",
                        "2+1",
                        "3+1",
                        "4+1",
                        "5+1",
                        "6+",
                      ].map((oda, i) => (
                        <option key={i} value={i + 1} className="bg-gray-900">
                          {oda}
                        </option>
                      ))}
                    </select>
                  </div>

                  {/* Bina Yaşı */}
                  <div className="group">
                    <label className="flex items-center gap-2 text-white/80 text-sm font-medium mb-2">
                      <Building2 size={16} className="text-yellow-400" />
                      Bina Yaşı
                    </label>
                    <input
                      type="number"
                      name="binaYasi"
                      value={formData.binaYasi}
                      onChange={handleChange}
                      placeholder="Örn: 5"
                      min="0"
                      max="50"
                      required
                      className="w-full px-4 py-3 rounded-xl bg-white/5 border border-white/10 text-white placeholder-white/30 focus:outline-none focus:ring-2 focus:ring-yellow-500/50 backdrop-blur-sm transition-all duration-300 hover:bg-white/10"
                    />
                  </div>

                  {/* Kat Sayısı */}
                  <div className="group">
                    <label className="flex items-center gap-2 text-white/80 text-sm font-medium mb-2">
                      <Building2 size={16} className="text-orange-400" />
                      Binanın Kat Sayısı
                    </label>
                    <input
                      type="number"
                      name="katSayisi"
                      value={formData.katSayisi}
                      onChange={handleChange}
                      placeholder="Örn: 10"
                      min="1"
                      max="50"
                      required
                      className="w-full px-4 py-3 rounded-xl bg-white/5 border border-white/10 text-white placeholder-white/30 focus:outline-none focus:ring-2 focus:ring-orange-500/50 backdrop-blur-sm transition-all duration-300 hover:bg-white/10"
                    />
                  </div>

                  {/* Bulunduğu Kat */}
                  <div className="group">
                    <label className="flex items-center gap-2 text-white/80 text-sm font-medium mb-2">
                      <Building2 size={16} className="text-pink-400" />
                      Bulunduğu Kat
                    </label>
                    <input
                      type="number"
                      name="bulunduguKat"
                      value={formData.bulunduguKat}
                      onChange={handleChange}
                      placeholder="Örn: 3"
                      min="0"
                      max="50"
                      required
                      className="w-full px-4 py-3 rounded-xl bg-white/5 border border-white/10 text-white placeholder-white/30 focus:outline-none focus:ring-2 focus:ring-pink-500/50 backdrop-blur-sm transition-all duration-300 hover:bg-white/10"
                    />
                  </div>

                  {/* Isıtma Tipi */}
                  <div className="group">
                    <label className="flex items-center gap-2 text-white/80 text-sm font-medium mb-2">
                      <Flame size={16} className="text-red-400" />
                      Isıtma Tipi
                    </label>
                    <select
                      name="isitmaTipi"
                      value={formData.isitmaTipi}
                      onChange={handleChange}
                      required
                      className="w-full px-4 py-3 rounded-xl bg-white/5 border border-white/10 text-white focus:outline-none focus:ring-2 focus:ring-red-500/50 backdrop-blur-sm transition-all duration-300 hover:bg-white/10"
                    >
                      <option value="" className="bg-gray-900">
                        Seçin
                      </option>
                      {ISITMA_TIPLERI.map((tip) => (
                        <option key={tip} value={tip} className="bg-gray-900">
                          {tip}
                        </option>
                      ))}
                    </select>
                  </div>

                  {/* Site İçerisinde */}
                  <div className="group flex items-end">
                    <label className="flex items-center gap-3 cursor-pointer w-full px-4 py-3 rounded-xl bg-white/5 border border-white/10 hover:bg-white/10 transition-all duration-300">
                      <input
                        type="checkbox"
                        name="siteIcerisinde"
                        checked={formData.siteIcerisinde}
                        onChange={handleChange}
                        className="w-5 h-5 rounded border-white/30 bg-white/10 text-purple-500 focus:ring-purple-500/50"
                      />
                      <CheckCircle
                        size={16}
                        className={
                          formData.siteIcerisinde
                            ? "text-emerald-400"
                            : "text-white/40"
                        }
                      />
                      <span className="text-white/80 text-sm font-medium">
                        Site İçerisinde
                      </span>
                    </label>
                  </div>
                </div>

                <button
                  type="submit"
                  disabled={loading}
                  className="w-full py-4 px-6 rounded-xl bg-gradient-to-r from-purple-600 to-blue-600 text-white font-semibold text-lg flex items-center justify-center gap-3 hover:from-purple-500 hover:to-blue-500 disabled:opacity-50 transition-all duration-300 shadow-lg shadow-purple-500/25 hover:shadow-purple-500/40 hover:scale-[1.02] active:scale-[0.98]"
                >
                  <Calculator size={22} />
                  {loading ? "Hesaplanıyor..." : "Fiyat Tahmin Et"}
                </button>
              </form>

              {tahmin && (
                <div className="mt-8 p-6 rounded-2xl bg-gradient-to-r from-emerald-500/20 to-teal-500/20 border border-emerald-500/30 backdrop-blur-sm">
                  <h2 className="text-white/70 text-center text-sm font-medium mb-2">
                    Tahmini Değer
                  </h2>
                  <div className="text-center">
                    <span className="text-4xl md:text-5xl font-bold bg-gradient-to-r from-emerald-400 to-teal-400 bg-clip-text text-transparent">
                      {formatFiyat(tahmin)}
                    </span>
                  </div>
                  <p className="text-white/50 text-center text-xs mt-4">
                    * Bu tahmin yapay zeka modeli tarafından hesaplanmıştır.
                  </p>
                </div>
              )}
            </>
          ) : activeTab === "butce" ? (
            /* Bütçe Analizi Tab */
            <div className="space-y-6">
              <div className="text-center mb-6">
                <p className="text-white/60 text-sm">
                  Bütçenizi ve hedef metrekarenizi girin, size en uygun ilçeleri
                  önerelim
                </p>
              </div>

              {/* Bütçe ve Hedef M² Input */}
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div className="md:col-span-1">
                  <label className="flex items-center gap-2 text-white/80 text-sm font-medium mb-2">
                    <Wallet size={16} className="text-emerald-400" />
                    Bütçeniz (TL)
                  </label>
                  <input
                    type="number"
                    value={butce}
                    onChange={(e) => setButce(e.target.value)}
                    placeholder="Örn: 5000000"
                    min="1000000"
                    className="w-full px-4 py-3 rounded-xl bg-white/5 border border-white/10 text-white placeholder-white/30 focus:outline-none focus:ring-2 focus:ring-emerald-500/50 backdrop-blur-sm transition-all duration-300 hover:bg-white/10"
                  />
                </div>
                <div className="md:col-span-1">
                  <label className="flex items-center gap-2 text-white/80 text-sm font-medium mb-2">
                    <Ruler size={16} className="text-blue-400" />
                    Hedef Metrekare
                  </label>
                  <select
                    value={hedefM2}
                    onChange={(e) => setHedefM2(e.target.value)}
                    className="w-full px-4 py-3 rounded-xl bg-white/5 border border-white/10 text-white focus:outline-none focus:ring-2 focus:ring-blue-500/50 backdrop-blur-sm transition-all duration-300 hover:bg-white/10"
                  >
                    <option value="60" className="bg-gray-900">
                      60 m² (1+1)
                    </option>
                    <option value="80" className="bg-gray-900">
                      80 m² (2+1)
                    </option>
                    <option value="100" className="bg-gray-900">
                      100 m² (2+1 / 3+1)
                    </option>
                    <option value="120" className="bg-gray-900">
                      120 m² (3+1)
                    </option>
                    <option value="150" className="bg-gray-900">
                      150 m² (4+1)
                    </option>
                    <option value="180" className="bg-gray-900">
                      180 m² (4+1 / 5+1)
                    </option>
                    <option value="200" className="bg-gray-900">
                      200+ m² (Villa/Dublex)
                    </option>
                  </select>
                </div>
                <button
                  onClick={analizButce}
                  className="md:self-end py-3 px-8 rounded-xl bg-gradient-to-r from-emerald-600 to-teal-600 text-white font-semibold flex items-center justify-center gap-2 hover:from-emerald-500 hover:to-teal-500 transition-all duration-300 shadow-lg shadow-emerald-500/25 hover:shadow-emerald-500/40"
                >
                  <TrendingUp size={20} />
                  Analiz Et
                </button>
              </div>

              {/* Bütçe Analiz Sonuçları */}
              {butceAnalizi && butceAnalizi.length > 0 && (
                <div className="space-y-4 mt-8">
                  <h3 className="text-white/80 text-lg font-medium flex items-center gap-2">
                    <Star className="text-amber-400" size={20} />
                    Size Önerilen İlçeler
                  </h3>

                  <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                    {butceAnalizi.map((item, index) => (
                      <div
                        key={item.ilce}
                        className={`relative overflow-hidden rounded-2xl backdrop-blur-xl bg-white/5 border border-white/10 p-5 hover:bg-white/10 transition-all duration-300 hover:scale-[1.02] ${
                          index === 0
                            ? "md:scale-105 ring-2 ring-emerald-500/50"
                            : ""
                        }`}
                      >
                        {/* Rank Badge */}
                        <div
                          className={`absolute top-3 right-3 w-8 h-8 rounded-full flex items-center justify-center text-sm font-bold ${
                            index === 0
                              ? "bg-gradient-to-br from-amber-400 to-orange-500 text-white"
                              : index === 1
                                ? "bg-gradient-to-br from-gray-300 to-gray-400 text-gray-800"
                                : "bg-gradient-to-br from-amber-600 to-amber-700 text-white"
                          }`}
                        >
                          {index + 1}
                        </div>

                        {/* İlçe Adı */}
                        <h4 className="text-xl font-bold text-white mb-2">
                          {item.ilce}
                        </h4>

                        {/* Potansiyel Badge */}
                        <div
                          className={`inline-flex items-center gap-1 px-3 py-1 rounded-full text-xs font-medium bg-gradient-to-r ${getPotansiyelRenk(item.potansiyel)} text-white mb-3`}
                        >
                          <TrendingUp size={12} />
                          {item.potansiyel} Potansiyel
                        </div>

                        {/* Detaylar */}
                        <div className="space-y-3">
                          <div className="flex justify-between items-center">
                            <span className="text-white/50 text-sm">
                              Ort. m² Fiyatı
                            </span>
                            <span className="text-white font-semibold">
                              {formatFiyat(item.m2Fiyat)}
                            </span>
                          </div>
                          <div className="flex justify-between items-center">
                            <span className="text-white/50 text-sm">
                              Alınabilir m²
                            </span>
                            <span
                              className={`font-bold text-lg ${item.tahminiM2 >= parseFloat(hedefM2) ? "text-emerald-400" : "text-amber-400"}`}
                            >
                              {item.tahminiM2} m²
                            </span>
                          </div>
                          <div className="flex justify-between items-center">
                            <span className="text-white/50 text-sm">
                              Hedef Uyumu
                            </span>
                            <span
                              className={`text-sm font-medium ${item.tahminiM2 >= parseFloat(hedefM2) ? "text-emerald-400" : "text-amber-400"}`}
                            >
                              {item.tahminiM2 >= parseFloat(hedefM2)
                                ? `✓ Hedefe uygun (+${item.tahminiM2 - parseFloat(hedefM2)} m²)`
                                : `↓ ${parseFloat(hedefM2) - item.tahminiM2} m² eksik`}
                            </span>
                          </div>
                        </div>

                        {/* Açıklama */}
                        <div className="mt-4 pt-4 border-t border-white/10">
                          <p className="text-white/60 text-xs flex items-start gap-2">
                            <ArrowRight
                              size={12}
                              className="mt-0.5 text-blue-400 flex-shrink-0"
                            />
                            {item.aciklama}
                          </p>
                        </div>
                      </div>
                    ))}
                  </div>

                  {/* Bütçe Özeti */}
                  <div className="mt-6 p-4 rounded-xl bg-white/5 border border-white/10">
                    <p className="text-white/60 text-center text-sm">
                      <span className="text-white font-semibold">
                        {formatFiyat(parseFloat(butce))}
                      </span>{" "}
                      bütçe ile
                      <span className="text-emerald-400 font-semibold">
                        {" "}
                        {hedefM2} m²
                      </span>{" "}
                      hedefi için
                      <span className="text-blue-400 font-semibold">
                        {" "}
                        {butceAnalizi[0]?.ilce}
                      </span>{" "}
                      en uygun seçenek
                    </p>
                  </div>
                </div>
              )}

              {butce && parseFloat(butce) < 1000000 && (
                <div className="p-4 rounded-xl bg-red-500/10 border border-red-500/30 text-center">
                  <p className="text-red-400 text-sm">
                    Minimum 1.000.000 TL bütçe girmeniz gerekmektedir.
                  </p>
                </div>
              )}
            </div>
          ) : activeTab === "chatbot" ? (
            /* Chatbot Tab */
            <div className="space-y-4">
              {/* Chat Messages */}
              <div className="h-96 overflow-y-auto rounded-2xl bg-white/5 border border-white/10 p-4 space-y-4">
                {chatMesajlar.map((msg, index) => (
                  <div
                    key={index}
                    className={`flex ${msg.rol === "user" ? "justify-end" : "justify-start"}`}
                  >
                    <div
                      className={`max-w-[85%] p-4 rounded-2xl ${
                        msg.rol === "user"
                          ? "bg-gradient-to-r from-purple-600 to-blue-600 text-white rounded-br-md"
                          : "bg-white/10 text-white/90 rounded-bl-md border border-white/10"
                      }`}
                    >
                      <div className="text-sm whitespace-pre-wrap leading-relaxed">
                        {msg.mesaj.split("\n").map((line, i) => (
                          <p
                            key={i}
                            className={
                              line.startsWith("**") ? "font-bold mt-2" : ""
                            }
                          >
                            {line.replace(/\*\*/g, "")}
                          </p>
                        ))}
                      </div>
                    </div>
                  </div>
                ))}
                {chatLoading && (
                  <div className="flex justify-start">
                    <div className="bg-white/10 text-white/90 p-4 rounded-2xl rounded-bl-md border border-white/10">
                      <div className="flex gap-1">
                        <span className="w-2 h-2 bg-white/50 rounded-full animate-bounce"></span>
                        <span
                          className="w-2 h-2 bg-white/50 rounded-full animate-bounce"
                          style={{ animationDelay: "0.1s" }}
                        ></span>
                        <span
                          className="w-2 h-2 bg-white/50 rounded-full animate-bounce"
                          style={{ animationDelay: "0.2s" }}
                        ></span>
                      </div>
                    </div>
                  </div>
                )}
              </div>

              {/* Quick Questions */}
              <div className="flex flex-wrap gap-2">
                {[
                  "Kadıköy hakkında",
                  "Yatırım tavsiyesi",
                  "Kredi bilgileri",
                  "Site mi apartman mı?",
                ].map((soru) => (
                  <button
                    key={soru}
                    onClick={() => {
                      setChatInput(soru);
                      setTimeout(() => chatGonder(), 100);
                    }}
                    className="px-3 py-1.5 rounded-full text-xs bg-white/5 border border-white/10 text-white/60 hover:text-white hover:bg-white/10 transition-all"
                  >
                    {soru}
                  </button>
                ))}
              </div>

              {/* Chat Input */}
              <div className="flex gap-3">
                <input
                  type="text"
                  value={chatInput}
                  onChange={(e) => setChatInput(e.target.value)}
                  onKeyPress={handleKeyPress}
                  placeholder="Bir soru sorun... (örn: Beşiktaş'ta fiyatlar nasıl?)"
                  className="flex-1 px-4 py-3 rounded-xl bg-white/5 border border-white/10 text-white placeholder-white/30 focus:outline-none focus:ring-2 focus:ring-pink-500/50 backdrop-blur-sm transition-all duration-300 hover:bg-white/10"
                />
                <button
                  onClick={chatGonder}
                  disabled={chatLoading || !chatInput.trim()}
                  className="px-6 py-3 rounded-xl bg-gradient-to-r from-pink-600 to-rose-600 text-white font-semibold flex items-center justify-center gap-2 hover:from-pink-500 hover:to-rose-500 disabled:opacity-50 transition-all duration-300 shadow-lg shadow-pink-500/25"
                >
                  <Send size={20} />
                </button>
              </div>
            </div>
          ) : null}

          {/* Model Info */}
          <div className="mt-8 p-6 rounded-2xl bg-white/5 border border-white/10 backdrop-blur-sm">
            <h3 className="text-white/70 text-center text-sm font-medium mb-4">
              Model Bilgisi
            </h3>
            <div className="grid grid-cols-3 gap-4">
              <div className="text-center">
                <div className="text-xs text-white/50 mb-1">Algoritma</div>
                <div className="text-sm text-white font-medium">
                  Stacked Ensemble (RF + GB)
                </div>
              </div>
              <div className="text-center border-x border-white/10">
                <div className="text-xs text-white/50 mb-1">Doğruluk (R²)</div>
                <div className="text-sm text-emerald-400 font-bold">%89.97</div>
              </div>
              <div className="text-center">
                <div className="text-xs text-white/50 mb-1">Eğitim Verisi</div>
                <div className="text-sm text-white font-medium">
                  4,000+ kayıt
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Footer */}
        <p className="text-center text-white/30 text-sm mt-6">
          © 2026 Konut Fiyat Tahmin Sistemi - Yapay Zeka ile Güçlendirilmiştir
        </p>
      </div>
    </div>
  );
}

export default HousePricePredictor;
