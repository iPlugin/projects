GL_BaseCamp
Hi everyone, I get the test:

[ Client/Server application to search files on remote HOST ]

- the client has the functionality to search files by a server request.
- the server will request a search by "file name"
- the client has to replay with "processing" each 500ms of searching
- the client has to reply with success or failure.
- success replay has to include a full path to the file.

===========================================================

[ For start, you need: ]

*For compiling software code*
- $ make
*For start the server*
- $ ./server 2000
*For start the client*
- $ ./client 127.0.0.1 2000 utils.cpp
*For delete files created during compilation*
- $ make clean

===========================================================

[ Sources of information used: ]

- socket 1 = https://www.youtube.com/watch?v=KEiur5aZnIM&t=448s
- socket 2 = https://www.youtube.com/watch?v=_lQ-3S4fJ0U&list=PLPyaR5G9aNDvs6TtdpLcVO43_jvxp4emI
- thread (repeated) = https://www.youtube.com/watch?v=ZqIUDTZRx5s