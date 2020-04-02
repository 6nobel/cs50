#include <cs50.h>
#include <stdio.h>

long cc;

int main(void)

{
//promt user for input  
    do  
    {
        cc = get_long("Credit card number:");
    }
    while (cc < 1000000000000 && cc > 9999999999999999);

//count digits
    long count = 0;
    long rest = cc;
    while (rest > 0)
    {
        rest = rest / 10;
        count++;
        
    }
  
// get even digits
int d1 = ((cc % 100) / 10*2);
int d2 = ((cc % 10000) / 1000*2);
int d3 = ((cc % 1000000) / 100000*2);
int d4 = ((cc % 100000000) / 10000000*2);
int d5 = ((cc % 10000000000) / 1000000000*2);
int d6 = ((cc % 1000000000000) / 100000000000*2);
int d7 = ((cc % 100000000000000) / 10000000000000*2);
int d8 = ((cc % 10000000000000000) / 1000000000000000*2);

//add individual digits
while (d1 > 9)
        {
            d1 = (d1 - 10 + 1);                
        }
while (d2 > 9)
        {
            d2 = (d2 - 10 + 1);                
        }
while (d3 > 9)
        {
            d3 = (d3 - 10 + 1);                
        }
while (d4 > 9)
        {
            d4 = (d4 - 10 + 1);                
        }
while (d5 > 9)
        {
            d5 = (d5 - 10 + 1);                
        }
while (d6 > 9)
        {
            d6 = (d6 - 10 + 1);                
        }
while (d7 > 9)
        {
            d7 = (d7 - 10 + 1);                
        }
while (d8 > 9)
        {
            d8 = (d8 - 10 + 1);                
        }

//get uneven digits
int d9   = (cc % 10);
int d10  = (cc % 1000) / 100;
int d11  = (cc % 100000) / 10000;
int d12  = (cc % 10000000) / 1000000;
int d13  = (cc % 1000000000) / 100000000;
int d14  = (cc % 100000000000) / 10000000000;
int d15  = (cc % 10000000000000) / 1000000000000;
int d16  = (cc % 1000000000000000) / 100000000000000;

//get checksum
int p1 = d1 + d2 + d3 + d4 + d5 + d6 + d7 + d8 + d9 + d10 + d11 + d12 + d13 + d14 + d15 + d16;

//result
if (p1 % 10 != 0) 
{
    printf("INVALID\n");
}
else if (count == 15 && ((cc % 1000000000000000) / 100000000000000 )==3 && ((((cc % 100000000000000) / 10000000000000) == 4) || (cc % 100000000000000) / 10000000000000 == 7))
{
    printf("AMEX\n");
}


else if (count == 16 && ((cc % 10000000000000000 / 1000000000000000)==5))
{
    printf("MASTERCARD\n");
}
else if ((count == 16 || count == 13) && (((cc % 10000000000000000 / 1000000000000000) == 4) || ((cc % 100000000000000) / 10000000000000) == 4) )
{
    printf("VISA\n");
}
else 
{
    printf("INVALID\n");
}
}
