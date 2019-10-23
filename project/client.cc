#include "pong.h"
#include <cstring>
#include <asio.hpp>
using asio::ip::udp;

asio::io_service service;
udp::resolver resolver(service);
udp::endpoint send_endpoint;
udp::socket sock(service, udp::endpoint(udp::v4(), PPORT));

sf::RenderWindow g_window(sf::VideoMode(WIDTH, HEIGHT), "test");
gamestate g_state;
drawinfo g_info;
const uint8_t player = PPLAYER;

void handle_send(std::error_code ec, std::size_t bytes_send) {}
void handle_recv(std::error_code ec, std::size_t bytes_recvd) {
    if(!ec && bytes_recvd > 0) {
        update_display(g_state, g_info);
        draw(g_window, g_info);
    }
    sock.async_receive_from(asio::buffer((uint8_t*)&g_state, sizeof(gamestate)), send_endpoint, handle_recv);
}

void handle_input() {
    static auto event = sf::Event();
    if(g_window.isOpen()) {
        if(g_window.pollEvent(event)) {
            switch(event.type) {
                case sf::Event::Closed:
                    g_window.close();
                    break;
                case sf::Event::KeyPressed: {
                    uint8_t key[] = {player, 0};
                    switch(event.key.code) {
                        case sf::Keyboard::Up:
                            key[1] = 0;
                            sock.async_send_to(asio::buffer(key, sizeof(uint8_t) * 2), send_endpoint, handle_send);
                            break;
                        case sf::Keyboard::Down:
                            key[1] = 1;
                            sock.async_send_to(asio::buffer(key, sizeof(uint8_t) * 2), send_endpoint, handle_send);
                            break;
                        default:
                            break;
                    }
                    break;
                }
                default:
                    break;
            }
        }
        service.post(handle_input);
    }
    else
        exit(0);
}

int main() {
    send_endpoint = *resolver.resolve({udp::v4(), "localhost", "5555"});
    uint8_t key[] = {player, 0};
    sock.send_to(asio::buffer(key, sizeof(uint8_t) * 2), send_endpoint);
    sock.receive_from(asio::buffer((uint8_t*)&g_state, sizeof(gamestate)), send_endpoint);

    sock.async_receive_from(asio::buffer((uint8_t*)&g_state, sizeof(gamestate)), send_endpoint, handle_recv);
    service.post(handle_input);
    service.run();
}
