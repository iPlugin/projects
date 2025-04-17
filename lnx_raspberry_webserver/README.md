![logo](screen/logo.png)

# Всім привіт 👋 Зміст:
- [Встановлення і налаштування RaspBerry](#встановлення-і-налаштування-raspberry)
- [Підключення по SSH до RaspBerry](#підключення-по-ssh-до-raspberry)
- [Перенесення PHP файлу через SCP](#перенесення-php-файлу-через-scp)
- [Налаштування веб-серверу Apache](#налаштування-веб-серверу-apache)

## Встановлення і налаштування RaspBerry

``` Bash
# aspire 192.168.3.155
wget https://downloads.raspberrypi.org/imager/imager_latest_amd64.deb
sudo apt install rpi-imager
rpi-imager
```

### Вибираємо пристрій, вибираємо ОС і накопичувач

![alt text](screen/image.png)

#### Edit settings

![alt text](screen/image-4.png)

#### General

![alt text](screen/image-1.png)

#### Services

![alt text](screen/image-2.png)

#### Option

![alt text](screen/image-3.png)

#### Yes

![alt text](screen/image-5.png)

#### Yes

![alt text](screen/image-6.png)

#### Continue

![alt text](screen/image-7.png)

#### Встановлюємо SD в плату

![alt text](screen/photo-1.jpg)

#### Піключаємо до живлення і Ethernet

![alt text](screen/photo-2.jpg)

## Підключення по SSH до RaspBerry

### Скануємо всі ip в локальній мережі через nmap і шукаємо ip RaspBerry

``` Bash
# aspire 192.168.3.155
sudo apt install nmap
sudo nmap -sn 192.168.3.0/24
```

![alt text](screen/image-8.png)

``` Bash
# aspire 192.168.3.155
ssh rasp@192.168.3.181
```

![alt text](screen/image-9.png)

## Перенесення PHP файлу через SCP

``` Bash
# aspire 192.168.3.155 -> 192.168.86.144
# raspberry 192.168.3.181 -> 192.168.86.32
```

#### Створюємо робочу дерикторію

``` Bash
# raspberry 192.168.86.32
mkdir myFolder
```

![alt text](screen/image-10.png)

#### Переносимо файл

``` Bash
# aspire 192.168.86.144
ll Desktop/
scp Desktop/file.php rasp@192.168.86.32:myFolder/
```

![alt text](screen/image-22.png)

## Налаштування веб-серверу Apache

``` Bash
# raspberry 192.168.86.32
sudo apt update && sudo apt upgrade
sudo apt install apache2 -y
```

![alt text](screen/image-13.png)


``` Bash
# raspberry 192.168.86.32
sudo mv myFolder/file.php /var/www/html/
cd /var/www/html
ls -al
sudo chown rasp: file.html
```

![alt text](screen/image-15.png)

``` Bash
# raspberry 192.168.86.32
sudo apt install php libapache2-mod-php -y
cat file.php
```

![alt text](screen/image-20.png)

``` Google request
# aspire 192.168.86.144
Google request: 192.168.86.32
```

![alt text](screen/image-23.png)