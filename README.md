# 🐦 Q-Learning Flappy Bird  
**Cho máy tự học cách dùng chim của mình**

---

## 📌 Giới thiệu

Đúng vậy, bạn không nghe nhầm đâu 😄  
Đây là một project **Reinforcement Learning (Học tăng cường)**, trong đó một chú chim (Bird) trong game **Flappy Bird** có thể **tự học cách bay qua các cột** mà **không cần bất kỳ thao tác nào từ con người**.

Agent sẽ chơi đi chơi lại hàng chục nghìn ván, rút kinh nghiệm từ thất bại, để cuối cùng bay ngày càng mượt hơn 🧠✨

---

## 🧠 Giải thích dễ hiểu (Cho người không chuyên)

Bird sẽ học bằng cách **chơi rất nhiều ván**:

- Bay qua cột → **được thưởng**
- Bay đúng độ cao → **được thưởng nhẹ**
- Đâm cột hoặc rơi xuống đất → **bị phạt nặng**

Ban đầu Bird bay rất **ngu và loạn xạ** vì đang thử đủ mọi hành động.  
Nhưng sau nhiều lần bị phạt và được thưởng, nó dần **hiểu hành động nào là tốt**, giống như huấn luyện thú cưng vậy:

> Làm đúng thì cho pate 🍖  
> Làm sai thì bị đập 😈  
> Lặp lại đủ lâu thì pet sẽ khôn ra.

---

## ⚙️ Giải thích kỹ thuật (Cho người học ML/AI)

- **Bird** → Agent  
- **Flappy Bird** → Environment  

### 📍 State (Trạng thái)
Tại mỗi timestep, agent quan sát:
- Khoảng cách từ `y_bird` đến **tâm khe cột**
- Gia tốc rơi
- Khoảng cách `x` đến cột gần nhất

### 🎮 Action (Hành động)
- Bay lên
- Không bay

### 🎁 Reward (Phần thưởng)
- Bay qua cột → **+ reward**
- Bay gần tâm khe → **+ reward nhỏ**
- Đâm cột / rơi → **- reward lớn**

Tất cả được dùng để cập nhật **Q-table** (`q.npy`) sao cho:
- Hành động tốt trong quá khứ → có xác suất được lặp lại cao hơn trong tương lai

### 🔍 Exploration
- Sử dụng **Epsilon-Greedy**
- Ban đầu epsilon cao → khám phá → bay loạn
- Sau vài trăm episode → giảm epsilon → bay ổn định hơn

---

## 📊 Kết quả huấn luyện (20,000 episodes)

- 🏆 **Số cột vượt qua tối đa**: 101
- 📈 **Trung bình số cột / 100 episode**: ~13
- 🖥️ **Máy chạy liên tục**: ~3 ngày (đang hấp hối 😵)
- 🎯 Thường ổn định ở mức: **20–30 cột**

👉 Bird vẫn chưa đi xa hơn, có thể do:
- Chưa đủ episode
- Hoặc giới hạn của Q-learning dạng bảng

---

## 🚀 Cách cài đặt và chạy project

### 1️⃣ Clone repository
```bash
git clone https://github.com/bexanhtuoi/Q-Flappy-Bird.git
cd Q-Flappy-Bird
```

### 2️⃣ Tạo môi trường ảo (khuyến nghị)

**Windows**

```bash
python -m venv venv
venv\Scripts\activate
```

**Linux / macOS**

```bash
python3 -m venv venv
source venv/bin/activate
```

---

### 3️⃣ Cài đặt thư viện cần thiết

```bash
pip install -r requirements.txt
```

---

### 4️⃣ Chạy chương trình

```bash
python main.py
```

👉 Chim sẽ tự chơi, tự học, không cần bấm phím 🎮🐦

---

## ⚠️ LƯU Ý QUAN TRỌNG

### ❌ KHÔNG chỉnh sửa file `q.npy`

* `q.npy` là **Q-table đã được huấn luyện sẵn**
* Nếu bạn:

  * Xóa
  * Sửa
  * Ghi đè

👉 Chim sẽ **mất toàn bộ trí nhớ** và phải học lại từ đầu 😭

📌 **Chỉ chỉnh sửa `q.npy` khi bạn muốn train lại hoàn toàn từ đầu.**

---

## 🔗 Mã nguồn

👉 GitHub:
**[https://github.com/bexanhtuoi/Q-Flappy-Bird.git](https://github.com/bexanhtuoi/Q-Flappy-Bird.git)**

---

## 🎄 Merry Christmas :3
