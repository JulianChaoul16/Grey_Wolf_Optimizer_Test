#include <GLFW/glfw3.h>
#include <glad/gl.h>

int main() {
    if(!glfwInit()) {
        return -1; // Initialization failed
    }

    GLFWwindow* window = glfwCreateWindow(800, 600, "OpenGL Window", nullptr, nullptr);
    if (!window) {
        glfwTerminate();
        return -1; // Window creation failed
    }
    glfwMakeContextCurrent(window);
}