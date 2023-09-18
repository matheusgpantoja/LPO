#include <FL/Fl.H>
#include <FL/Fl_Window.H>
#include <FL/Fl_Gl_Window.H>
#include <FL/gl.h>
#include <sstream>
#include <cstdlib>
#include <ctime>
#include <cmath>

struct Object {
    float x, y, size;
    int weight, value;
    int shape; // 0 = quadrado, 1 = círculo, 2 = triângulo
    bool collected = false;
};

Object objects[10];
float player_x = 0.0f, player_y = 0.0f;
float currentWeight = 0.0f;
float currentValue = 0.0f; // Novo: valor atual na mochila
const float maxWeight = 50.0f;

bool checkOverlap(Object a, Object b, float minDistance) {
    float distance = std::sqrt(std::pow(a.x - b.x, 2) + std::pow(a.y - b.y, 2));
    return distance < minDistance;
}

bool checkCollision(float px, float py, float ox, float oy, float osize) {
    return px < ox + osize &&
           px + 0.1f > ox &&
           py < oy + osize &&
           py + 0.2f > oy;
}

class MyGlWindow : public Fl_Gl_Window {
public:
    float totalValue = 0.0f; // Novo: Valor total dos itens coletados

    MyGlWindow(int X, int Y, int W, int H, const char *L = 0) : Fl_Gl_Window(X, Y, W, H, L) {
    }

    void draw() {
        if (!valid()) {
            valid(1);
            glLoadIdentity();
            glOrtho(-1.5, 1.5, -1.5, 1.5, -1, 1);
        }
        glClear(GL_COLOR_BUFFER_BIT);

        // Draw objects
        for (int i = 0; i < 10; ++i) {
            if (!objects[i].collected) {
                drawObject(objects[i], i);
            }
        }

        // Draw object information
        for (int i = 0; i < 10; ++i) {
            std::stringstream ssInfo;
            ssInfo << "Id" << i + 1 << ": Peso->" << objects[i].weight << " ; R$->" << objects[i].value;
            glColor3f(1.0, 1.0, 1.0);
            gl_font(FL_HELVETICA, 12);
            gl_draw(ssInfo.str().c_str(), -1.45f, 1.4f - i * 0.1f);
        }

        // Novo: Draw backpack information
        std::stringstream ssBackpack;
        ssBackpack << "Peso: " << currentWeight << "/" << maxWeight << " (" << (currentWeight / maxWeight) * 100 << "%)";
        ssBackpack << " ; R$->" << totalValue;
        glColor3f(1.0, 1.0, 1.0);
       	gl_font(FL_HELVETICA, 12);
        gl_draw(ssBackpack.str().c_str(), -1.4f, -1.4f);

        // Draw character
        // Body (rectangle)
        glColor3f(0.0f, 0.0f, 1.0f);
        glBegin(GL_QUADS);
        glVertex2f(player_x, player_y);
        glVertex2f(player_x + 0.1f, player_y);
        glVertex2f(player_x + 0.1f, player_y + 0.2f);
        glVertex2f(player_x, player_y + 0.2f);
        glEnd();

        // Head (circle)
        glColor3f(1.0f, 1.0f, 1.0f);
        glBegin(GL_TRIANGLE_FAN);
        glVertex2f(player_x + 0.05f, player_y + 0.25f);
        for (int i = 0; i <= 360; i += 10) {
            float theta = i * 3.14159 / 180;
            glVertex2f(player_x + 0.05f + std::cos(theta) * 0.05, player_y + 0.25f + std::sin(theta) * 0.05);
        }
        glEnd();

        // Arms (rectangles)
        glColor3f(1.0f, 0.0f, 0.0f);
        glBegin(GL_QUADS);
        glVertex2f(player_x - 0.05f, player_y + 0.15f);
        glVertex2f(player_x, player_y + 0.15f);
        glVertex2f(player_x, player_y + 0.05f);
        glVertex2f(player_x - 0.05f, player_y + 0.05f);
        glEnd();

        // Other arm
        glBegin(GL_QUADS);
        glVertex2f(player_x + 0.1f, player_y + 0.15f);
        glVertex2f(player_x + 0.15f, player_y + 0.15f);
        glVertex2f(player_x + 0.15f, player_y + 0.05f);
        glVertex2f(player_x + 0.1f, player_y + 0.05f);
        glEnd();

        // Legs (rectangles)
        glColor3f(0.0f, 1.0f, 0.0f);
        glBegin(GL_QUADS);
        glVertex2f(player_x, player_y);
        glVertex2f(player_x + 0.025f, player_y);
        glVertex2f(player_x + 0.025f, player_y - 0.1f);
        glVertex2f(player_x, player_y - 0.1f);
        glEnd();

        glBegin(GL_QUADS);
        glVertex2f(player_x + 0.075f, player_y);
        glVertex2f(player_x + 0.1f, player_y);
        glVertex2f(player_x + 0.1f, player_y - 0.1f);
        glVertex2f(player_x + 0.075f, player_y - 0.1f);
        glEnd();

        // Check for collisions and collect objects
        for (int i = 0; i < 10; ++i) {
            if (!objects[i].collected && checkCollision(player_x, player_y, objects[i].x, objects[i].y, objects[i].size)) {
                if (currentWeight + objects[i].weight <= maxWeight) {
                    currentWeight += objects[i].weight;
                    totalValue += objects[i].value; // Novo: Atualizar o valor total
                    objects[i].collected = true;
                }
            }
        }
    }

    // ... (o resto do seu código para o método drawObject)

    void drawObject(Object obj, int index) {
        glColor3f((index + 1) % 3 / 2.0, (index + 2) % 3 / 2.0, (index + 3) % 3 / 2.0);
        glPushMatrix();
        glTranslatef(obj.x, obj.y, 0);
        glScalef(obj.size, obj.size, 1);
        if (obj.shape == 0) {
            glBegin(GL_QUADS);
            glVertex2f(-0.5, -0.5);
            glVertex2f(0.5, -0.5);
            glVertex2f(0.5, 0.5);
            glVertex2f(-0.5, 0.5);
            glEnd();
        } else if (obj.shape == 1) {
            glBegin(GL_TRIANGLE_FAN);
            glVertex2f(0, 0);
            for (int i = 0; i <= 360; i += 10) {
                float theta = i * 3.14159 / 180;
                glVertex2f(std::cos(theta) * 0.5, std::sin(theta) * 0.5);
            }
            glEnd();
        } else if (obj.shape == 2) {
            glBegin(GL_TRIANGLES);
            glVertex2f(-0.5, -0.5);
            glVertex2f(0.5, -0.5);
            glVertex2f(0, 0.5);
            glEnd();
        }
        glPopMatrix();

        // Draw ID below the object
        std::stringstream ssID;
        ssID << "Id" << index + 1;
        glColor3f(1.0, 1.0, 1.0); // White color for the text
        gl_font(FL_HELVETICA, 12); // Set the font and size
        gl_draw(ssID.str().c_str(), static_cast<float>(obj.x + 0.02), static_cast<float>(obj.y - 0.08)); // Draw the text slightly offset from the object
    }
};
int main(int argc, char **argv) {
    Fl_Window win(800, 600, "Knapsack Game");
    MyGlWindow mygl(10, 10, 780, 580);

    std::srand(std::time(0));

    // Initialize objects
    for (int i = 0; i < 10; ++i) {
        bool overlap;
        do {
            overlap = false;
            objects[i].x = std::rand() % 200 / 100.0 - 1.0;
            objects[i].y = std::rand() % 200 / 100.0 - 1.0;
            for (int j = 0; j < i; ++j) {
                if (checkOverlap(objects[i], objects[j], 0.2)) {
                    overlap = true;
                    break;
                }
            }
        } while (overlap);

        objects[i].size = 0.05 + float(i) / 100.0;
        objects[i].weight = (i + 1) * 2 + std::rand() % 5;
        objects[i].value = std::rand() % 100 + 10;

        if (i < 4) {
            objects[i].shape = 0;
        } else if (i < 7) {
            objects[i].shape = 1;
        } else {
            objects[i].shape = 2;
        }
    }

    win.end();
    win.show(argc, argv);

    float totalValue = 0.0f; // Novo: Total value in the backpack

    while (Fl::check()) {
        // Move character with keys
        if (Fl::event_key('w')) player_y += 0.01f;
        if (Fl::event_key('s')) player_y -= 0.01f;
        if (Fl::event_key('a')) player_x -= 0.01f;
        if (Fl::event_key('d')) player_x += 0.01f;

        // Novo: Update total value in the backpack
        totalValue = 0.0f;
        for (int i = 0; i < 10; ++i) {
            if (objects[i].collected) {
                totalValue += objects[i].value;
            }
        }

        mygl.redraw();
    }

    return 0;
}

