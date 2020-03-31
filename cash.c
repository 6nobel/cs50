#include <cs50.h>
#include <stdio.h>
#include <math.h>

float d;
int c;
int coins;


int main(void)
{
// prompt user to insert cash  
    do
    {
        d = get_float("Change owed: ");
    }
    while (d <= 0.001);

// translating dollars to cents
    c = round(d * 100);
// introducing variable coins
    coins = 0;

// quarters
    while (c - 25 >= 0)
    {
        c = c - 25;
        coins++;
    }
// dimes
    while (c - 10 >= 0)
    {
        c = c - 10;
        coins++;
    }
// nickels
    while (c - 5 >= 0)
    {
        c = c - 5;
        coins++;
    }
// cents
    while (c - 1 >= 0)
    {
        c = c - 1;
        coins++;
    }
// printout of results
    printf("%i\n", coins);
}
