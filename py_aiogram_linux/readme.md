
# Інструкція


1. Білдинг образу(image) ```docker build . --platform=linux/amd64 -t hajusag/linux_tracker:0.0.1``` 0.0.1 - це версія, кожного разу треба підіймати на 1
2. Завантаження/Upload образу на DockerHub ```docker push hajusag/linux_tracker:0.0.1```
3. Завантаження на Linux Server ```sudo docker pull hajusag/linux_tracker:0.0.1```
4. Інструкція запуску контейнера на сервері
5. Вхід на сервер через термінал ``` ssh kiraparcer@195.201.150.230 ```

6. Перед запуском нового контейнера, треба зупинити та видалити старий

7. Запуск Docker контейнеру на сервері 
```sudo docker run --name linux_memory_tracker  hajusag/linux_tracker:0.0.1```

## пояснення 
Замість ```hajusag/linux_tracker:0.0.1``` - підставте свій репозиторій з ДокерХабу