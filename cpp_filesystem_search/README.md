# GL_BaseCamp

Привіт, отримав технічне завдання:

Application (App) to find file on Local Host:
1. App has to find file by "name"
2. Search has to be started from root "/" directory.
3. To make this search faster - App creates new Searching Thread
for each sub directory in root directory, but not more thon 8 Execution Threads.
4. Thread Who will Find needed File has to print Full Path to the file and
has to notify all the rest threads to stop searching.

- Logic "to search file" has to be placed into static library.
- Application just uses this library to find files in a fast way.
- Static Library compilation has to be done separately from Application.
- Compiler: GCC or G++.
- Use Makefile for compilation/linking instructions.

Things to Google: (Concurrency, Makefile, GCC, Static Library)

============================================

Для запуску потрібно:

- : make // для збірки програмного коду
- : ./search_app // для запуску програми
- : make clean // для видалення файлів які сторилися під час компіляції

============================================

Джерела які використовував:

- filesystem = https://medium.com/@sshambir/%D0%BF%D1%80%D0%B8%D0%B2%D0%B5%D1%82-std-filesystem-4c7ed50d5634
- Рекурсія = https://www.youtube.com/watch?v=wnXogMRQNYQ
- Час виконання коду = https://www.youtube.com/watch?v=bN6dfoGK38Y
- Потоки 1 = https://www.youtube.com/watch?v=NawpxG81RRk&list=PLQOaTSbfxUtCrKs0nicOg2npJQYSPGO9r&index=169
- Потоки 2 = https://www.youtube.com/watch?v=UEtWLpDOg68&list=PLQOaTSbfxUtCrKs0nicOg2npJQYSPGO9r&index=171
- Багатофайловий проєкт - https://www.youtube.com/watch?v=pAxEfF2yVlM
- Makefile = створював ChatGTP