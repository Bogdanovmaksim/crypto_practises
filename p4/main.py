import numpy as np
import math
import matplotlib.pyplot as plt
from PIL import Image, ImageEnhance
from skimage.metrics import structural_similarity as ssim
import os


# Конвертация текста
def text_to_bits(text):
    bytes_data = text.encode('utf-8')
    bits_str = ''.join(f"{b:08b}" for b in bytes_data)
    return np.array([int(bit) for bit in bits_str])


def bits_to_text(bits):
    bit_str = ''.join(bits.astype(str))
    bytes_list = [int(bit_str[i:i + 8], 2) for i in range(0, len(bit_str), 8) if len(bit_str[i:i + 8]) == 8]
    return bytearray(bytes_list).decode('utf-8', errors='ignore')


# Алгоритм QIM
def embed_qim(img_matrix, bit_array, q):
    if q % 2 != 0:
        raise ValueError("Шаг квантования q должен быть четным.")

    stego_matrix = img_matrix.astype(np.float64).copy()
    blue_channel = stego_matrix[:, :, 2].flatten()

    n_bits = len(bit_array)
    if n_bits > len(blue_channel):
        raise ValueError("Сообщение слишком длинное для этого изображения.")

    target_pixels = blue_channel[:n_bits]
    embedded_pixels = np.floor(target_pixels / q) * q + (q // 2) * bit_array

    blue_channel[:n_bits] = embedded_pixels
    blue_channel = np.clip(blue_channel, 0, 255)

    stego_matrix[:, :, 2] = blue_channel.reshape(img_matrix.shape[0], img_matrix.shape[1])
    return stego_matrix.astype(np.uint8)


def extract_qim(stego_matrix, msg_length, q):
    blue_channel = stego_matrix[:, :, 2].flatten().astype(np.float64)
    target_pixels = blue_channel[:msg_length]

    p0 = np.floor(target_pixels / q) * q
    p1 = p0 + (q / 2)

    diff0 = np.abs(target_pixels - p0)
    diff1 = np.abs(target_pixels - p1)

    return np.where(diff0 < diff1, 0, 1)

# Метрики
def print_metrics(orig, stego, num_bits, original_bits=None, extracted_bits=None):
    mse = np.mean((orig.astype(np.float64) - stego.astype(np.float64)) ** 2)
    rmse = math.sqrt(mse)
    psnr = float('inf') if mse == 0 else 10 * math.log10((255.0 ** 2) / mse)
    ssim_val = ssim(orig, stego, channel_axis=-1)
    ec = num_bits / (orig.shape[0] * orig.shape[1])

    # Расчёт BER и NCC, если переданы биты
    if original_bits is not None and extracted_bits is not None:
        ber = np.sum(original_bits != extracted_bits) / len(original_bits) if len(original_bits) > 0 else 1
        orig_float = original_bits.astype(np.float64)
        ext_float = extracted_bits.astype(np.float64)
        numerator = np.sum(orig_float * ext_float)
        denominator = np.sqrt(np.sum(orig_float ** 2)) * np.sqrt(np.sum(ext_float ** 2))
        ncc = numerator / denominator if denominator != 0 else 0
    else:
        ber = 0
        ncc = 0

    print("\n--- ОЦЕНКА ЭФФЕКТИВНОСТИ ---")
    print(f"Ёмкость (EC): {ec:.6f} bpp")
    print(f"MSE:          {mse:.4f}")
    print(f"RMSE:         {rmse:.4f}")
    print(f"PSNR:         {psnr:.2f} dB")
    print(f"SSIM:         {ssim_val:.4f}")
    print(f"BER:          {ber:.4f}")
    print(f"NCC:          {ncc:.6f}")


def plot_histograms(orig_arr, stego_arr):
    orig_blue = orig_arr[:, :, 2].flatten()
    stego_blue = stego_arr[:, :, 2].flatten()

    plt.figure(figsize=(10, 4))
    plt.subplot(1, 2, 1)
    plt.hist(orig_blue, bins=256, range=[0, 256], color='blue', alpha=0.7)
    plt.title('Оригинал (Синий канал)')

    plt.subplot(1, 2, 2)
    plt.hist(stego_blue, bins=256, range=[0, 256], color='red', alpha=0.7)
    plt.title('Стего (Синий канал)')
    plt.show()


# Интерфейс
def main():
    while True:
        print("\nМЕТОД QIM")
        print("1. Встроить сообщение")
        print("2. Извлечь сообщение")
        print("3. Исказить изображение (тест робастности)")
        print("0. Выход")
        choice = input("Выберите действие: ")

        if choice == '1':
            in_file = input("Имя исходного изображения (например, input1.jpg): ")
            if not os.path.exists(in_file):
                print("Файл не найден. Создаю тестовый input1.jpg...")
                Image.fromarray(np.random.randint(0, 256, (256, 256, 3), dtype=np.uint8)).save("input1.jpg")
                in_file = "input1.jpg"

            out_file = input("Имя для сохранения (например, stego.png): ") or "stego.png"
            q = int(input("Шаг квантования q (четное число, например 16): ") or 16)
            text = input("Введите секретное сообщение: ")

            orig = np.array(Image.open(in_file).convert('RGB'))
            bits = text_to_bits(text)

            # Встраивание
            stego = embed_qim(orig, bits, q)
            Image.fromarray(stego).save(out_file)
            print(f"\nСообщение успешно встроено в {out_file}!")
            print(f"Параметры: шаг q = {q}, длина в битах = {len(bits)}")

            # Оценка
            print_metrics(orig, stego, len(bits))
            plot_histograms(orig, stego)

        elif choice == '2':
            stego_file = input("Имя стегоизображения: ")
            q = int(input("Введите шаг квантования q, который использовался: "))
            msg_len = int(input("Введите длину сообщения в битах: "))

            try:
                stego = np.array(Image.open(stego_file).convert('RGB'))
                ext_bits = extract_qim(stego, msg_len, q)
                print(f"\nИЗВЛЕЧЕННОЕ СООБЩЕНИЕ: {bits_to_text(ext_bits)}")
            except Exception as e:
                print(f"Ошибка извлечения: {e}")

        elif choice == '3':
            print("\n--- ТЕСТ НА РОБАСТНОСТЬ ---")
            stego_file = input("Имя стегоизображения для искажения: ")
            try:
                img = Image.open(stego_file)
                # Сохраняем в JPEG
                jpeg_name = "stego_compressed.jpg"
                img.save(jpeg_name, format="JPEG", quality=80)
                print(f"Сжатая JPEG-копия сохранена как '{jpeg_name}'")

                # Меняем яркость
                bright_name = "stego_bright.png"
                ImageEnhance.Brightness(img).enhance(1.3).save(bright_name)
                print(f"Копия с измененной яркостью сохранена как '{bright_name}'")
                print("Теперь попробуй извлечь текст из этих новых файлов (Пункт 2 меню)!")
            except Exception as e:
                print(f"Ошибка: {e}")

        elif choice == '0':
            break
        else:
            print("Неверный ввод.")


if __name__ == "__main__":
    main()
