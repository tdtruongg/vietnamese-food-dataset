# Vietnamese Food Dataset (1,962 Images + Labels)

Tập dữ liệu chuẩn hóa gồm đúng 1.962 ảnh món ăn Việt Nam chất lượng cao và nhãn bounding box (đã loại bỏ toàn bộ ảnh chất lượng kém / không đạt chuẩn).

---

## 📊 Thống Kê Tổng Quan

- **Tổng số ảnh**: 1.962 ảnh
- **Tổng số file nhãn**: 1.962 file (.txt tương ứng từng ảnh)
- **Tổng số bounding box**: 7508 boxes
- **Số lớp đối tượng (Classes)**: 51 lớp món ăn Việt Nam

---

## 📁 Cấu Trúc Thư Mục Trong File Zip

```
vietnamese_food_dataset/
├── images/                       # Chứa đúng 1.962 ảnh (.jpg)
├── labels/                       # 1.962 file nhãn YOLO (.txt)
├── obj_train_data/               # 1.962 file nhãn định dạng Darknet / CVAT
├── train.txt                     # Danh sách 1.962 ảnh dùng để huấn luyện
├── classes.txt                   # Danh sách 51 tên class món ăn
├── obj.names                     # Danh sách class định dạng Darknet
├── obj.data                      # Cấu hình Darknet
├── data.yaml                     # Cấu hình huấn luyện cho Ultralytics YOLO (v5/v8/v11)
├── annotations_coco.json         # File nhãn COCO 1.0 (cho MMDetection, Detectron2, CVAT)
└── README.md                     # Tài liệu hướng dẫn
```

---

## 🚀 Hướng Dẫn Sử Dụng

### 1. Huấn luyện với Ultralytics YOLO (v8 / v11)
File `data.yaml` đã được thiết lập sẵn:
```python
from ultralytics import YOLO

model = YOLO('yolov8n.pt')
model.train(data='data.yaml', epochs=100, imgsz=640)
```

### 2. Huấn luyện với Darknet
Sử dụng: `obj.data`, `obj.names`, `train.txt`

### 3. Huấn luyện với MMDetection / Detectron2 / PyTorch
Sử dụng: `annotations_coco.json` và thư mục ảnh `images/`

---

## 📋 Danh Sách 51 Lớp Món Ăn
0. bánh bèo
1. bánh bột lọc
2. bánh canh
3. bánh chưng
4. bánh cuốn
5. bánh căn
6. bánh giò
7. bánh khọt
8. bánh mì
9. bánh pía
10. bánh tráng
11. bánh tét
12. bánh xèo
13. bánh đúc
14. bún bò Huế
15. bún
16. bún mắm
17. bún riêu
18. bún thịt nướng
19. bún đậu mắm tôm
20. canh chua
21. cao lầu
22. cháo lòng
23. chả
24. cua
25. cá chiên
26. cơm chiên
27. cơm tấm
28. gà luộc
29. gỏi
30. gỏi cuốn
31. heo quay
32. hàu
33. hủ tiếu
34. lẩu
35. mì Quảng
36. mực
37. nem chua
38. ngao sò
39. phở
40. rau sống
41. súp cua
42. thịt bò
43. rau luộc
44. tôm
45. xôi xéo
46. ốc
47. món ăn khác
48. rau xào
49. nước chấm
50. gà quay
