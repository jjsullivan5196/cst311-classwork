CXX := clang++ -std=c++17 -lpthread -lsfml-graphics -lsfml-window -lsfml-system

server: pong.h server.cc
	${CXX} -o server server.cc

client0: pong.h client.cc
	${CXX} -DPPORT=5550 -DPPLAYER=0 -o client0 client.cc

client1: pong.h client.cc
	${CXX} -DPPORT=5551 -DPPLAYER=1 -o client1 client.cc

clients: client0 client1
