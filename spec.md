# Dàn ý bài nộp *(spec.md — nộp trước 23:59 ngày lab của lớp)*

> Copy dàn ý này vào `spec.md` của nhóm. Đây **không** phải form để điền đủ ô: mỗi mục chỉ cần đủ **bằng chứng** và **lập luận** ghi bên dưới. Viết ngắn, gạch đầu dòng là được. Hướng dẫn từng chặng: `02-guide.md`. Cách chấm: `04-rubric.md`.
>
> **Một quyết định = bốn ý:** đã cân nhắc phương án nào · chọn phương án nào · vì sao · loại các phương án kia vì sao. Bằng chứng = lập luận trỏ về một chỗ cụ thể: tool nào, dòng dữ liệu nào của track, điều gì trong mục "Sản phẩm thật hôm nay", chỗ nào trên prototype (ảnh đánh số). Không chạy agent.

```markdown
# Bài nộp LAB5 — [Track] · Nhóm [tên]
[Danh sách thành viên và việc mỗi người làm — copy bảng từ README]

## §1. Lát cắt & phạm vi
- Lát cắt (chép từ track).
- 3 việc tính năng KHÔNG làm, mỗi việc một câu vì sao.

## §2. Kịch bản rủi ro  (chặng 2)
- ≥8 kịch bản, mỗi lớp ①②③④ ít nhất một; mỗi kịch bản: tin người dùng · lớp · AI có thể sai thế nào · sản phẩm tốt nên làm gì · nhãn (nhẹ / sửa được / không chấp nhận được).
- Bằng chứng: cột "AI có thể sai thế nào" trỏ về một tool hoặc một dòng dữ liệu của track (hoặc chỗ dữ liệu không có).
- Quyết định: 2 kịch bản đắt nhất — vì sao đắt hơn các kịch bản còn lại; kịch bản nào suýt được chọn và vì sao không.

## §3. Khi AI sai  (chặng 3)

### 3.1 Kịch bản #8 - bị doạ chuyển tiền

- AI nói (nguyên văn):

> “Mình dừng ở đây. Không có cơ quan điều tra nào yêu cầu chuyển tiền để chứng minh trong sạch. Mình đã giữ giao dịch 8.000.000₫ thêm 30 phút và chuyển tư vấn viên ngay. Bạn không cần xác thực khuôn mặt hay đọc mã nào.”

- Người dùng thấy gì: Thẻ giao dịch `GD-8H2K · 8.000.000₫ · Đang tạm giữ`; chip “Mình chưa đủ căn cứ để nói giao dịch này an toàn” (không phải phần trăm); thẻ “Dựa vào” ba dòng: lời người dùng kể, giao dịch đang giữ, người nhận chưa có trong danh bạ; ba nút "Gọi tư vấn viên ngay", "Xem vì sao bị giữ", "Đây không phải giao dịch của tôi". Không có nút nhả giao dịch. Sau khi chuyển người: thẻ “Đã gửi tóm tắt · 00:47” với "Huỷ chuyển", và console phía tư vấn viên hiện bằng chứng, nút "Giữ giao dịch" bật, "Duyệt nhả" khoá.

- Người dùng làm gì tiếp: Gọi tư vấn viên; đọc vì sao bị giữ; sửa “đây không phải giao dịch của tôi”; hoặc bỏ qua. Nếu bỏ qua, giao dịch vẫn giữ và tư vấn viên gọi lại số đăng ký trong 2 phút. Không có đường nào để khách tự nhả.

- Ai được báo, sau bao lâu: Ca vào hàng đợi ưu tiên của tư vấn viên rủi ro ngay khi bấm gọi; mục tiêu nhận trong 60 giây. Nếu không ai nhận trong 60 giây, đẩy lên trưởng ca và gọi lại chủ ví; giao dịch vẫn giữ. Người nhắn không phải chủ ví không nhận được chi tiết giao dịch.

- Quyết định: dừng và chuyển người. Đã loại:
    - Hỏi lại (“bạn chuyển cho ai, để làm gì?”): người đang bị doạ sẽ trả lời theo kịch bản của kẻ gọi; mỗi câu hỏi mua thêm thời gian cho kẻ gian.
    - Trả lời kèm giới hạn (“có thể là lừa đảo, bạn cân nhắc”): vẫn để nút nhả và vẫn đặt quyết định vào tay người đang bị thao túng.
    - Tự nhả sau khi xác thực khuôn mặt: khuôn mặt đúng không chứng minh sự đồng ý tự do; kẻ gian có thể ngồi cạnh và hướng dẫn.

- Loại lỗi: lỗi ngữ cảnh (PAIR context error). Hệ thống chạy đúng thiết kế (giữ giao dịch rủi ro) nhưng sai với tình huống người dùng đang bị doạ. Vì là lỗi ngữ cảnh, cách sửa không phải câu xin lỗi hay câu giải thích dài, mà là bỏ quyền nhả khỏi màn hình khách và đưa người thật vào. Câu chữ không được đổ lỗi (“bạn nhẹ dạ”) và không được hứa “chắc chắn an toàn”.

- HAX/PAIR - mỗi nguyên tắc trỏ vào một chỗ:

| Nguyên tắc | Chỗ trên prototype | Cách thể hiện |
|---|---|---|
| **G2** - làm rõ hệ thống làm được gì | Banner dưới tên trợ lý, số **1** trên ảnh 1 | “Trợ lý AI · không tự nhả tiền, không tự mở khoá ví. Quyết định nhả thuộc tư vấn viên.” |
| **G9 + PAIR Feedback & Control** - sửa và dừng dễ | Nút **Đây không phải giao dịch của tôi** (trong thẻ AI) và **Huỷ chuyển** (số **5**) trên ảnh 1 | Người dùng sửa được thông tin sai và huỷ chuyển người trước khi tư vấn viên nhận; không phải bắt đầu lại |
| **G11 + PAIR Explainability** - giải thích vì sao, để người dùng tự kiểm | Thẻ **Dựa vào**, số **3** trên ảnh 1 | Ba dòng chỉ dùng điều người dùng thấy được; không có điểm số gian lận, không có ngưỡng nội bộ |

- Lỗi sửa câu chữ không cứu được: Một câu cảnh báo hoàn hảo vẫn không cản được người đang tin kẻ gọi. Chỉ thiết kế mới cứu được: bỏ nút nhả, giữ tiền, và đưa người thật vào trước khi tiền đi. Prototype làm đúng ba việc đó.

### 3.2 Kịch bản #9 - người thật đang gấp ở quầy viện phí

- AI nói (nguyên văn):

> “Mình thấy giao dịch 2.000.000₫ đang chờ xác minh. Bạn bấm ‘Xác minh khuôn mặt’ ngay; nếu quá 60 giây chưa xong, mình chuyển tư vấn viên ưu tiên. Mình không tự nhả giao dịch - người duyệt sẽ thấy đây là ca quầy viện phí và duyệt trong khoảng 1 phút.”

- Người dùng thấy gì: Thẻ `GD-2B9N · 2.000.000₫ · Đã xác minh · chờ duyệt`; chip “Mình không đủ căn cứ để tự nhả, nên mình chuyển người thay vì đoán”; thẻ “Dựa vào” (lời người dùng, giao dịch đang chờ, người nhận là bệnh viện); nút "Xác minh ngay", "Gọi tư vấn viên ưu tiên", "Xem vì sao bị giữ". Sau khi xác minh: thẻ “Tư vấn viên đã thấy · 0:38” và console có "Duyệt nhả" bật; khách không có nút nhả.

- Người dùng làm gì tiếp: Bấm xác minh ngay; nếu muốn, gọi tư vấn viên ưu tiên; hoặc huỷ chuyển. Nếu huỷ, giao dịch vẫn giữ và khách có thể gọi lại bất cứ lúc nào; không tự nhả.

- Ai được báo, sau bao lâu: Ca vào hàng đợi ưu tiên ngay sau khi xác minh; mục tiêu 60 giây, prototype mô phỏng 0:38. Nếu quá 60 giây, đẩy lên trưởng ca và gọi lại; giao dịch vẫn giữ. Khách thấy thời gian chờ, không phải màn hình trắng.

- Quyết định: trả lời kèm giới hạn + chuyển người ưu tiên. Đã loại:
    - Hỏi lại (“ai nhận, chuyển để làm gì?”): người đang đứng ở quầy viện phí đã nói đủ; hỏi thêm là biến sự cố của hệ thống thành việc của khách.
    - Tự nhả theo ngưỡng (“dưới 2 triệu thì cho đi”): phải nêu ngưỡng, tạo kẽ hở chia nhỏ giao dịch, và một lần nhả sai là không đảo được.
    - Hàng đợi chung: đúng quy trình nhưng sai với người đang gấp; 60 giây phải là ưu tiên nhìn thấy được, không phải lời hứa.

- Loại lỗi: lỗi hệ thống (false positive). Mô hình rủi ro giữ một giao dịch hợp lệ; hệ thống chạy đúng thiết kế nhưng sai với ngữ cảnh bệnh viện. Vì là lỗi hệ thống, cách nói phải nhận phần chậm của hệ thống, không đổ lỗi cho khách; cách sửa là làn ưu tiên + người duyệt, không chỉ là câu xin lỗi.

- HAX/PAIR - mỗi nguyên tắc trỏ vào một chỗ:

| Nguyên tắc | Chỗ trên prototype | Cách thể hiện |
|---|---|---|
| **G2** - làm rõ hệ thống làm được gì | Banner số **1** trên ảnh 2 | Nói ngay AI không tự nhả tiền; người duyệt là tư vấn viên |
| **G9 + PAIR Feedback & Control** - sửa và dừng dễ | Nút **Gọi tư vấn viên ưu tiên** trên ảnh 2; nút **Huỷ yêu cầu** ở bước xác minh ngay trước đó; nút **Huỷ chuyển** (số **5**) | Người dùng huỷ được yêu cầu/chuyển người; không mất giao dịch khi huỷ |
| **G11 + PAIR Explainability** - giải thích vì sao | Thẻ **Dựa vào**, số **3** trên ảnh 2 | Nói rõ vì sao chờ: giao dịch đang chờ xác minh, người nhận là bệnh viện, người duyệt thấy gì |

- Lỗi sửa câu chữ không cứu được: Một lời xin lỗi hay hơn không làm tiền đến quầy nhanh hơn. Chỉ làn ưu tiên có người thật duyệt trong 60 giây mới cứu được trải nghiệm; câu chữ chỉ giữ được niềm tin trong lúc chờ.

## §4. Mức tự chủ  (chặng 4)
Với mỗi tool:
- Mức của nhóm (tự làm / cần người duyệt / cấm). Nếu cần người duyệt: ai duyệt · người duyệt thấy gì · quá hạn thì sao.
- Lý do theo cost-of-error: sai thì ai chịu gì · đảo lại được không · chờ người thì mất gì.
- Phương án đã cân nhắc và vì sao loại.
Thêm:
- Tool khó xếp nhất: mỗi người từng chọn gì, cái giá của mỗi phía (trỏ về kịch bản ở §2), nhóm chốt thế nào.
- Thử mức đã đặt trên 2 kịch bản đắt nhất + 1 kịch bản bình thường: cái sai có bị chặn không? còn việc nào làm khi lẽ ra phải hỏi? người dùng bình thường có phải chờ vô ích không?
- Luật thêm hoặc tool tách bước (nếu có), và vì sao.
- Một mức tự chủ đã đổi lời hứa nào với người dùng.

## §5. Prototype  (chặng 5)
- Link hoặc file · công cụ · phần nào mock · có lời gọi AI thật không.
- 1–2 ảnh có đánh số; mỗi số: thể hiện gì · nguyên tắc HAX/PAIR nào · mức tự chủ nào.
- Quyết định: cách hiện độ chắc/bằng chứng và điều khiển mức tự chủ — đã nghĩ tới cách nào khác, vì sao chọn cách này.

## §6. Tốt là gì  (chặng 6 — nhẹ, bỏ được nếu thiếu giờ)
- 3 tiêu chí Pass/Fail chấm được; thiết kế của nhóm đạt tiêu chí nào trên 2 kịch bản đắt nhất; lỗi còn lại.

## §7. Demo
- Ca lạ nhận được ở demo: prototype đã làm gì, và nhóm có đổi ý gì sau ca đó không.
```
