#include <iostream>
#include <cstdlib>
#include <ctime>
#include <limits>

class AnimalUtil {
public:
    enum Animal { DOG = 1, CAT, BIRD, FISH };

    static const char* toStr(Animal a) {

        switch (a) {
            case DOG:  return "Dog";
            case CAT:  return "Cat";
            case BIRD: return "Bird";
            case FISH: return "Fish";
            default:   return "Unknown";
        }
    }
};

const std::string staticWelcomeMessage = "Welcome to the Animal Guesser!";

int main() {
    std::srand(static_cast<unsigned>(std::time(nullptr)));

    std::cout << staticWelcomeMessage << "\n";

    // Print out the address of staticWelcomeMessage for question #4
    std::cout << "Address of staticWelcomeMessage: " << &staticWelcomeMessage << "\n";

    std::cout << "Guess the Animal! (1: Dog, 2: Cat, 3: Bird, 4: Fish)\n";
    std::cout << "Enter 0 to quit.\n";

    AnimalUtil::Animal* mysteryAnimal;

    // Error #1 - see question #1
    //std::cout << "The animal is initialized to: " << AnimalUtil::toStr(*mysteryAnimal) << "\n";
    
    // Error #2 - see question #2
    //mysteryAnimal = nullptr;

    //std::cout << "The animal should initally be nothing: " << AnimalUtil::toStr(*mysteryAnimal) << "\n";
    
    // Error #3 - Figure it out.
    while (true) {
        mysteryAnimal =
            new AnimalUtil::Animal(static_cast<AnimalUtil::Animal>(1 + std::rand() % 4));

        std::cout << "\nYour guess: ";
        int guess = -1;
        if (!(std::cin >> guess)) {
            std::cin.clear();
            std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
            std::cout << "Invalid input; try again.\n";
            continue;
        }
        if (guess == 0) {
            std::cout << "Bye!\n";
            delete mysteryAnimal;    // Free memory before exiting
            break;
        }

        // Validation check for input (1,2,3,4)
        if (guess < 1 || guess > 4) {
            std::cout << "Invalid input; Please input 1,2,3, or 4.\n";
            delete mysteryAnimal;    // Free memory before next loop iteration
            continue;
        }

        if (*mysteryAnimal == static_cast<AnimalUtil::Animal>(guess)) {
            std::cout << "Correct! It was " << AnimalUtil::toStr(*mysteryAnimal) << "\n";
        } else {
            std::cout << "Wrong! It was " << AnimalUtil::toStr(*mysteryAnimal) << "\n";
        }
        // Print outs for question #3
        //- The address of the mysteryAnimal pointer
        //- The address where the pointer is pointing
        //- The value located at the address where the pointer is pointing.
        std::cout << "The animal was stored at address: " << &mysteryAnimal << "\n";
        std::cout << "The pointer is pointing to address: " << mysteryAnimal << "\n";
        std::cout << "The value at that address is: " << AnimalUtil::toStr(*mysteryAnimal) << "\n";

        // Clean up allocated memory at mysteryAnimal before next loop iteration
        delete mysteryAnimal; 

    }
    return 0;
}
