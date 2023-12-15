#include "mbed.h"
void toBinary(unsigned char val, char *str) {
    for (int i = 7; i >= 0; i--) {
        str[i] = (val % 2) ? '1' : '0';
        val /= 2;
    }
    str[8] = '\0'; // Null-terminate the string
}

int main() {
    int i;
    unsigned char *ram_buffer = (unsigned char *)0x20003000;
    char binary[9]; // 8 bits plus null terminator
    // Array to store binary data
    char binaryArray[64][9];
    // Read values from memory, convert to binary, and store in the array
    for (i = 0; i < 64; i++) {
        toBinary(ram_buffer[i], binary);
        printf("%s ", binary);
        // Copy the binary representation to the array
        strcpy(binaryArray[i], binary);
    }
    // Print newlines to console
    printf("\r\n");
    // Now, the binary data is stored in the binaryArray.
    // Example: Printing the binary data from the array
    for (i = 0; i < 64; i++) {
        printf("%s ", binaryArray[i]);
    }
    // Add a delay before resetting the board
    ThisThread::sleep_for(5);
    // Reset the board manually
    printf("\r\nReset the board now.\r\n");
    ThisThread::sleep_for(5); 
   
    printf("Turn off the board now.\r\n");

   
    while (1) {
       
    return 0;
}