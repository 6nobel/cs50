#include <cs50.h>
#include <stdio.h>
#include <math.h>

float d;
int c;
int coins;


int main(void)
{
    do
    {
     d = get_float("Change owed: ");
     }
    while (d <= 0.01);

    c = round(d*100);

    coins = 0;

      while (c-25 >= 0)
    {
        c = c -25;
        coins++;
    }

     while (c-10 >= 0)
    {
        c = c -10;
        coins++;
    }

       while (c-5 >= 0)
    {
        c = c -5;
        coins++;
    }

       while (c-1 >= 0)
    {
        c = c -1;
        coins++;
    }
    printf("%i\n", coins);
}
