#pragma once
#include <cstdint>
#include <iostream>
#include <array>
#include <algorithm>
#include <SFML/Graphics.hpp>

// display constants
const uint32_t WIDTH = 800, HEIGHT = 400;
const uint32_t BALL_R = WIDTH * 0.01f;
const uint32_t BAT_W = WIDTH * 0.03f, BAT_H = HEIGHT / 4;
const uint32_t BAT_HH = BAT_H / 2;

// game win state
enum win_state : uint8_t {
    None = 0,
    Player1,
    Player2
};

// global game state
struct gamestate {
    uint8_t bats[2];
    uint8_t scores[2];
    uint8_t ball[2];
    short dir[2];
    win_state win;
};

// shapes for bats/ball
struct drawinfo {
    sf::CircleShape ball = sf::CircleShape(BALL_R);
    std::array<sf::RectangleShape, 2> bats = { 
        sf::RectangleShape{sf::Vector2f(BAT_W, BAT_H)}, 
        sf::RectangleShape{sf::Vector2f(BAT_W, BAT_H)} 
    };
    std::array<sf::Shape*, 3> shapes = { &bats[0], &bats[1], &ball };

    drawinfo() {
        for(auto* shape : shapes) {
            shape->setFillColor(sf::Color::Red);
        }
    }
};

// check if ball hits a bat
bool bat_collide(const gamestate& state, uint8_t b) {
    const uint8_t& bx = state.ball[0], by = state.ball[1];
    const uint8_t& height = state.bats[b];
    const uint8_t wbound = (100 * b) + (b ? -3 : 3);
    const uint8_t hbound = height + 25;

    return ((by >= height) && (by <= hbound)) && (b ? (bx > wbound) : (bx < wbound));
}

// game rules/physics
void update_game(gamestate& state) {
    // bat check
    for(uint8_t i = 0; i < 2; i++) {
        if(bat_collide(state, i))
            state.dir[0] *= -1;
    }

    // screen check
    for(uint8_t i = 0; i < 2; i++) {
        // change direction
        if(state.ball[i] == 0 || state.ball[i] == 100) {
            state.dir[i] *= -1;
            // score check
            if(!i) {
               state.ball[i] ? state.scores[0]++ : state.scores[1]++;
               state.ball[0] = state.ball[1] = 50;
               std::cout << (uint16_t)state.scores[0] << ' ' << (uint16_t)state.scores[1] << '\n';
            }
        }

        // update position
        state.ball[i] += state.dir[i];
    }
}

// update shapes on screen
void update_display(const gamestate& state, drawinfo& info) {
    info.bats[0].setPosition(0, (HEIGHT * (state.bats[0]/100.0f)));
    info.bats[1].setPosition(WIDTH - BAT_W, (HEIGHT * (state.bats[1]/100.0f)));
    info.ball.setPosition((WIDTH - BALL_R) * (state.ball[0]/100.0f), (HEIGHT - BALL_R) * (state.ball[1]/100.0f));
}

// draw game
void draw(sf::RenderWindow& win, drawinfo& info) {
    win.clear(sf::Color::Black);
    for(auto* shape : info.shapes) {
        win.draw(*shape);
    }
    win.display();
}

// fake source of gamestates
gamestate recv_state() {
    static gamestate g {
        {75, 75}, {0, 0}, {50, 50}, {1, 1},
        win_state::None 
    };

    update_game(g);
    return g;
}
