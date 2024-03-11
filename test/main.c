#include <stdio.h>
#include <stdlib.h>
#include "huffman.h"

int main(){
        // Ask user for input
        char filename[100]; // Assume file name won't be > 100
        printf("Enter File Name to read: \n");
        scanf("%s", filename);

        // Open file
    FILE* file = fopen(filename, "r");
    
    huffmanEncode(file);

    fclose(file);

    return 0;
    
}
