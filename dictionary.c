// Implements a dictionary's functionality

#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>
#include <cs50.h>
#include <ctype.h>

#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// Number of buckets in hash table
const unsigned int N = 25;

// Hash table
node *table[N];

//word counter
int words = 0;

// Returns true if word is in dictionary else false
bool check(const char *word)
{
    //make temporary node
    node *checker = malloc(sizeof(node));
    if (checker == NULL)
    {
        return 1;
    }

    int hashed = hash(word);

    checker = table[hashed];

    while (checker != NULL)
    {
        if (strcasecmp(checker->word, word) == 0)
        {
            return true;
        }
        checker = checker->next;
    }
    return false;
}

// Hashes word to a number, coded with example from CS50 Study, thanks for that!!
unsigned int hash(const char *word)
{

    // initialize index to 0
    int temp = 0;

    // sum ascii values
    for (int i = 0; word[i] != '\0'; i++)
    {
        // search for lower cases words
        temp += tolower(word[i]);
    }
    //change size to fit to hashtable
    return temp % N;
}


// Loads dictionary into memory, returning true if successful else false
bool load(const char *dictionary)
{
    //open file and check if successfull
    FILE *d = fopen(dictionary, "r");
    if (d == NULL)
    {
        printf("can't load dictionary\n");
        return 1;

    }

    //temporary array
    char temp[LENGTH + 1];

    //scan until end of file
    while (fscanf(d, "%s\n", temp) != EOF)
    {
        //make new node
        node *n = malloc(sizeof(node));
        if (n == NULL)
        {
            return 1;
        }
        //copy temp word to node
        strcpy(n->word, temp);

        //hash the word
        int hashed = hash(temp);

        //insert into note depending on if existing or not
        if (table[hashed] == NULL)
        {
            table[hashed] = n;
            n->next = NULL;
        }

        // if belongs in middle or end
        else
        {
            n->next = table[hashed];
            table[hashed] = n;
        }
        //count words
        words++;
    }
    fclose(d);
    return true;
}

// Returns number of words in dictionary if loaded else 0 if not yet loaded
unsigned int size(void)
{
    return words;
}

// Unloads dictionary from memory, returning true if successful else false
bool unload(void)
{
    for (int i = 0; i < N; i++)
    {
        // start cursor
        node *cursor;

        // place the cursor
        cursor = table[i];

        while (cursor)
        {
            node* tmp = cursor;
            cursor = cursor->next;
            free(tmp);
        }

        // clean the hashtable
        table[i] = NULL;
    }
    return true;
}
