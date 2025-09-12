import board
import busio
from digitalio import DigitalInOut
from adafruit_pn532.spi import PN532_SPI

# Инициализация SPI
spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
cs_pin = DigitalInOut(board.D8)  # Укажите пин CS
pn532 = PN532_SPI(spi, cs_pin, debug=False)

# Инициализация NFC-модуля
pn532.SAM_configuration()

print("Поднесите NFC-карту к модулю...")

try:
    while True:
        # Проверка наличия карты
        uid = pn532.read_passive_target(timeout=0.5)
        if uid is not None:
            print("Найдена карта с UID:", [hex(i) for i in uid])
except KeyboardInterrupt:
    print("Программа завершена.")