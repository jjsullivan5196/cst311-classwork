#include "pong.h"
#include <thread>
#include <chrono>
#include <algorithm>
#include <asio.hpp>

using hclock = std::chrono::high_resolution_clock;
using asio::ip::udp;
gamestate g_state {{50, 50}, {0, 0}, {50, 50}, {1, -1}, win_state::None};
asio::io_service service;
udp::socket sock(service, udp::endpoint(udp::v4(), 5555));
std::array<udp::endpoint, 2> clients;
uint8_t key[2];

void handle_client(std::error_code ec, std::size_t bytes_recvd) {
    if(!ec && bytes_recvd > 0) {
        uint8_t& bat = g_state.bats[key[0]];
        bat = key[1] ? std::min(bat + 4, 75) : std::max(bat - 4, 0);
    }
    sock.async_receive_from(asio::buffer(key, sizeof(uint8_t) * 2), clients[key[0]], handle_client);
}

void handle_send(std::error_code ec, std::size_t bytes_send) {}

void handle_update() {
    auto begin = hclock::now();
    update_game(g_state);
    for(auto& c : clients) {
        sock.async_send_to(asio::buffer((uint8_t*)&g_state, sizeof(gamestate)), c, handle_send);
    }
    std::this_thread::sleep_for(std::chrono::milliseconds(25) - (hclock::now() - begin));
    service.post(handle_update);
}

int main() {
    for(auto& c : clients) {
        sock.receive_from(asio::buffer(key, sizeof(uint8_t) * 2), c);
        sock.send_to(asio::buffer((uint8_t*)&g_state, sizeof(gamestate)), c);
        sock.async_receive_from(asio::buffer(key, sizeof(uint8_t) * 2), c, handle_client);
    }
    service.post(handle_update);
    service.run();
}
