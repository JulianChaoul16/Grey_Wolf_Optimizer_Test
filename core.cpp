#include <iostream>
#include <vector>
struct Agent {
    float x, y; // Position in 3D space
    float vx, vy; // Velocity components
    Agent(float x, float y,  float vx, float vy)
        : x(x), y(y), vx(vx), vy(vy) {}
};

struct Hive {
    std::vector<Agent> agents;

    void addAgent(float x, float y, float vx, float vy) {
        agents.emplace_back(x, y, vx, vy);
    }

    void updatePositions(float dt) {
        for (auto& agent : agents) {
            agent.x += agent.vx * dt;
            agent.y += agent.vy * dt;
        }
    }

    void printPositions() const {
        for (const auto& agent : agents) {
            std::cout << "Agent Position: (" << agent.x << ", " << agent.y << ")\n";
        }
    }
};