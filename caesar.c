#include <stdio.h>
#include <cs50.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

// Program that shifts plaintext as per ceasars cipher with a key (int) that is entered as command line argument to a cipher text

bool confirm_only_numbers(string input);


int main(int argc, string argv[])
{
    if (argc < 2 || argc > 2 || confirm_only_numbers(argv[1]) < 1)
    {
        printf("usage ./ceasar key\n");
        return 1;
    }
    //convert key string to number
    int k = atoi(argv[1]);
    //promt plaintext from user
    string text = get_string("plaintext:");
    //printout empty ciphertext line
    printf("ciphertext:");
    // main conversation of each character
    for (int l = 0, n = strlen(text); l < n; l++)
    {
        //checks if letters, if not does nothing
        if (isalpha(text[l]) > 0)
        {
            //checks is upper case, changes formula accordingly
            if (isupper(text[l]) > 0)
            {
                text[l]  = (text[l]  - 64 + k) % 26 + 64;
            }
            else
            {
                text[l]  = (text[l]  - 96 + k) % 26 + 96;
            }

        }
        //prints each letters
        printf("%c", text[l]);
    }
    printf("\n");
}
//function to confirm only numbers
bool confirm_only_numbers(string input)
{
    bool j;
    for (int i = 0, n = strlen(input); i < n; i++)
    {
        if (input[i] >= '0' && input[i] <= '9')
        {
            j = true;
        }
        else
        {
            j = false;
        }
    }

    return j;
}