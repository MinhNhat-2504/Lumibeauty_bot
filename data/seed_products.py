"""
Script tạo dữ liệu mẫu sản phẩm vào Azure Cosmos DB.
Chạy 1 lần: python data/seed_products.py
"""
import sys, os, uuid
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database.cosmos import get_container

PRODUCTS = [
    {"id": str(uuid.uuid4()), "name": "Sữa rửa mặt kiểm soát dầu CeraVe",       "price": 280000,  "skintype": ["da dầu","da hỗn hợp"],              "description": "Làm sạch sâu, kiểm soát dầu nhờn, không gây khô da.", "image": "srmCerave.jpg"},
    {"id": str(uuid.uuid4()), "name": "Toner cân bằng dầu Paula's Choice",        "price": 650000,  "skintype": ["da dầu"],                            "description": "Thu nhỏ lỗ chân lông, kiểm soát bóng dầu cả ngày.", "image": "tonerPaulachoise.jpg"},
    {"id": str(uuid.uuid4()), "name": "Kem dưỡng ẩm không dầu Neutrogena",        "price": 320000,  "skintype": ["da dầu","da hỗn hợp"],              "description": "Dưỡng ẩm nhẹ nhàng, không tắc nghẽn lỗ chân lông.", "image": "kemduongNeutrogena.jpg"},
    {"id": str(uuid.uuid4()), "name": "Serum Niacinamide 10% The Ordinary",       "price": 350000,  "skintype": ["da dầu","da hỗn hợp"],              "description": "Thu nhỏ lỗ chân lông, giảm thâm mụn, kiểm soát dầu.", "image": "serum_10%nia_ordinary.jpg"},
    {"id": str(uuid.uuid4()), "name": "Kem dưỡng ẩm sâu Cetaphil",               "price": 220000,  "skintype": ["da khô","da nhạy cảm"],             "description": "Dưỡng ẩm chuyên sâu 24h, phục hồi hàng rào bảo vệ da.", "image": "kemduongCetaphil.jpg"},
    {"id": str(uuid.uuid4()), "name": "Serum Hyaluronic Acid Vichy",              "price": 580000,  "skintype": ["da khô","da hỗn hợp"],              "description": "Cấp ẩm tức thì, căng mướt làn da suốt 24 giờ.", "image": "serum_HA_Vichy.jpg"},
    {"id": str(uuid.uuid4()), "name": "Sữa rửa mặt dịu nhẹ Bioderma",            "price": 190000,  "skintype": ["da khô","da nhạy cảm"],             "description": "Làm sạch nhẹ nhàng, không gây khô rát.", "image": "srmBioderma.jpg"},
    {"id": str(uuid.uuid4()), "name": "Dầu dưỡng mặt Kiehl's Midnight Recovery",  "price": 1200000, "skintype": ["da khô"],                            "description": "Phục hồi và tái tạo da qua đêm, chống oxy hóa mạnh.", "image": "dauduongMidnightRevery.jpg"},
    {"id": str(uuid.uuid4()), "name": "Kem dưỡng cân bằng ẩm La Roche-Posay",    "price": 450000,  "skintype": ["da hỗn hợp"],                        "description": "Cân bằng độ ẩm cho từng vùng da, không nhờn rít.", "image": "kemduongLaRoche_Posay.jpg"},
    {"id": str(uuid.uuid4()), "name": "Toner hoa hồng Klairs",                    "price": 380000,  "skintype": ["da hỗn hợp","da nhạy cảm"],         "description": "Cân bằng pH, dưỡng ẩm nhẹ, kết cấu trong suốt.", "image": "tonerKlairs.jpg"},
    {"id": str(uuid.uuid4()), "name": "Serum Vitamin C Skinceuticals",             "price": 2800000, "skintype": ["da hỗn hợp","da dầu"],              "description": "Làm sáng da, chống oxy hóa, giảm nám và đốm thâm.", "image": "serumC_Skinceuticals.jpg"},
    {"id": str(uuid.uuid4()), "name": "Kem dưỡng phục hồi Avène Cicalfate",       "price": 390000,  "skintype": ["da nhạy cảm"],                       "description": "Phục hồi da tổn thương, chống kích ứng, làm dịu da đỏ.", "image": "kemduongAvencecicalfate.jpg"},
    {"id": str(uuid.uuid4()), "name": "Kem chống nắng SPF50+ Anessa",             "price": 490000,  "skintype": ["da nhạy cảm","da hỗn hợp","da khô","da dầu"], "description": "Chống nắng UVA/UVB, nhẹ nhàng cho mọi loại da.", "image": "kcnAnessa.jpg"},
    {"id": str(uuid.uuid4()), "name": "Xịt khoáng Evian",                         "price": 150000,  "skintype": ["da nhạy cảm","da khô"],             "description": "Làm mát, xoa dịu da, bổ sung khoáng chất.", "image": "xitkhoang_Evian.jpg"},
    {"id": str(uuid.uuid4()), "name": "Sữa rửa mặt Gentle Skin Cleanser Eucerin", "price": 260000,  "skintype": ["da nhạy cảm","da khô"],             "description": "Dành cho da nhạy cảm, không xà phòng, pH trung tính.", "image": "srm_Eucerin.jpg"},
    {"id": str(uuid.uuid4()), "name": "Sữa rửa mặt Simple",                       "price": 130000,  "skintype": ["da nhạy cảm"],                      "description": "Dành cho da nhạy cảm, không xà phòng, pH trung tính.", "image": "srmSimple.jpg"},
    {"id": str(uuid.uuid4()), "name": "Sữa rửa mặt Cetaphil",                     "price": 200000,  "skintype": ["da nhạy cảm"],                      "description": "Dành cho da nhạy cảm, không xà phòng, pH trung tính.", "image": "srmCentaphil.jpg"},
    {"id": str(uuid.uuid4()), "name": "Serum vitamin C Klairs",                   "price": 380000,  "skintype": ["da nhạy cảm"],                      "description": "Dành cho da nhạy cảm, mới bắt đầu tập dùng vitamin C.", "image": "serum_CKlaris.jpg"},
    {"id": str(uuid.uuid4()), "name": "Nước tẩy trang Bioderma Sensibio H2O",     "price": 450000,  "skintype": ["da nhạy cảm", "da khô"],            "description": "Làm sạch lớp trang điểm và bụi bẩn dịu nhẹ, không cần rửa lại với nước.", "image": "taytrang_Bioderma.jpg"},
    {"id": str(uuid.uuid4()), "name": "Tẩy tế bào chết Paula's Choice 2% BHA",    "price": 890000,  "skintype": ["da dầu", "da hỗn hợp"],             "description": "Loại bỏ tế bào chết, làm sạch sâu lỗ chân lông và hỗ trợ giảm mụn.", "image": "taytbc_Paulachoice.jpg"},
    {"id": str(uuid.uuid4()), "name": "Mặt nạ đất sét Kiehl's Rare Earth",        "price": 850000,  "skintype": ["da dầu", "da hỗn hợp"],             "description": "Hút sạch bã nhờn, se khít lỗ chân lông, làm sạch sâu cho da.", "image": "matna_Kiehl'sRare Earth.jpg"},
    {"id": str(uuid.uuid4()), "name": "Kem chống nắng La Roche-Posay Anthelios",  "price": 475000,  "skintype": ["da dầu", "da hỗn hợp"],             "description": "Kiểm soát bóng nhờn, bảo vệ da tối ưu trước tia UVA/UVB.", "image": "kcn_LarochePosay.jpg"},
    {"id": str(uuid.uuid4()), "name": "Kem dưỡng mắt Estee Lauder ANR",           "price": 1850000, "skintype": ["da khô", "da hỗn hợp", "da dầu", "da nhạy cảm"], "description": "Giảm quầng thâm, ngăn ngừa lão hóa và nếp nhăn vùng mắt.", "image": "duongmat_EsteeLauderANR.jpg"},
    {"id": str(uuid.uuid4()), "name": "Nước tẩy trang L'Oreal Micellar Water",    "price": 170000,  "skintype": ["da dầu", "da hỗn hợp"],             "description": "Công nghệ Micellar làm sạch sâu lớp trang điểm, hạt micelle hút dầu thừa.", "image": "taytrang_LOreal.jpg"},
    {"id": str(uuid.uuid4()), "name": "Nước tẩy trang Garnier Micellar",          "price": 160000,  "skintype": ["da nhạy cảm"],                      "description": "Làm sạch dịu nhẹ không chứa cồn, không gây kích ứng da.", "image": "taytrang_Garnier.jpg"},
    {"id": str(uuid.uuid4()), "name": "Sữa rửa mặt Cosrx Low pH Good Morning",    "price": 220000,  "skintype": ["da dầu", "da nhạy cảm"],            "description": "Độ pH chuẩn 5.5, làm sạch nhẹ nhàng không làm khô căng da.", "image": "srm_Goodmorning.jpg"},
    {"id": str(uuid.uuid4()), "name": "Sữa rửa mặt Senka Perfect Whip",           "price": 120000,  "skintype": ["da thường", "da hỗn hợp"],          "description": "Tạo bọt tơ tằm siêu mịn, rửa sạch bụi bẩn và bã nhờn.", "image": "srmSenka.jpg"},
    {"id": str(uuid.uuid4()), "name": "Sữa rửa mặt Hada Labo Advanced Nourish",   "price": 150000,  "skintype": ["da khô"],                           "description": "Chứa HA dưỡng ẩm sâu, rửa xong da vẫn mềm mại.", "image": "srm_hadalabo.jpg"},
    {"id": str(uuid.uuid4()), "name": "Toner làm dịu da Anua Heartleaf 77%",      "price": 450000,  "skintype": ["da nhạy cảm", "da dầu"],            "description": "Chiết xuất diếp cá làm dịu da mụn, giảm sưng đỏ viêm.", "image": "toner_77%.jpg"},
    {"id": str(uuid.uuid4()), "name": "Toner cấp ẩm Hada Labo Gokujyun",          "price": 280000,  "skintype": ["da khô", "da hỗn hợp"],             "description": "Cấp nước tức thì cho da khô ráp, giúp da ngậm nước căng bóng.", "image": "toner_hadalabo.jpg"},
    {"id": str(uuid.uuid4()), "name": "Nước tẩy trang L'Oreal Revitalift",        "price": 200000,  "skintype": ["da khô", "da thường"],              "description": "Làm sạch bã nhờn, dưỡng ẩm và chống lão hóa da."},
    {"id": str(uuid.uuid4()), "name": "Nước tẩy trang Senka All Clear Water",     "price": 140000,  "skintype": ["da dầu", "da hỗn hợp"],             "description": "Tẩy sạch cặn trang điểm, giảm mụn cám, mụn đầu đen."},
    {"id": str(uuid.uuid4()), "name": "Kem chống nắng Skin Aqua Tone Up UV",      "price": 180000,  "skintype": ["da hỗn hợp", "da thường"],          "description": "Nâng tone da tự nhiên, chống nắng bảo vệ toàn diện."},
    {"id": str(uuid.uuid4()), "name": "Kem chống nắng Bioré UV Aqua Rich",        "price": 150000,  "skintype": ["da dầu", "da thường"],              "description": "Mỏng nhẹ màng nước, không nhờn rít, thấm cực nhanh."},
    {"id": str(uuid.uuid4()), "name": "Kem chống nắng Cell Fusion C",             "price": 400000,  "skintype": ["da nhạy cảm", "da mụn"],            "description": "Chống nắng phục hồi chuyên biệt cho da đang điều trị."},
    {"id": str(uuid.uuid4()), "name": "Kem chống nắng Innisfree Intensive",       "price": 280000,  "skintype": ["da dầu", "da hỗn hợp"],             "description": "Chống nước siêu tốt, kiềm dầu nhẹ nhàng cho mùa hè."},
    {"id": str(uuid.uuid4()), "name": "Sữa rửa mặt Hada Labo Perfect White",      "price": 145000,  "skintype": ["da thường", "da sạm"],              "description": "Tạo bọt mịn, làm sạch sâu và hỗ trợ làm sáng đều màu da."},
    {"id": str(uuid.uuid4()), "name": "Sữa rửa mặt Innisfree Green Tea",          "price": 200000,  "skintype": ["da dầu", "da hỗn hợp"],             "description": "Chiết xuất trà xanh kháng viêm, làm sạch sâu lỗ chân lông."},
    {"id": str(uuid.uuid4()), "name": "Sữa rửa mặt La Roche-Posay Effaclar",      "price": 380000,  "skintype": ["da dầu", "da mụn"],                 "description": "Gel rửa mặt y khoa giúp loại bỏ dầu thừa, ngăn vi khuẩn mụn."},
    {"id": str(uuid.uuid4()), "name": "Sữa rửa mặt Muji Mild Scrub",              "price": 120000,  "skintype": ["da khô", "da nhạy cảm"],            "description": "Làm sạch da siêu dịu nhẹ từ thiên nhiên, có hạt massage."},
    {"id": str(uuid.uuid4()), "name": "Nước hoa hồng Thayers Rose Petal",         "price": 250000,  "skintype": ["da thường", "da nhạy cảm"],         "description": "Se khít lỗ chân lông, không cồn, làm dịu da cực tốt."},
    {"id": str(uuid.uuid4()), "name": "Nước hoa hồng Mamonde Rose Water",         "price": 270000,  "skintype": ["da khô", "da thường"],              "description": "Chiết xuất 90% nước hoa hồng cấp ẩm sâu cho da."},
    {"id": str(uuid.uuid4()), "name": "Nước hoa hồng Muji Light Toning Water",    "price": 200000,  "skintype": ["da nhạy cảm", "da khô"],            "description": "Cân bằng độ ẩm cơ bản cho da cực kỳ dễ kích ứng."},
    {"id": str(uuid.uuid4()), "name": "Nước hoa hồng L'Oreal Revitalift Crystal", "price": 240000,  "skintype": ["da thường", "da xỉn màu"],          "description": "Tẩy tế bào chết dịu nhẹ, giúp da pha lê sáng mịn."},
    {"id": str(uuid.uuid4()), "name": "Tinh chất Kiehl's Clearly Corrective",     "price": 1600000, "skintype": ["da thâm nám", "da thường"],         "description": "Đặc trị mờ thâm nám, giúp da sáng khỏe đồng đều."},
    {"id": str(uuid.uuid4()), "name": "Tinh chất Estee Lauder Advanced Night",    "price": 2200000, "skintype": ["da lão hóa", "da khô"],             "description": "Tái tạo da ban đêm vĩ đại, chống lão hóa chuyên sâu."},
    {"id": str(uuid.uuid4()), "name": "Tinh chất Balance Active Formula Vitamin C","price": 150000,  "skintype": ["da thâm mụn", "da thường"],         "description": "Làm sáng da, cải thiện sắc tố da, mờ thâm siêu đỉnh."},
    {"id": str(uuid.uuid4()), "name": "Tinh chất L'Oreal Revitalift HA",          "price": 320000,  "skintype": ["da khô", "da thiếu nước"],          "description": "Siêu tinh chất cấp ẩm 1.5% Hyaluronic Acid giúp da căng mịn."},
    {"id": str(uuid.uuid4()), "name": "Kem dưỡng ẩm Clinique Moisture Surge",     "price": 980000,  "skintype": ["da khô", "da hỗn hợp thiên khô"],   "description": "Cấp nước 100 giờ, tự động bù nước, da mịn như nhung."},
    {"id": str(uuid.uuid4()), "name": "Kem dưỡng trắng da dạng gel Laneige",      "price": 750000,  "skintype": ["da thường", "da dầu"],              "description": "Chất gel siêu mát mẻ, dưỡng trắng và trị sạm nám."},
    {"id": str(uuid.uuid4()), "name": "Kem dưỡng phục hồi B5 Bioderma Cicabio",   "price": 310000,  "skintype": ["da tổn thương", "da nhạy cảm"],     "description": "Tái tạo mô biểu bì, siêu phục hồi da sau nặn mụn."},
    {"id": str(uuid.uuid4()), "name": "Kem dưỡng mắt AHC Essential Eye Cream",    "price": 280000,  "skintype": ["mọi loại da"],                      "description": "Cấp ẩm, chống nhăn vùng mắt nổi tiếng quốc dân."},
    {"id": str(uuid.uuid4()), "name": "Kem dưỡng chống lão hóa Olay Retinol 24",  "price": 350000,  "skintype": ["da lão hóa", "da thường"],          "description": "Giảm thiểu nếp nhăn, săn chắc da chỉ sau 24 ngày."},
    {"id": str(uuid.uuid4()), "name": "Mặt nạ giấy tràm trà Naruko",              "price": 250000,  "skintype": ["da mụn", "da dầu"],                 "description": "Chiết xuất tinh dầu tràm trà kiểm soát sưng viêm mụn."},
    {"id": str(uuid.uuid4()), "name": "Mặt nạ ngủ Laneige Water Sleeping Mask",   "price": 600000,  "skintype": ["da khô", "da thiếu ngủ"],           "description": "Khóa ẩm ban đêm, phục hồi da mệt mỏi đem lại sự rạng rỡ."},
    {"id": str(uuid.uuid4()), "name": "Mặt nạ lột mụn Innisfree Jeju Volcanic",   "price": 240000,  "skintype": ["da dầu", "da mụn cám"],             "description": "Lột mụn đầu đen, bã nhờn mạnh mẽ từ tro núi lửa."},
    {"id": str(uuid.uuid4()), "name": "Mặt nạ ngủ môi Laneige Lip Sleeping Mask",  "price": 380000,  "skintype": ["môi khô", "môi thâm"],              "description": "Tẩy da chết môi, làm hồng hào và mềm mịn môi."},
    {"id": str(uuid.uuid4()), "name": "Tẩy tế bào chết Cure Natural Aqua Gel",    "price": 450000,  "skintype": ["mọi loại da", "da nhạy cảm"],       "description": "Tẩy da chết dạng gel dịu nhẹ nhất từ Nhật Bản."},
    {"id": str(uuid.uuid4()), "name": "Tẩy tế bào chết Rosette Peeling Gel",      "price": 150000,  "skintype": ["da dầu", "da hỗn hợp"],             "description": "Lấy đi bụi bẩn sừng chết bề mặt, giúp da thông thoáng."},
    {"id": str(uuid.uuid4()), "name": "Tẩy da chết cà phê Đắk Lắk Cocoon",        "price": 115000,  "skintype": ["da cơ thể"],                        "description": "Làm sạch vùng da toàn thân, trị viêm nang lông hiệu quả."},
    {"id": str(uuid.uuid4()), "name": "Nước hoa hồng diếp cá Dokudami",           "price": 180000,  "skintype": ["da mụn", "da nhạy cảm"],            "description": "Lotion siêu to kháng viêm mụn lưng và mụn mặt."},
    {"id": str(uuid.uuid4()), "name": "Serum phục hồi B5 GoodnDoc",               "price": 460000,  "skintype": ["da tổn thương", "da mỏng yếu"],     "description": "Tinh chất vitamin C & B5 cấp cứu làn da nhiễm kem trộn."},
    {"id": str(uuid.uuid4()), "name": "Kem trị mụn Megaduo Gel",                  "price": 140000,  "skintype": ["da mụn trứng cá", "da mụn ẩn"],     "description": "Gel bôi y tế đẩy lùi mụn thâm an toàn bác sĩ da liễu khuyên dùng."},
    {"id": str(uuid.uuid4()), "name": "Xịt khoáng La Roche-Posay Serozinc",       "price": 280000,  "skintype": ["da dầu", "da mụn"],                 "description": "Làm dịu chuyên biệt có kẽm Sulfate giúp giảm bóng nhờn."}
]

# Ảnh minh họa cho /xem (Telegram tải URL). Có thể thay bằng URL thật hoặc đặt file local trong /images.
for idx, prod in enumerate(PRODUCTS, 1):
    prod.setdefault(
        "image_url",
        f"https://picsum.photos/seed/lumibeauty-{idx:03d}/600/600",
    )

def seed():
    container = get_container("products", "/id")
    for p in PRODUCTS:
        container.create_item(body=p)
    print(f"✅ Đã thêm {len(PRODUCTS)} sản phẩm vào Azure Cosmos DB!")

if __name__ == "__main__":
    seed()
