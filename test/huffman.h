#ifndef HUFFMAN_H
#define HUFFMAN_H

#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>

typedef struct HuffmanNode HuffmanNode;
typedef struct Heap Heap;
typedef struct HuffmanData HuffmanData;

// Struct definitions for Huffman Nodes and Heap
struct HuffmanNode{
    int chara;
    float freq;
    struct HuffmanNode *left;
    struct HuffmanNode *right;
    char code[128];
};

struct Heap{
    HuffmanNode **data;
    int maxSize;
    int currentSize;
};

struct HuffmanData{
    int chara;
    float freq;
    char* code;
};

//typedef struct HuffmanNode HuffmanNode;
//typedef struct Heap Heap;

// Function Declarations
HuffmanNode* newHuffmanNode(int chara, float freq);
Heap* makeHeap(int capacity);
void swap(HuffmanNode** a, HuffmanNode** b);
int parent(int n);
int leftChild(int n);
int rightChild(int n);
void upheap(Heap* myHeap, int i);
void insert(HuffmanNode* node, Heap* myHeap);
void downheap(Heap* myHeap, int i);
HuffmanNode* removemin(Heap* myHeap);
void huffmanEncode(FILE* file);
void printHuffmanCodes(HuffmanNode* root, char* code);
int compareNodes(const void* a, const void* b);
void sortHuffNodes(HuffmanNode** nodes, int size);

#endif
