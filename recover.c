#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[])
{
    //check if 1 command line argument
    if (argc != 2)
    {
        printf("Usage: ./recover image\n");
        return 1;
    }

    //open file from command line argument
    FILE *f = fopen(argv[1], "r");
    if (!f)
    {
        return 1;
    }

    //create buffer
    unsigned char buffer[512];

    int fileopen = 0;
    int filenumber = 0;
    char filename[8];
    FILE *img = NULL;


    //read file
    while(fread(buffer, 512, 1, f) == 1)
    {
        //check if jpeg
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0)
        {   

            //check if there is an open file, if not open a new
            if (fileopen == 0)
            {
                sprintf(filename, "%03i.jpg", filenumber);
                img = fopen(filename, "a");
                fileopen++;
                filenumber++;
                //write buffer in file img
                fwrite(buffer, 512, 1, img);
            }
            else
            {   fclose (img);
                sprintf(filename, "%03i.jpg", filenumber);
                img = fopen(filename, "a");
                fileopen++;
                filenumber++;

                //write buffer in file img
                fwrite(buffer, 512, 1, img);
            } 
        
        }
        
    //write buffer in file img
    if (fileopen == 0)
    {
        continue;
    }
    else 
    {
        fwrite(buffer, 512, 1, img);
    }
    }

//close file
fclose(f);
return 0;
}
