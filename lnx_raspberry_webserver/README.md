![logo](screen/logo.png)

# Всім привіт 👋 Зміст:
- [Встановлення і налаштування RaspBerry](#встановити-операційну-систему-за-допомогою-imager)
- [Підключення по SSH](#робимо-підключення-по-ssh)
- [Перекидання файлів через SCP](#перекидаємо-папку-на-raspberry-через-scp)
- [Робота з S-bit](#запускаємо-netroute-на-raspberry)
- [Налаштування веб-сервер Apache](#налаштування-веб-сервер-apache)

## Встановити операційну систему за допомогою Imager

``` Bash
# aspire 192.168.3.155
wget https://downloads.raspberrypi.org/imager/imager_latest_amd64.deb
sudo apt install rpi-imager
rpi-imager
```

Вибираємо пристрій, вибираємо ОС і накопичувач

![alt text](screen/image.png)

Edit settings

![alt text](screen/image-4.png)

General

![alt text](screen/image-1.png)

Services

![alt text](screen/image-2.png)

Option

![alt text](screen/image-3.png)

Yes

![alt text](screen/image-5.png)

Yes

![alt text](screen/image-6.png)

Continue

![alt text](screen/image-7.png)


Встановлюємо SD в плату

![alt text](screen/photo-1.jpg)

Піключаємо живлення, Ethernet

![alt text](screen/photo-2.jpg)

## Робимо підключення по SSH

Скануємо всі ip в локальній мережі через nmap і шукаємо ip Raspberry

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

## Перекидаємо папку на raspberry через SCP

Створюємо робочу дерикторію

``` Bash
# raspberry 192.168.3.181
mkdir myFolder
```

![alt text](screen/image-10.png)

Перекидаємо папку

``` Bash
# aspire 192.168.3.155
ll Desktop/
scp -r Desktop/src rasp@192.168.3.181:myFolder/
```

![alt text](screen/image-11.png)

``` Bash
# raspberry 192.168.3.181
cd myFolder/src
ls
make start
sudo chmod +x netrouter
sudo cp netrouter /usr/local/bin
make clean
cd ~
```

## Запускаємо netroute на raspberry

Посилання на цей [проєкт](https://github.com/iPlugin/projects/tree/main/cpp_openwrt_netrouter) є в моєму github

``` Bash
# raspberry 192.168.3.181
sudo chmod 4755 /usr/local/bin/netrouter
netrouter 8.8.8.8
rm -r myFolder/src
```

![alt text](screen/image-12.png)

## Налаштування веб-сервер Apache

``` Bash
# raspberry 192.168.3.181
sudo apt update && sudo apt upgrade
sudo apt install apache2 -y
```

![alt text](screen/image-13.png)

``` Google request
# aspire 192.168.3.155
Google request: 192.168.3.181
```

![alt text](screen/image-14.png)

``` Bash
# raspberry 192.168.3.181
cd /var/www/html
ls -al
sudo chown rasp: index.html
```

![alt text](screen/image-15.png)

Встановлення PHP для Apache

``` Bash
# raspberry 192.168.3.181
sudo apt install php libapache2-mod-php -y
sudo rm index.html
sudo nano index.php
cat index.php
```

![alt text](screen/image-16.png)

``` Google request
# aspire 192.168.3.155
Google request: 192.168.3.181
```

![alt text](screen/image-17.png)