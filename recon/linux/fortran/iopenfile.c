/*
 *  iopenfile.c
 *  cwtest
 *
 *  Created by crispin williams on 07/07/2006.
 *  Copyright 2006 barbarian inc. All rights reserved.
 *
 */
 


#include <stdio.h>
#include <stdlib.h>
 
#include <string.h>
//#include "decode.h"

   struct filename {
   FILE * pFile;
                  };
 struct filename my_struct;

 static int time_data[192],width_data[192],iev_number[2];
  int n_channel_1,extended_time_tag_1;
  int n_channel_2,extended_time_tag_2;
  int i_decode_error,tdc_flag_1,tdc_flag_2;
  int debug;

  int iarray[2];
  int len_head,nwords;


int iopenfile_(char *filename, unsigned int length_arg)
{
  
//  printf(" length of character string %d \n", length_arg);
  filename[length_arg]= 0;
   
//  printf(" Opening file");
//  printf(filename);
//  printf(" \n");
  my_struct.pFile = fopen (filename, "rb" );
  
  if (my_struct.pFile==NULL){
    printf(" error opening file");
    exit (1);
	}

//now read two words that Roman put at the start of the file - for checking the endian etc

	len_head = 2;
    nwords=fread(iarray,4,len_head,my_struct.pFile);
	if (iarray[0] != 1162167584)
	{ 
	printf("error at start of input file");
	exit (1);
	}
     
  return 0;
}
 int irewind_()
 {
 rewind(my_struct.pFile);
 //now read two words that Roman put at the start of the file - for checking the endian etc

	len_head = 2;
    nwords=fread(iarray,4,len_head,my_struct.pFile);
	if (iarray[0] != 1162167584)
	{ 
	printf("error at start of input file");
	exit (1);
	}

 
 }
 

 
