GL_BaseCamp Hi everyone, I get the test №1.2:

[ Client/Server application to close processes on remote HOST ]

- the client gets the processes list and sends them by server request.
- the server will request to close one of the processes on the client's host.
- the client has to reply with success or failure.

===========================================================

[ For start, you need ]

*Installing*
- $ sudo apt-get install libcurl4-openssl-dev
- $ sudo apt-get install nlohmann-json3-dev

*For compiling software code*
- $ make

*For start the server*
- $ sudo ./runServer

*For start the client*
- $ sudo ./runClient

*For delete files created during compilation*
- $ make clean

===========================================================

[ Sources of information used ]

Git tags = https://www.youtube.com/watch?v=WUEL8AHlQlI
Raw Socket 1 = https://habr.com/ru/companies/smart_soft/articles/184430/
Raw Socket 2 = https://habr.com/ru/articles/183316/
Raw Socket 3 = https://sock-raw.org/papers/sock_raw
Raw Socket 3 = https://www.youtube.com/watch?v=BkQiZ5rSR8A&t=944s
Checksum Calculated = https://www.youtube.com/watch?v=_zMf4KYoKbM&t=79s