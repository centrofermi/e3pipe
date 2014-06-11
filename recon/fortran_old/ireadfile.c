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
 
 
 
int iread_file(int * nwords, int * ntype, int  idata[],int * ierror)
{
  
  int len_block,len_head,nread,i,j,k,id_caen,leading,debug;
  int iarray [8000],data_flag[200];
  int nsec,second,day,year;
  int tdc_num,event_id,bunch_id,channel_number;
  int tdc_num_tr,event_id_tr,word_count,tdc_num_err,error_flags,extended_time_tag;
  
  
   *ierror = 0;
   debug = 0; 
  	
	// first read one word - this is the length of the next block of data  //
	len_head = 1;
    nread=fread(iarray,4,len_head,my_struct.pFile);
	len_block=iarray[0];
//	printf (" first data word %d number of words read %d \n", len_block,nread);
// check for errors                                                    //
	if (nread != 1)  {
					   *ierror = 3;
					   return 0;
					  }
	
	if(len_block < 1) {
					  *ierror = 1;
					   return 0;
					  }
    else if(len_block > 8000)
                      {
					  *ierror = 2;
					   return 0;
					  }


// now read out a block of data...
        len_block=len_block-1;
        nread =fread(iarray,4,len_block,my_struct.pFile);	
		*ntype = iarray[0];
		*nwords =nread;
//		printf(" read block : length %d  type %d  \n",*nwords,*ntype);
//
// now have block of data - decode it according to type:
//
       if(iarray[0] == 0)
	   
// gps event
	   {

//	   idata[0]=((iarray[2] & 0xFFFF)+((iarray[3] & 0x7FF)*0x10000)*10);  // nanosecs 
	   idata[0]=((iarray[2] & 0xFFFF)+((iarray[3] & 0x7FF)*0x10000))*10;  // nanosecs 
	   idata[1]=(iarray[4] & 0xFFF)*0x20 + ((iarray[3] & 0xF800) >> 11); // seconds in day
	   idata[2]=((iarray[4] & 0xF000) >> 12) + ((iarray[5]& 0x1F) * 0x10); // day in year
	   idata[3]=((iarray[5] & 0x3E0) >> 5) +1996 ; // year
//	   if (debug == 1)
//	    printf(" decode gps event ns %d sec %d day %d year %d \n",idata[0],idata[1],idata[2],idata[3]);
//		printf (" ns  %X %X %X \n",iarray[2],(iarray[3] & 0x7FF),(idata[0]/10 & 0xFFFF));

	   return 0;
	   }
	   
	   if (iarray[0] == 5)
	   {
// Geometry block
	   i=0;
	   while (i < len_block)
	   {
	   idata[i]=iarray[i+1];
	   i=i+1;
	   }
	   return 0;
	   }
	   if (iarray[0] == 6)
	   {
// WAD block
	   i=0;
	   while (i < len_block)
	   {
	   idata[i]=iarray[i+1];
	   i=i+1;
	   }
	   return 0;
	   }
	   
	   if (iarray[0] == 1 || iarray[0] == 2)
	   
// tdc event
	   {
	   j=0;
       i=0;
    while (i <= 199)
       {
     	data_flag[i]=0;
        i=i+1;
       }
	i=1;
	idata[2]=0;
					while (i < len_block){
					if (debug == 1) printf(" iarray[i] %X ",iarray[i]);
					id_caen = iarray[i] & 0xF8000000;
					
					if (id_caen == 0x40000000) {
// Global header //
					                            idata[0] = (iarray[i] & 0x07FFFFE0) >>5;
												if (debug == 1) printf (" event number = %d \n",idata[0]);
												}
					if (id_caen == 0x80000000) {
// Global trailer //
					                            idata[2] = idata[2]+(iarray[i] & 0x1F);
												if (debug == 1) printf (" 5 bit counter = %d %d \n",idata[2],(iarray[i] & 0x1f));
												}
					else if (id_caen == 0x08000000){
// TDC header //

					tdc_num = (iarray[i] & 0x03000000) >> 24;
					event_id = (iarray[i] & 0x00FFF000) >> 12;
					bunch_id = (iarray[i] & 0x00000FFF);
					if (debug == 1) printf (" TDC number = %d event_id = %d  bunch_id = %d \n",tdc_num,event_id,bunch_id);
					                              }
					else if (id_caen == 0) {
// TDC measurement //
// check if leading or trailing edge
                    leading=(iarray[i] & 0x04000000);
					if (leading == 0){
					j=j+1;
					k=(j*3);
					idata[k] = 1+((iarray[i] & 0x03F80000) >> 19);  // channel number - start with channel 1
					data_flag[idata[k]] = k;                    // take note that leading edge has been found					
					idata[k+1]    = (iarray[i] & 0x0007FFFF);   // time value
//					idata[k+2]   = (iarray[i] & 0x0007F000) >> 12; // width
					idata[k+2]   = 0; // width

					if (debug == 1) printf (" channel =  %d  time = %d  width = %d \n",idata[k],idata[k+1],idata[k+2]);
					                  }
					else              {
// trailing edge
               					channel_number= 1+((iarray[i] & 0x03F80000) >> 19); // channel number
								if (data_flag[channel_number] != 0)
								{
								idata[data_flag[channel_number]+2]=(iarray[i]  & 0x0007FFFF) - idata[data_flag[channel_number]+1];
								data_flag[channel_number]=0;
                                }								
								
								
					                  }				  
					                       }
					else if (id_caen == 0x18000000) {
// TDC trailer //
					tdc_num_tr = (iarray[i] & 0x03000000) >> 24;
					event_id_tr    = (iarray[i] & 0x00FFF000) >> 12;
					word_count   = (iarray[i] & 0x00000FFF);
					if (debug == 1) printf (" tdc_num_tr =  %d  event_id = %d  word_count = %d \n",tdc_num_tr,event_id_tr,word_count);
					                       }
					else if (id_caen == 0x20000000) {
// TDC error //
					tdc_num_err = (iarray[i] & 0x03000000) >> 24;
					error_flags    = (iarray[i] & 0x00003FFF);
					if (debug == 1) printf (" tdc_num_err =  %d  error_flags = %X  \n",tdc_num_err,error_flags);

					                       }
					else if (id_caen == 0x88000000) {					   
										   
//	extended time tag //
					extended_time_tag = (iarray[i] & 0x07FFFFFF);
					if (debug == 1) printf ("extended time tag : %d  \n",extended_time_tag);
					idata[2]=extended_time_tag* 0x20+idata[2];
					if (debug == 1) printf ("extended time tag : %d  %d \n",extended_time_tag,idata[2]);

					                       }
										   
					++i;
					}
					idata[1]=j;   // number of hits
	   
	   return 0;
	   }						  						  

  return 0;
}



