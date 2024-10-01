# import numpy as np
# from matplotlib import pyplot as plt
# from mpl_toolkits.mplot3d import Axes3D
#
#
# x = np.arange(4.23, 14.23, 0.05)
# y = x * np.power(x**2 - 1, 1/5)  # Định nghĩa hàm y = x * căn bậc 5 của (x^2 - 1)
# "theo định nghĩa c3"
# # arr = np.array([2, 3, 4, 5])
# # exponent = 3
# #
# # result = np.power(arr, exponent)
# # print(result)
# # Kết quả sẽ là:
# #
# # css
# # Copy code
# # [  8  27  64 125]
#
# plt.plot(x, y)
# plt.xlabel("Trục x")
# plt.ylabel("Trục y")
# plt.title('Đồ thị hàm số y = x * căn bậc 5 của (x^2 - 1)')
# plt.grid(True)
# plt.show()
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score

# Đọc dữ liệu từ file hoặc từ biến đã lưu trữ
data = {
    'age': [19, 18, 28, 33, 32, 31, 46, 37, 37, 60, 25, 62, 23, 56],
    'sex': ['female', 'male', 'male', 'male', 'male', 'female', 'female', 'female', 'male', 'female', 'male', 'female', 'male', 'female'],
    'bmi': [27.9, 33.77, 33, 22.705, 28.88, 25.74, 33.44, 27.74, 29.83, 25.84, 26.22, 26.29, 34.4, 39.82],
    'children': [0, 1, 3, 0, 0, 0, 1, 3, 2, 0, 0, 0, 0, 0],
    'smoker': ['yes', 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'yes', 'no', 'no'],
    'region': ['southwest', 'southeast', 'southeast', 'northwest', 'northwest', 'southeast', 'southeast', 'northwest', 'northeast', 'northwest', 'northeast', 'southeast', 'southwest', 'southeast'],
    'charges': [16884.924, 1725.5523, 4449.462, 21984.47061, 3866.8552, 3756.6216, 8240.5896, 7281.5056, 6406.4107, 28923.13692, 2721.3208, 27808.7251, 1826.843, 11090.7178]
}

df = pd.DataFrame(data)

# Xử lý biến phân loại thành dạng số bằng phương pháp mã hóa one-hot
df = pd.get_dummies(df, columns=['sex', 'smoker', 'region'])

# Tạo features (X) và target (y)
X = df.drop('charges', axis=1)
y = df['charges']

# Chia dữ liệu thành tập train và tập test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Tạo và fit mô hình
model = LinearRegression()
model.fit(X_train, y_train)

# Dự đoán trên tập test và tính toán độ đo R^2 và MSE
y_pred = model.predict(X_test)
r2 = r2_score(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)

print(f'R^2: {r2}')
print(f'Mean Squared Error: {mse}')