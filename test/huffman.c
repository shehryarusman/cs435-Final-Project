/*
   @file huffman.c
   @author Zach Dowhower <zd89@drexel.edu> 
   @date February 29, 2024
   @section DESCRIPTION
   TBD
   */

#include "huffman.h"
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>

// Type definitions for File
typedef struct HuffmanNode HuffmanNode;
typedef struct Heap Heap;
typedef struct HuffmanData HuffmanData;

typedef struct {
	int chara; 
	float freq; 
	char code[128]; 
} CharCode;

void generateHuffmanCodes(HuffmanNode* root, char* code, int depth, CharCode charCodes[], int* index) {
	if (!root) return;

	if (root->left == NULL && root->right == NULL) {
		charCodes[*index].chara = root->chara;
		charCodes[*index].freq = root->freq;
		strncpy(charCodes[*index].code, code, depth);
		charCodes[*index].code[depth] = '\0';
		(*index)++;
		return;
	}

	if (root->left) {
		code[depth] = '0';
		generateHuffmanCodes(root->left, code, depth + 1, charCodes, index);
	}

	if (root->right) {
		code[depth] = '1';
		generateHuffmanCodes(root->right, code, depth + 1, charCodes, index);
	}
}

void sortAndPrintCharCodes(CharCode charCodes[], int size) {
	qsort(charCodes, size, sizeof(CharCode), compareNodes);
	printf("| ASCII | Percent  | Code |\n");
	printf("|-------|----------|------|\n");
	for (int i = 0; i < size; i++) {
		printf("| %5d | %8.5f | %s |\n", charCodes[i].chara, charCodes[i].freq, charCodes[i].code);
	}
}

Heap* makenull(int capacity){
	Heap* newHeap = (Heap*)malloc(sizeof(Heap));
	newHeap->data = (HuffmanNode**)malloc(capacity * sizeof(HuffmanNode*));
	newHeap->maxSize = capacity;
	newHeap->currentSize = 0;
	return newHeap;

}

// Free all memory used by heap
void deleteHeap(Heap* myHeap){
	if (myHeap != NULL){
		free(myHeap->data);
		free(myHeap);
	}
}

// Check if empty
bool empty(Heap* myHeap){
	return myHeap->currentSize == 0;
}

// Create new Huffman Node
HuffmanNode* newHuffmanNode(int chara, float freq){
	HuffmanNode* newNode = (HuffmanNode*)malloc(sizeof(HuffmanNode));
	newNode->chara = chara;
	newNode->freq = freq;
	newNode->left = NULL; 
	newNode->right = NULL;
	return newNode;
}

// Delete min node from Heap
HuffmanNode* removemin(Heap* myHeap){
	if (myHeap->currentSize == 0){
		return NULL;
	}

	HuffmanNode* min = myHeap->data[0];
	myHeap->currentSize--;
	myHeap->data[0] = myHeap->data[myHeap->currentSize];
	downheap(myHeap, 0);
	return min;
}

// Downheap starting at node at index i
void downheap(Heap* myHeap, int i){
	int leftIndex = leftChild(i);
	int rightIndex = rightChild(i);
	int minIndex = i;

	if (leftIndex < myHeap->currentSize && myHeap->data[leftIndex]->freq < myHeap->data[minIndex]->freq){
		minIndex = leftIndex;
	}
	if (rightIndex < myHeap->currentSize && myHeap->data[rightIndex]->freq < myHeap->data[minIndex]->freq){
		minIndex = rightIndex;
	}

	if (minIndex != i){
		swap(&myHeap->data[i], &myHeap->data[minIndex]);
		downheap(myHeap, minIndex);
	}
}

// Insert node into heap
void insert(HuffmanNode* node, Heap* myHeap){
	if (myHeap->currentSize < myHeap->maxSize){
		int i = myHeap->currentSize++;
		myHeap->data[i] = node;
		upheap(myHeap, i);
	}
}

// Upheap starting at node indexed to i
void upheap(Heap* myHeap, int i){
	int parentIndex = parent(i);

	while (i > 0 && myHeap->data[parentIndex]->freq > myHeap->data[i]->freq){
		swap(&myHeap->data[i], &myHeap->data[parentIndex]);
		i = parentIndex;
		parentIndex = parent(i);
	}
}

// Swap 2 Huffman Nodes
void swap(HuffmanNode** a, HuffmanNode** b){
	HuffmanNode* temp = *a;
	*a = *b;
	*b = temp;
}

// Get parent index of node
int parent(int n){
	return (n - 1) / 2;
}

// Get index of left child in node
int leftChild(int n){
	return (2 * n) + 1;
}

// and Get Index of right child in node
int rightChild(int n){
	return (2 * n) + 2;
}

void huffmanEncode(FILE* file) {
	// Count frequencies of characters
	float count[128] = {0}; // Initalize to 0
	int total = 0;
	int c;

	while ((c = fgetc(file)) != EOF) {
		// Ignore chars outside ASCII
		if (c >= 0 && c < 128) {
			count[c]++;
			total++;
		}
	}
	fclose(file);

	// Create Heap and Insert Nodes
	Heap* heap = makenull(128);
	for (int i = 0; i < 128; i++) {
		if (count[i] > 0) {
			HuffmanNode* node = newHuffmanNode(i, count[i] / total);
			insert(node, heap);
		}
	}

	// Construct Huffman Tree
	while (heap->currentSize > 1) {
		HuffmanNode* left = removemin(heap);
		HuffmanNode* right = removemin(heap);
		HuffmanNode* merged = newHuffmanNode(-1, left->freq + right->freq);
		merged->left = left;
		merged->right = right;
		insert(merged, heap);
	}

	// Generate codes
	CharCode charCodes[128];
	int charCodeIndex = 0;
	char code[128];
	generateHuffmanCodes(heap->data[0], code, 0, charCodes, &charCodeIndex);

	// Sort and print codes
	sortAndPrintCharCodes(charCodes, charCodeIndex);

	// Free memory
	deleteHeap(heap);
}

int compareNodes(const void* a, const void* b){
	CharCode* code1 = (CharCode*)a;
	CharCode* code2 = (CharCode*)b;
	return code1->chara - code2->chara;
}

