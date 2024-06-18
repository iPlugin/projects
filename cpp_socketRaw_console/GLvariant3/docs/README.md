GL_BaseCamp
Hi everyone, I get the test №3:

[ Client/Server application to search files on remote HOST ]

Implement Packets checker application.
- Create simple TCP based client-server applications.
- Create a proxy application (that is in the middle).
- Application logic:
	- Client sends data to Proxy. 
	- Option1: Proxy just forwards it to the server.
	- Option2: Proxy does modifications in payload and resend them to server.

For Option2: Server must figure out that data has been changed in the middle (calculating packet checksum).


===========================================================

[ For start, you need: ]

Tags:
v1.0.0			: without music 
v1.0.0_audio	: with music

*For install software for music*
- $ sudo apt-get install libsdl2-dev libsdl2-mixer-dev

*For compiling software code*
- $ make
*For start the server*
- $ sudo ./runServer 2000 2001
*For start the proxy*
- $ sudo ./runProxy proxy 2001 2000 2002
*For start the client*
- $ sudo ./runClient 2002 2001 test.txt
*For delete files created during compilation*
- $ make clean

===========================================================

[ Sources of information used: ]

- Git tags = https://www.youtube.com/watch?v=WUEL8AHlQlI
- Raw Socket 1 = https://habr.com/ru/companies/smart_soft/articles/184430/
- Raw Socket 2 = https://habr.com/ru/articles/183316/
- Raw Socket 3 = https://sock-raw.org/papers/sock_raw
- Raw Socket 3 = https://www.youtube.com/watch?v=BkQiZ5rSR8A&t=944s
- Checksum Calculated = https://www.youtube.com/watch?v=_zMf4KYoKbM&t=79s