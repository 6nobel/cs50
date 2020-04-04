#include <stdio.h>
#include <cs50.h>
#include <string.h>

int count_letters(string input);
int count_words(string input2);
int count_sentences(string input3);

//prompt input and get output
int main(void)
{
    string text = get_string("Text: ");
    float L = (float) count_letters(text) / (float) count_words(text) * 100;
    float S = (float) count_sentences(text) / (float) count_words(text) * 100;
    float index = 0.0588 * L - 0.296 * S - 15.8;

    if (index > 16)
    {
      printf("Grade 16+\n");
    }
    else if (index < 1)
    {
        printf("Before Grade 1\n");
    }
    else
    {
    printf("Grade %.0f\n", index);
    }
}

//function to count letters
int count_letters(string input)
{
    int letters = 0;
        for (int i = 0, n = strlen(input) ; i < n ; i++)
    {
        if ((input[i] >= 'a' && input[i] <= 'z') || (input[i] >= 'A' && input[i] <= 'Z'))
        {
          letters++;
        }

    }
    return (int) letters;
}

//function to count words
int count_words(string input2)
{
    int words = 1;
        for (int i = 0, n = strlen(input2) ; i < n ; i++)
    {
        if (input2[i] == ' ')
        {
          words++;
        }

    }
    return (int) words;
}

//function to count sentences
int count_sentences(string input3)
{
    int sentences = 0;
        for (int i = 0, n = strlen(input3) ; i < n ; i++)
    {
        if (input3[i] =='.')
        {
          sentences++;
        }
        else if (input3[i] =='?')
        {
          sentences++;
        }
        else if (input3[i] =='!')
        {
          sentences++;
        }
    }
    return (int) sentences;
}