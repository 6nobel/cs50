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
            float or = image[i][j].rgbtRed;
            float og = image[i][j].rgbtGreen;
            float ob = image[i][j].rgbtBlue;

            //change Red
            float orrtemp = or * 0.393;
            float ogrtemp = og * 0.769;
            float obrtemp = ob * 0.189;

            int redtemp = round(orrtemp + ogrtemp + obrtemp);

            if (redtemp > 255)
            {
                image[i][j].rgbtRed = 255;
            }
            else
            image[i][j].rgbtRed = redtemp;

            //change green
            float orgtemp = or * 0.349;
            float oggtemp = og * 0.686;
            float obgtemp = ob * 0.168;

            int greentemp = round(orgtemp + oggtemp + obgtemp);

            if (greentemp > 255)
            {
                image[i][j].rgbtRed = 255;
            }
            else
            image[i][j].rgbtGreen = greentemp;


            // change blue
            float orbtemp = or * 0.272;
            float ogbtemp = og * 0.534;
            float obbtemp = ob * 0.131;

            int bluetemp = round(orbtemp + ogbtemp + obbtemp);

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
