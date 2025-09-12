import spidev

# Попробуйте разные скорости
speeds = [1000000, 500000, 2000000]

for speed in speeds:
    print(f"Тест на скорости {speed} Hz...")
    spi = spidev.SpiDev()
    spi.open(0, 0)
    spi.max_speed_hz = speed
    spi.mode = 0
    
    try:
        test_data = [0x00, 0x00, 0xFF, 0x02, 0xFE, 0xD4, 0x02, 0x2A, 0x00]
        response = spi.xfer2(test_data)
        print(f"Ответ: {[hex(x) for x in response]}")
    except Exception as e:
        print(f"Ошибка: {e}")
    finally:
        spi.close()
    print()