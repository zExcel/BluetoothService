#include <iostream>
#include <stdlib.h>
#include <string>
#include <time.h>
#include <wiringPi.h>

#define LED 2

void changeLampStatus(int displayValue) { digitalWrite(LED, displayValue); }

int main(int argc, char *argv[]) {

  wiringPiSetup();
  pinMode(LED, OUTPUT);

  srand(time(NULL));

  if (argc != 2) {
    std::cout
        << "Program requires a lamp status. 1 to turn it on, 0 to turn it off."
        << std::endl;
    return -1;
  }

  int lampStatus = std::stoi(argv[1]);
  if (lampStatus == 1) {
    std::cout << "Turning the lamp on" << std::endl;
    changeLampStatus(HIGH);
  } else {
    std::cout << "Turning the lamp off" << std::endl;
    changeLampStatus(LOW);
  }

  return 0;
}
