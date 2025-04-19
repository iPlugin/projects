![logo](screen/logo.png)

# Всім привіт 👋
### Організував радіозв’язок між двома Raspberry Pi (rasp1 і rasp2) через LoRa SX1268 за допомогою Python-скриптів

- [Встановлення і налаштування RaspBerry](#встановлення-і-налаштування-raspberry)
- [Підключення по SSH до RaspBerry](#підключення-по-ssh-до-raspberry)
- [Налаштування Raspberry Pi](#налаштування-raspberry-pi-rasp1)
- [Результат роботи LoRa](#передача-повідомлень)

### Компоненти:
- Два Raspberry Pi (rasp1 і rasp2)
- Два LoRa-модулі SX1268 (Waveshare)
- Антени
- SD-карти з Raspberry Pi OS
- Живлення для обох плат
- Комп’ютер для конфігурації (aspire)

## Встановлення і налаштування RaspBerry

``` Bash
# aspire 192.168.3.155
wget https://downloads.raspberrypi.org/imager/imager_latest_amd64.deb
sudo apt install rpi-imager
rpi-imager
```

### Вибираємо пристрій, вибираємо ОС і накопичувач (rasp1)

![alt text](screen/iimage.png)

#### Edit settings (rasp1)

![alt text](screen/iimage2.png)

#### General (rasp1)

![alt text](screen/iimage3.png)

#### Services (rasp1)

![alt text](screen/iimage4.png)

#### Option (rasp1)

![alt text](screen/iimage5.png)

#### Yes (rasp1)

![alt text](screen/iimage6.png)

#### Yes (rasp1)

![alt text](screen/iimage7.png)

#### Continue (rasp1)

![alt text](screen/image.png)

#### Піключаємо до живлення, встановлюємо SD, модуль SX1268 LoRa (rasp1)

![alt text](screen/photo1.jpg)

### Вибираємо пристрій, вибираємо ОС і накопичувач (rasp2)

![alt text](screen/iimage.png)

#### Edit settings (rasp2)

![alt text](screen/iimage2.png)

#### General (rasp2)

![alt text](screen/image-1.png)

#### Services (rasp2)

![alt text](screen/image-2.png)

#### Option (rasp2)

![alt text](screen/image-3.png)

#### Yes (rasp2)

![alt text](screen/image-4.png)

#### Yes (rasp2)

![alt text](screen/image-5.png)

#### Continue (rasp2)

![alt text](screen/image-8.png)

#### Піключаємо до живлення, встановлюємо SD, модуль SX1268 LoRa (rasp2)

![alt text](screen/photo2.jpg)

## Підключення по SSH до RaspBerry

### Скануємо всі ip в локальній мережі через nmap і шукаємо ip RaspBerry (rasp1)

``` Bash
# aspire 192.168.3.155
sudo apt install nmap
sudo nmap -sn 192.168.3.0/24
```

![alt text](screen/image-6.png)

``` Bash
# aspire 192.168.3.155
ssh rasp1@192.168.3.182
```

![alt text](screen/image-7.png)

### Скануємо всі ip в локальній мережі через nmap і шукаємо ip RaspBerry (rasp2)

``` Bash
# aspire 192.168.3.155
sudo nmap -sn 192.168.3.0/24
```

![alt text](screen/image-9.png)

``` Bash
# aspire 192.168.3.155
ssh rasp2@192.168.3.183
```

![alt text](screen/image-10.png)

## Налаштування Raspberry Pi (rasp1)

``` Bash
# rasp1
sudo apt update && sudo apt upgrade
sudo raspi-config
```

#### Interfacing Options (rasp1)

![alt text](screen/image-11.png)

#### Serial Port (rasp1)

![alt text](screen/image-12.png)

#### No (rasp1)

![alt text](screen/image-13.png)

#### Yes (rasp1)

![alt text](screen/image-14.png)

#### Ok (rasp1)

![alt text](screen/image-15.png)

#### Yes (rasp1)

![alt text](screen/image-16.png)

``` Bash
# rasp1
cd Documents
wget https://files.waveshare.com/upload/1/18/SX126X_LoRa_HAT_CODE.zip
unzip SX126X_LoRa_HAT_CODE.zip
```

![alt text](screen/image-23.png)

``` Bash
# rasp1
sudo apt install python3-serial
```

![alt text](screen/image-25.png)

``` Bash
# rasp1
cd SX126X_LoRa_HAT_Code/raspberrypi/python/
sudo nano main.py # addr=1
```

![alt text](screen/image-26.png)

``` Bash
# rasp1
sudo python3 main.py
```

![alt text](screen/image-31.png)

## Налаштування Raspberry Pi (rasp2)

``` Bash
# rasp2
sudo apt update && sudo apt upgrade
sudo raspi-config
```

#### Interfacing Options (rasp2)

![alt text](screen/image-17.png)

#### Serial Port (rasp2)

![alt text](screen/image-18.png)

#### No (rasp2)

![alt text](screen/image-19.png)

#### Yes (rasp2)

![alt text](screen/image-20.png)

#### Ok (rasp2)

![alt text](screen/image-21.png)

#### Yes (rasp2)

![alt text](screen/image-22.png)

``` Bash
# rasp2
sudo apt install python3-serial
cd Documents
wget https://files.waveshare.com/upload/1/18/SX126X_LoRa_HAT_CODE.zip
unzip SX126X_LoRa_HAT_CODE.zip
```

![alt text](screen/image-24.png)

``` Bash
# rasp2
sudo apt install python3-serial
```

![alt text](screen/image-27.png)

``` Bash
# rasp2
cd SX126X_LoRa_HAT_Code/raspberrypi/python/
sudo nano main.py # addr=2
```

![alt text](screen/image-28.png)

``` Bash
# rasp2
sudo python3 main.py
```

![alt text](screen/image-32.png)

## Передача повідомлень

``` Bash
rasp1 -> "2,868,Вітаю з rasp1!" -> rasp2
```

![alt text](screen/image-29.png)

``` Bash
rasp2 -> "1,868,Вітаю з rasp2!" -> rasp1
```

![alt text](screen/image-30.png)