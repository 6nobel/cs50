#include "helpers.h"
#include <math.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < (height); i++)
    {
        for (int j = 0; j < (width); j++)
        {
            //get avarage
            int k = round(( (float) image[i][j].rgbtRed + (float) image[i][j].rgbtGreen + (float) image[i][j].rgbtBlue) / 3);

            //assign k to all values
            image[i][j].rgbtRed = k;
            image[i][j].rgbtGreen = k;
            image[i][j].rgbtBlue = k;

        }
    }
}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < (height); i++)
    {
        for (int j = 0; j < (width); j++)
        {
            //helper variables
            int or = image[i][j].rgbtRed;
            int og = image[i][j].rgbtGreen;
            int ob = image[i][j].rgbtBlue;

            //change Red
            float orrtemp = (float) or * 0.393;
            float ogrtemp = (float) og * 0.769;
            float obrtemp = (float) ob * 0.189;

            int redtemp = round(orrtemp + ogrtemp + obrtemp);

            if (redtemp > 255)
            {
                image[i][j].rgbtRed = 255;
            }
            else
            image[i][j].rgbtRed = redtemp;

            //change green
            float orgtemp = (float) or * 0.349;
            float oggtemp = (float) og * 0.686;
            float obgtemp = (float) ob * 0.168;

            int greentemp = round (orgtemp + oggtemp + obgtemp);

            if (greentemp > 255)
            {
                image[i][j].rgbtRed = 255;
            }
            else
            image[i][j].rgbtGreen = greentemp;


            // change blue
            float orbtemp = (float) or * 0.272;
            float ogbtemp = (float) og * 0.534;
            float obbtemp = (float) ob * 0.131;

            int bluetemp = round( orbtemp + ogbtemp + obbtemp);

            if (bluetemp > 255)
            {
                image[i][j].rgbtRed = 255;
            }
            else
            image[i][j].rgbtBlue = bluetemp;

        }
    }
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    return;
}
