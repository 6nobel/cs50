#include <stdio.h>
#include <cs50.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

bool confirm_only_numbers(string input);


int main (int argc, string argv[])
{
    if (argc < 2 || argc > 2 || confirm_only_numbers(argv[1]) < 1)
    {
        printf("usage ./ceasar key\n");
        return 1;
    }

    int k = atoi (argv[1]);

    string text = get_string("plaintext:");
    for (int l = 0, n = strlen(text); l < n; l++)
    {

        if (isalpha(text[l] ) > 0)
        {
            if (isupper(text[l] ) > 0)
            {
                text[l]  = (text[l]  - 64 + k) % 26 + 64;
            }
            else
            {
                text[l]  = (text[l]  - 96 + k) % 26 + 96;
            }

        }
        printf("ciphertext:%c\n", text[l] );
        return 0;
    }
}
//function to confirm only numbers
bool confirm_only_numbers(string input)
{
    bool j;
    for (int i = 0, n = strlen(input); i < n; i++)
    {
        if (input[i] > '0' && input[i] <= '9')
        {
            j = true;
        }
        else
        j = false;
    }
    return j;
}