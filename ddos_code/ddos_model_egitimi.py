import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Dense



# Excel dosyalarını oku
df_saldiri = pd.read_excel(r"C:\Users\Lenovo\Downloads\dos_flows_43_features-_2_.xlsx")
df_normal = pd.read_excel(r"C:\Users\Lenovo\Downloads\normal_flows_43_features-_2_.xlsx")

# Etiketle (1: saldırı, 0: normal)
df_saldiri["label"] = 1
df_normal["label"] = 0

# Birleştir
df = pd.concat([df_saldiri, df_normal], ignore_index=True)
df = df.sample(frac=1).reset_index(drop=True)

# X ve y ayır
X = df.drop("label", axis=1)
y = df["label"]

# Sayısal olmayan verileri temizle
X = X.apply(pd.to_numeric, errors='coerce')
X = X.fillna(0)

# Tip dönüşümleri
X = X.astype('float32')
y = y.astype('int')

# Eğitim/test ayır
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Model oluştur
model = Sequential()
model.add(Dense(64, input_shape=(X_train.shape[1],), activation='relu'))
model.add(Dense(32, activation='relu'))
model.add(Dense(1, activation='sigmoid'))

# Derle
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

# Eğit
model.fit(X_train, y_train, epochs=20, batch_size=32, validation_split=0.1)

# Test et
loss, accuracy = model.evaluate(X_test, y_test)
print(f"Test doğruluğu: {accuracy:.2f}")

# Modeli Keras formatında kaydet
model.save("ddos_model1.keras")
