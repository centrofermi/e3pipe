      program EEE_V15
c
c  Analysis of EEE events
c  Tracking by Franco Riggi
c  Decoding of raw data by Crispin Williams
c
c
      real*8 data1,t0,tns,time_ev,day,sec,tns1,tns2,t_delay
	  real*8 tstdc,ananosec,test
	  
	  real*8 usec
	  
	  real*8 val1, val2
	  real*8 mytstdc
	  
	  integer(kind=8) imytstdc, iusec, inanosec, itest, iwindow_start
	  real*8 mytD
	  integer mytime
	  
      integer year
	  integer iarray(1000)
	  integer icalib(2),icalib_new(2)
c
      dimension t(192),t2(192)
      real x_b(24),y_b(24),x_u(24),y_u(24),x_m(24),y_m(24)
	  real t_u(24),t_m(24),t_b(24),t_uc(24),t_mc(24),t_bc(24)	 

      real x_bc(24),y_bc(24),x_uc(24),y_uc(24),x_mc(24),y_mc(24)
	  integer istrip_bc(24),istrip_mc(24),istrip_uc(24)
      dimension mult_bottom(50),mult_middle(50),mult_up(50)
      dimension mhits_bottom(50),mhits_middle(50),mhits_up(50)
      dimension mult_tot(50),mhits_tot(50)
      real r(12),xp(4)
      real n0,n1,n2
	  
	   integer*4 itdc1ch(100),itdc2ch(100)
	   integer*4 itdc1time(100),itdc2time(100)
	   integer*4 itdc1width(100),itdc2width(100)
		  integer*4 ihitl_b(24),ihitr_b(24)
          integer*4 ihitl_m(24),ihitr_m(24)
          integer*4 ihitl_t(24),ihitr_t(24)
		integer*4 i_hit(192)
		integer*4 i_good_b(24),i_good_m(24),i_good_u(24)	   


       real chi_tc(20),v0_tc(20),v1_tc(20),v2_tc(20),tof_tc(20)
	   real time_track(20),track_time
	   integer istrip_b_tc(20),istrip_m_tc(20),istrip_u_tc(20)
	   integer igps_flag

      
      character*250 filename,fileout,file2t,filetime,filesum,n_ev
	  character*4 station_id
	  character*5 run_char
      data delta_bmin,delta_mmin,delta_umin/7.,7.,7./
	  integer*1 b_array(4)
	  equivalence (b_array(1),iword)
	  character*1 tab

	  track_time = 0
	  iwindow_start = 0
	  
c
c Files used
c
c Unit     File                   Content               I/O
c  10     random12.txt       random_numbers           Input
c   1     'filename'         input data               Input
c   2     'fileout'          results/debug            Output
c   3     'filetime'         event times              Output
c   4     'file2t'           2-tracks events          Output
c   5     'filesum'          Run summary              Output
c
c
c

c
      tab=char(9)
      idebug=0
	  idebug3=0
	
	  
c t_delay is the time between the event input to the GPS unit ... and the reset clock on the tdcs.. at CERN it is 1450 ns.  This
c can be entered in a block structure at start of run



      write(*,*) '*****  Analysis of run EEE  ******'
      write(*,*) ' '
c  
c first open the binary input file	  
c
c get number of arguments of command line
c
	  i = COMMAND_ARGUMENT_COUNT()
	  if (i.lt.1) then
	  write (*,*)' You must specify a binary file to analyse'
	  write (*,*)' :e.g.  EEE_V15 inputfile.bin '
	  stop
	  endif
	  
c first argument is the input filename
	   k=1	   
	   CALL GET_COMMAND_ARGUMENT(k, filename, len, istatus)
	   write (*,*) ' Input file name is ',filename
	   if (filename(len-3:len).ne.'.bin')then
	   write (*,*) ' The input file must be binary'
	   write (*,*) 'and have the extension .bin'
	   stop
	   endif
	   run_char=filename(len-8:len-4)
	   READ (run_char, '(I10)'), irun_number
c
c extract run number
c
       	   
c
c second argument is the number of events
c if not specified ... set to infinite (nev_tot = 0)
       nev_tot=0
	   if (i.gt.1)then
	   k=2
	   CALL GET_COMMAND_ARGUMENT(k,n_ev,len2,istatus)
c	   write(*,*)n_ev(1:len2)

        READ (n_ev, '(I10)'), nev_tot
	endif
c
c open input file
c	   
	   i=iopenfile_(filename(1:len))
	  
c
c Define input data file
c
c      write(*,*) 'Input file name'
c      read(*,1) filename
    1 format(A50)
c      open(unit=1,file=filename,status='old')
c
c Define output filenames
c
      do i=1,250
	  fileout(i:i)=filename(i:i)
	  filetime(i:i)=filename(i:i)
	  file2t(i:i)=filename(i:i)
	  filesum(i:i)=filename(i:i)
	  enddo
	  fileout(len-3:len)='.out'
	  filetime(len-3:len)='.tim'
	  file2t(len-3:len)='.2tt'
	  filesum(len-3:len)='.sum'

c      write(*,*) 'Output file name for results/debug'
c      read(*,1) fileout
      open(unit=2,file=fileout,status='unknown')
c
c      write(*,*) 'Output file name for event times'
c      read(*,1) filetime
      open(unit=3,file=filetime,status='unknown')
c
c      write(*,*) 'Output file name for 2-tracks events'
c      read(*,1) file2t
      open(unit=4,file=file2t,status='unknown')
c


c      open(unit=10,file='random12.txt',status='old')
c
      nev_run=0

c      write(*,*) 'No.of events to be analyzed'
c      read(*,*) nev_tot
   2   format(' Results for run ',A50)
       write(2,*)' run_number,event_number,'
     $ ,'secs_since_1.1.2007,nanosec,microseconds_since_start_of_run'
     $  ,'track: unit_vector_x,unit_vector_y,unit_vector_z',
     $ ',chi_squared,time of flight[ns],track length[cm]'
	 
       write(3,*)' run_number,event_number,event_time'
     $ ,'secs since 1.1.2007,nanosec'
	 
	   write(4,*)' run_number,event_number,'
     $ ,'secs_since_1.1.2007,nanosecs,microseconds_since_start_of_run'
     $  ,'track1: unit_vector_x,unit_vector_y,unit_vector_z',
     $ ',chi_squared,time of flight[ns],track length[cm]',
     $ ',track2: unit_vector_x,unit_vector_y,unit_vector_z',
     $ ',chi_squared,time of flight[ns],track length[cm]'

		iout_e=0
c       write(*,*)'Print-out info for each event? (0=no,1=yes)'
c       read(*,*) iout_e
c
           t_b_corr=0.
		   t_m_corr=0.
		   t_t_corr=0.
		   
		   
c
c  open eee_calib file - if it exist
c
		   icalib_exist=0
           open(unit=20,file='eee_calib.txt',IOSTAT= ios,status='old')
c          write(*,*) ' Opening calibration file iostat =',ios
		   if (ios.eq.0) then
		   icalib_exist=1
		   read(20,*)t_b_corr,t_m_corr,t_t_corr
		read(20,*)
     $  tb_low_limit_left,tb_high_limit_left,
     $  tb_low_limit_right,tb_high_limit_right
		read(20,*)
     $  tm_low_limit_left,tm_high_limit_left,
     $  tm_low_limit_right,tm_high_limit_right
		read(20,*)
     $  tt_low_limit_left,tt_high_limit_left,
     $  tt_low_limit_right,tt_high_limit_right


c		   write(*,*)' corrections',t_b_corr,t_m_corr,t_t_corr
		   close(20)
		   endif
		   
		   tb_left=0.
		   tb_right=0.
		   n_tb_hits=0
		   tm_left=0.
		   tm_right=0.
		   n_tm_hits=0
		   tt_left=0.
		   tt_right=0.
		   n_tt_hits=0


	   n_xl1=0
	   n_xh1=0
	   n_xl2=0
	   n_xh2=0
	   n_xl3=0
	   n_xh3=0

       n_x1=0
	   n_x2=0
	   n_x3=0
	   x1_ra=0.
	   x2_ra=0.
	   x3_ra=0.

	   time_br=0.
	   n_time_br=0
	   time_bl=0.
	   n_time_bl=0
	   
	   time_mr=0.
	   n_time_mr=0
	   time_ml=0.
	   n_time_ml=0
	   
	   time_ur=0.
	   n_time_ur=0
	   time_ul=0.
	   n_time_ul=0

      ifirst_ev = 0

      n_tot=0
      n_3clust=0
      n_2clust=0
      n_1clust=0
      n_nohits=0
      n_2hits=0
      n_3hits=0
      do k=1,50
       mhits_bottom(k)=0
       mhits_middle(k)=0
       mhits_up(k)=0
       mhits_tot(k)=0
       mult_bottom(k)=0
       mult_middle(k)=0
       mult_up(k)=0
       mult_tot(k)=0
      end do
      zb=-80.
      zm=0.
      zu=80.
c
c  first : read geometry block and WAD block
c
       igeoflag=0
	   iwadflag=0
       do kk=1,10
	   if(iwadflag.eq.1.and.igeoflag.eq.1)goto 2234
	    j=iread_file_(nlen,ntype,iarray,ierror)
		if(ntype.eq.6) then
		iwadflag=1
		write(*,*)' Have found WAD block'
        write (*,*)" WAD Block"
		write (*,*) (iarray(k),k=1,6)
		t_delay=iarray(5)/1000000000.
        iwindow_start=iarray(2)

		endif
		if (ntype.eq.5) then
		igeoflag=1
c
c  have found geometry block

c


      write (*,*)" Geometry Block"
	   write (*,*) (iarray(k),k=1,10)
	   write (*,*) (iarray(k),k=11,17)
       pi=acos(-1.)
c	   write(*,*)' pi=',pi
       angle=pi*(float(iarray(1))/100.)/180.
	   idist12=iarray(2)
	   idist23=iarray(3)
c
c	   	   idist23=10
c	   
	   zz1=0.
	   zz2=zz1+float(idist12)
	   zz3=zz2+float(idist23)
c
	   ibleft=iarray(10)
	   ibright=iarray(11)
	   imleft=iarray(12)
	   imright=iarray(13)
	   itleft=iarray(14)
	   itright=iarray(15)
	   iword=iarray(17)
	   do k=1,4
	   station_id(k:k) = char(b_array(5-k))
	   enddo

	   
	   write(*,*)' station_id ',station_id
	   icable_b_left=iarray(4)
	   icable_b_right=iarray(5)
	   icable_m_left=iarray(6)
	   icable_m_right=iarray(7)
	   icable_t_left=iarray(8)
	   icable_t_right=iarray(9)
	   
	   
	   
	   icable_b = icable_b_left + icable_b_right
	   icable_t = icable_t_left + icable_t_right
	   adist=idist12+idist23
	   atofcable=(float(icable_b-icable_t))/40.
	   atofd=adist/30.+(float(icable_b-icable_t))/40.
	   atofd_low=atofd-3.0
	   atofd_high=atofd+3.0
	   atofu=-adist/30.+(float(icable_b-icable_t))/40.
	   write(*,*)' expected tof', atofu,atofd
	   
		if(icalib_exist.ne.1) then


	   
c		tb_low_limit_right=alow+(float(icable_b_right)/18.7)
c		tb_high_limit_right=ahigh+(float(icable_b_right)/18.7)		 
c		tb_low_limit_left=alow+(float(icable_b_left)/18.7)
c		tb_high_limit_left=ahigh+(float(icable_b_left)/18.7)
c		tm_low_limit_right=alow+(float(icable_m_right)/18.7)
c		tm_high_limit_right=ahigh+(float(icable_m_right)/18.7)		 
c		tm_low_limit_left=alow+(float(icable_m_left)/18.7)
c		tm_high_limit_left=ahigh+(float(icable_m_left)/18.7)
c		tt_low_limit_right=alow+(float(icable_t_right)/18.7)
c		tt_high_limit_right=ahigh+(float(icable_t_right)/18.7)		 
c		tt_low_limit_left=alow+(float(icable_t_left)/18.7)
c		tt_high_limit_left=ahigh+(float(icable_t_left)/18.7)
		
	   
		tb_low_limit_right=100.
		tb_high_limit_right=600.	 
		tb_low_limit_left=100.
		tb_high_limit_left=600.
		tm_low_limit_right=100.
		tm_high_limit_right=600.	 
		tm_low_limit_left=100.
		tm_high_limit_left=600.
		tt_low_limit_right=100.
		tt_high_limit_right=600.		 
		tt_low_limit_left=100.
		tt_high_limit_left=600.
		
		endif
		
c
c time offset in nanoseconds		 
		 time_offset_b = float(icable_b_left-icable_b_right)*0.0536
		 time_offset_m = float(icable_m_left-icable_m_right)*0.0536
		 time_offset_t = float(icable_t_left-icable_t_right)*0.0536
c		 write(*,*)" time_offset_b",time_offset_b
		 
c		 write(*,*)icable_b_right,icable_b_left
c		 write(*,*)tb_low_limit_right,tb_high_limit_right
c		 write(*,*)tb_low_limit_left,tb_high_limit_left	 

		 endif
		enddo
c
c  have not found geometry block in first 10 data blocks... do not know what to do...
c
       if(igeoflag.eq.0)then
       write(*,*)" Have not found geometry data block in " 
	   write (*,*)"first 10 blocks of data-something is wrong"
	   endif
	   
       if(iwadflag.eq.0)then
       write(*,*)" Have not found wad data block in " 
	   write (*,*)"first 10 blocks of data-something is wrong"
	   endif
	   
	   stop
	   
2234   continue	   	   					  
c	  
c second try and get tdc time calibration
c
       igps_event=0
1234   continue
       j=iread_file_(nlen,ntype,iarray,ierror)
	   if (ntype.eq.0) then
	       if (igps_event.eq.1) then
       write(*,*)' Have found initial gps event' 		   
		     j=irewind_()
		     goto 1235
	       endif
		 igps_event = 1
		 goto 1234
	   endif
	   if (ntype.eq.1.or.ntype.eq.2) then
	   icalib_new(ntype)=iarray(3)
c	   write(*,*)icalib_new(ntype),iarray(1),iarray(2),iarray(3)
	   goto 1234
	   endif
	   goto 1234

1235   continue	
c       write (*,*)' tdc calibration', icalib_new(1),icalib_new(2)  
	   icalib(1)=icalib_new(1)
	   icalib(2)=icalib_new(2) 
		igps_event=0 
   	  

c
c Ciclo sugli eventi
c
1236  continue

c      do i=1,nev_tot
c      write(*,*)' analysing nev_tot = ',nev_tot,' events'
      if (nev_tot.ne.0) then
	    if( n_tot.ge.nev_tot)goto 2999
	  endif	
      teta_ev=0.
      phi_ev=0.
      chi2_ev=0.
      time_ev=0.0
c	  idebug=0
c	  if(nev.eq.115)then
c	   idebug=1
c	  endif 
c
c Read a set of random numbers (0<r<1) to be used for smearing
c
c       read(10,*)  (r(j),j=1,12)
c       do k=1,24
c        x_bc(k)=-999.
c        y_bc(k)=-999.
c        x_mc(k)=-999.
c        y_mc(k)=-999.
c        x_uc(k)=-999.
c        y_uc(k)=-999.
c       end do
       do k=1,192
        t(k)=0.
		t2(k)=0
		i_hit(k)=0
       end do
	   ihit_b_l=0
	   ihit_b_r=0
	   ihit_m_l=0
	   ihit_m_r=0
	   ihit_t_l=0
	   ihit_t_r=0
	   

c
c
c Read data
c
       igps_flag=0
	   idebug2=0
c
   3   continue
c       read(1,*,END=3000) nev,ncod,data1,data2
       j=iread_file_(nlen,ntype,iarray,ierror)
c	   write(*,*)ierror
	   if(ierror.ne.0)go to 3000

c
c Decode data
c
c
       if(ntype.eq.0) then
c gps event
c
c       write (*,*) ' gps event'
c	   write (*,*) iarray(1),iarray(2),iarray(3),iarray(4)
       tns= iarray(1)
	   sec=iarray(2)
	   day=iarray(3)
	   year=iarray(4)-2007
	   icalib(1)=icalib_new(1)
	   icalib(2)=icalib_new(2)
c	   write(*,*)' gps event',sec,tns,icalib_new(1),icalib_new(2)
	   day=day+365.*year
	   if (iarray(4).gt.2008) day=day+1.
	   if (iarray(4).gt.2012) day=day+1.
	   if (iarray(4).gt.2016) day=day+1.
	   igps_event=igps_event+1
	   igps_flag =1
	   go to 3
	   endif
	   
	   if(ntype.eq.1)then
c	   write(*,*)' ****'
       increm1=iarray(3)-icalib_new(1)
c	   if(igps_flag.eq.1)then
c	   write (*,*) 
c     $   'tdc 1 event',iarray(1),iarray(2),iarray(3),increm1
c       igps_flag=0
c       endif
       nev1=iarray(1)
	   icalib_new(1)=iarray(3)
	   tns1=iarray(3)
	   itdc1hits=0
	   do j=1,iarray(2)
	   k=(j*3)+1
c store in temporary block if idebug set
c
       if(idebug.eq.1)then
	   itdc1ch(j)=iarray(k)
	   itdc1time(j)=iarray(k+1)
	   itdc1width(j)=iarray(k+3)
	   itdc1hits=j
	   endif
	   	   
c	   write (*,*) j,iarray(k),iarray(k+1),iarray(k+2)
       time_hit=float(iarray(k+1))/10.
       if(iarray(k).gt.0.and.iarray(k).lt.25)then
	   if(i_hit(k).eq.0)then
	   i_hit(k)=1
	   time_br=time_br+time_hit
	   n_time_br=n_time_br+1
	   endif
c  right bottom hit
       		 if (time_hit.ge.tb_low_limit_right .and. 
     $                time_hit.lt.tb_high_limit_right) then 
	       if(t(iarray(k)).eq.0.) then
	   	    t(iarray(k))=time_hit
			ihit_b_r=ihit_b_r+1
		   else
			if(t2(iarray(k)).eq.0)t2(iarray(k))=time_hit
		   endif
	   endif 
	   endif
	   if(iarray(k).gt.32.and.iarray(k).lt.57)then
c  left bottom hit
	   if(i_hit(k).eq.0)then
	   i_hit(k)=1
	   time_bl=time_bl+time_hit
	   n_time_bl=n_time_bl+1
	   endif

       		 if (time_hit.ge.tb_low_limit_left .and. 
     $                time_hit.lt.tb_high_limit_left) then 
	     if(t(iarray(k)).eq.0.)then
	   	   t(iarray(k))=time_hit
		   ihit_b_l=ihit_b_l+1
		   else
			if(t2(iarray(k)).eq.0)t2(iarray(k))=time_hit
	     endif
	   endif 
	   endif

       if(iarray(k).gt.64.and.iarray(k).lt.89)then
c  right top hit
	   if(i_hit(k).eq.0)then
	   i_hit(k)=1
	   time_ur=time_ur+time_hit
	   n_time_ur=n_time_ur+1
	   endif

        
       		 if (time_hit.ge.tt_low_limit_right .and. 
     $                time_hit.lt.tt_high_limit_right) then 
	     if(t(iarray(k)).eq.0.)then
	   	   t(iarray(k))=time_hit
		   ihit_t_r=ihit_t_r+1
		   else
			if(t2(iarray(k)).eq.0)t2(iarray(k))=time_hit
	     endif
	   endif 
	   endif
	   if(iarray(k).gt.96.and.iarray(k).lt.121)then
c  left top hit
	   if(i_hit(k).eq.0)then
	   i_hit(k)=1
	   time_ul=time_ul+time_hit
	   n_time_ul=n_time_ul+1
	   endif

        time_hit=float(iarray(k+1))/10.
       		 if (time_hit.ge.tt_low_limit_left .and. 
     $                time_hit.lt.tt_high_limit_left) then 
	     if(t(iarray(k)).eq.0.)then
	   	   t(iarray(k))=time_hit
		   ihit_t_l=ihit_t_l+1
		   else
			if(t2(iarray(k)).eq.0)t2(iarray(k))=time_hit
	     endif
	   endif 
	   endif
c	   write (*,*) t(iarray(k))

	   enddo
	   go to 3
	   endif
	   
	   
	   if(ntype.eq.2)then
c	   write(*,*)' ****'
       increm2=iarray(3)-icalib_new(2)
c	   write (*,*) 
c     $  'tdc 2 event',iarray(1),iarray(2),iarray(3),increm2
       nev2=iarray(1)
	   icalib_new(2)=iarray(3)
	   tns2=iarray(3)
	   itdc2hits=0
	   do j=1,iarray(2)
	   k=(j*3)+1
	   if(idebug.eq.1)then
	    itdc2ch(j)=iarray(k)
	    itdc2time(j)=iarray(k+1)
	    itdc2width(j)=iarray(k+3)
	    itdc2hits=j
	   endif
	   time_hit=float(iarray(k+1))/10.

c	   write (*,*) j,iarray(k),iarray(k+1),iarray(k+2)
	          if(iarray(k).gt.0.and.iarray(k).lt.25)then
c  right middle hit
	   if(i_hit(k).eq.0)then
	   i_hit(k)=1
	   time_mr=time_mr+time_hit
	   n_time_mr=n_time_mr+1
	   endif

       		 if (time_hit.ge.tt_low_limit_right .and. 
     $                time_hit.lt.tt_high_limit_right) then 
	     if(t(iarray(k)+128).eq.0.) then
	   	   t(iarray(k)+128)=time_hit
		   ihit_m_r=ihit_m_r+1
		   else
			if(t2(iarray(k)+128).eq.0)t2(iarray(k))=time_hit
	     endif
	   endif 
	   endif
	   if(iarray(k).gt.32.and.iarray(k).lt.57)then
c  left middle hit
	   if(i_hit(k).eq.0)then
	   i_hit(k)=1
	   time_ml=time_ml+time_hit
	   n_time_ml=n_time_ml+1
	   endif

       		 if (time_hit.ge.tt_low_limit_left .and. 
     $                time_hit.lt.tt_high_limit_left) then 
	     if(t(iarray(k)+128).eq.0.)then
	   	   t(iarray(k)+128)=time_hit
		   ihit_m_l=ihit_m_l+1
		   else
			if(t2(iarray(k)+128).eq.0)t2(iarray(k)+128)=time_hit
	     endif
	   endif 
	   endif
	   
c	   	   write (*,*) t(iarray(k)+128)

	   enddo
	   go to 5
	   endif
	   goto 3
	   
c
c End of readout and decoding
c
c
   5  continue
c
c Event time (since 01.01.2007)
c
      if(nev1.eq.nev2)nev=nev1
	  idebug2=0
	  iout_e=0
c	  if(nev.eq.53)then
c	   iout_e=1
c	  idebug2=1
c	  endif
      n_tot=n_tot+1
	  time_ev=(day-1.D0)*86400.D0+sec+(tns)/1.0D9
	  
c   Not sure if this is correct -  will try some changes:  18/03/20011  C.W.
c
c	  tstdc=(1.000001-t_delay)*(tns1/icalib(1)+tns2/icalib(2))*0.5
c	  tstdc = tstdc+t_delay
c

	mytstdc = tns1/icalib(1)
	
	mytstdc = mytstdc * 10D14
	mytD = mytstdc / 10D14

	mytstdc = tns2/icalib(2)
	mytstdc = mytstdc * 10D14

	

	mytD = mytD + (mytstdc / 10D14)
	
	  tstdc=(1.000001D0-t_delay)*(mytD)*0.5D0
	  tstdc = tstdc-0.000001D0
	  
	  delaytest = 1.00001D0
	  
	  delaytest = delaytest - t_delay
	  	
	  val1 = delaytest*tns1*0.5D0 / iCalib(1)

	  val2 = delaytest*tns2*0.5D0 / iCalib(2)
	  
	  mytstdc = val1 + val2
	  
	  mytstdc = mytstdc - 0.000001D0

	  time_ev=time_ev+tstdc
  	
		mytime = time_ev
			
		mytstdc = ((tstdc * 1000000000 + tns ) / 1000000000) * 10D14;

		time_ev = mytime + mytstdc / 10D14;

	  if (ifirst_ev.eq.0) then
	  ifirst_ev = 1
	  itime_ev=time_ev
	  endif
      usec=mytime -itime_ev
	  usec = usec + mytstdc / 10D14

	  iusec= usec*1000000
c	  ifix(usec*1000000)
	  	  
	  isec=time_ev
	  
	  ananosec=isec
	   
	   mytstdc = tns1/icalib(1)
	  
	imytstdc = mytstdc * 10D15

	mytD = imytstdc / 10D15

	mytstdc = tns2/icalib(2)
	imytstdc = mytstdc * 10D15
	mytD = mytD + (imytstdc / 10D15)
	  ananosec= (tns) + tstdc *1.0D9
	  inanosec=ananosec	
	  
c    
c jump out of loop if no hits in any end of chamber
c	  
	  nhits=ihit_b_l*ihit_b_r*ihit_m_l*ihit_m_r*ihit_t_l*ihit_t_r
c	  write(*,*)nev,nhits,ihit_b_l,ihit_m_l,ihit_t_l

	  if (nhits.eq.0) then
	  n_nohits=n_nohits+1
	  goto 2000
	  endif
	  
c write out event time in special file ...   
	  write(3,201) irun_number,nev,isec,inanosec
  201 format(1X,I5,1X,I10,1X,I10,1X,I10)

  
c bottom chamber
c  **************  
c now decode strip number....
         xl=158.
		 n_b=0
c loop over the 24 strips:
         do k = 1,24
		 kk1=k
		 if (ibright.eq.3)then
		 kk1=25-k
		 endif
		 if (t(kk1).gt.0.) then
c valid hit at one end... now check the other end
         kk2=k+32
		 kk4=kk2+1
         if(ibleft.eq.1)then
		 kk2=57-k
		 endif
		 if (t(kk2).gt.0.) then
c         write(*,*)" hit in bottom chamber   strip",k
c		 write(*,*) t(kk1),t(kk2)
		   n_b=n_b+1
		   cen=0.
c calculate x position and check that it is in chamber....		   
	  xp(1)=0.5*xl*(1.0+(t(kk2)-t(kk1)-time_offset_b)/10.)+t_b_corr
		  if(xp(1).lt.0. .or. xp(1).gt.158.)then
		  if(t2(kk1).gt.0..or.t2(kk2).gt.0.)then
c x_position outside chamber and second hit exists.
      xp(2)=0.5*xl*(1.0+(t(kk2)-t2(kk1)-time_offset_b)/10.)+t_b_corr
      xp(3)=0.5*xl*(1.0+(t2(kk2)-t(kk1)-time_offset_b)/10.)+t_b_corr
	  xp(4)=0.5*xl*(1.0+(t2(kk2)-t2(kk1)-time_offset_b)/10.)+t_b_corr
	  if(idebug3.eq.1)
     $  write(*,*)' xp bot',nev,xp(1),xp(2),xp(3),xp(4)
		  xp(1)=abs(xp(1)-78.)
		  xp(2)=abs(xp(2)-78.)
		  xp(3)=abs(xp(3)-78.)
		  xp(4)=abs(xp(4)-78.)
		  xp_old=xp(1)
		  kk_old=1
		  do kk=2,4
		  if(xp(kk).lt.xp_old)then
		  kk_old=kk
		  xp_old=xp(kk)
		  endif
		  enddo
		  if(kk_old.eq.2)then
		  t(kk1)=t2(kk1)
		  elseif(kk_old.eq.3)then
		  t(kk2)=t2(kk2)
		  elseif(kk_old.eq.4)then
		  t(kk1)=t2(kk1)
		  t(kk2)=t2(kk2)
		  endif

          endif
		  endif		   
		   tb_left=tb_left+t(kk2)
		   tb_right=tb_right+t(kk1)
		   n_tb_hits=n_tb_hits+1
           tb_sum=t(kk1)-0.29+t(kk2)
cc
ccc Y-coordinate is perpendicular to strip direction   Y=0 for strip 1   Y=82 for strip 24
ccc X-coordinate is along the strip direction and obtained from the time-difference
ccc   X is proportional to (T_left-T_right) which goes from -10 ns to +10 ns
ccc   (T_left - T_right)=-9  X=0
ccc   (T_left - T_right)=+9  X=158
ccc
ccc   X  |0---------------------------------------> 158
ccc      |
ccc      | Left                                    Right
ccc      |
ccc  Y   |82
ccc                                                 V

c
		   ihitr_b(n_b)=kk1
		   ihitl_b(n_b)=kk2

      y_b(n_b)=float(k)*3.2
	  x_b(n_b)=0.5*xl*(1.0+(t(kk2)-t(kk1)-time_offset_b)/10.)
	  x_b(n_b)=x_b(n_b)+t_b_corr
	  t_b(n_b)=(t(kk2)+t(kk1))/2.	 
         		 
		 endif
		 endif
		 enddo
		 
		 
c		 if (n_b.gt.0) then
c		  write(*,*)n_b," hit in bottom chambers"
c		   do k=1,n_b
c		   write (*,*)k,x_b(k),y_b(k)
c		   enddo
c		 endif
c
c middle chamber
c***************  
c now decode strip number... 
		 n_m=0
c loop over the 24 strips:
         do k = 1,24
		 kk1=k+128
		 if (imright.eq.3)kk1=153-k
		 if (t(kk1).gt.0.) then
c valid hit at one end... now check the other end
         kk2=k+160
         if(imleft.eq.1)kk2=185-k
		 if (t(kk2).gt.0.) then
c         write(*,*)" hit in middle chamber   strip",k
c		 write(*,*) t(kk1),t(kk2)
		   n_m=n_m+1
		   cen=0.
c calculate x position and check that it is in chamber....		   
      xp(1)=0.5*xl*(1.0+(t(kk2)-t(kk1)-time_offset_m)/10.)+t_m_corr
		  if(xp(1).lt.0. .or. xp(1).gt.158.)then
		  if(t2(kk1).gt.0..or.t2(kk2).gt.0.)then
c x_position outside chamber and second hit exists.
      xp(2)=0.5*xl*(1.0+(t(kk2)-t2(kk1)-time_offset_m)/10.)+t_m_corr
      xp(3)=0.5*xl*(1.0+(t2(kk2)-t(kk1)-time_offset_m)/10.)+t_m_corr
      xp(4)=0.5*xl*(1.0+(t2(kk2)-t2(kk1)-time_offset_m)/10.)+t_m_corr
	  if(idebug3.eq.1)
     $   write(*,*)' xp middle',nev,xp(1),xp(2),xp(3),xp(4)

		  xp(1)=abs(xp(1)-78.)
		  xp(2)=abs(xp(2)-78.)
		  xp(3)=abs(xp(3)-78.)
		  xp(4)=abs(xp(4)-78.)
		  xp_old=xp(1)
		  kk_old=1
		  do kk=2,4
		  if(xp(kk).lt.xp_old)then
		  kk_old=kk
		  xp_old=xp(kk)
		  endif
 		  enddo
		  if(kk_old.eq.2)then
		  t(kk1)=t2(kk1)
		  elseif(kk_old.eq.3)then
		  t(kk2)=t2(kk2)
		  elseif(kk_old.eq.4)then
		  t(kk1)=t2(kk1)
		  t(kk2)=t2(kk2)
		  endif

          endif
		  endif		   

           tm_sum=t(kk1)+t(kk2)
		   tm_left=tm_left+t(kk2)
		   tm_right=tm_right+t(kk1)
		   n_tm_hits=n_tb_hits+1

cc
ccc Y-coordinate is perpendicular to strip direction   Y=0 for strip 1   Y=82 for strip 24
ccc X-coordinate is along the strip direction and obtained from the time-difference
ccc   X is proportional to (T_left-T_right) which goes from -10 ns to +10 ns
ccc   (T_left - T_right)=-9  X=0
ccc   (T_left - T_right)=+9  X=158
ccc
ccc   X  |0---------------------------------------> 158
ccc      |
ccc      | Left                                    Right
ccc      |
ccc  Y   |82
ccc                                                 V

c
		   ihitr_m(n_m)=kk1
		   ihitl_m(n_m)=kk2

	  y_m(n_m)=float(k)*3.2
      x_m(n_m)=0.5*xl*(1.0+(t(kk2)-t(kk1)-time_offset_m)/10.)+t_m_corr
	  t_m(n_m)=(t(kk2)+t(kk1))/2.	 
		 
         		 
		 endif
		 endif
		 
				   
		 enddo
c		 if (n_m.gt.0) then
c		  write(*,*)n_m," hit in middle chambers"
c		   do k=1,n_m
c		   write (*,*)k,x_m(k),y_m(k)
c		   enddo
c		 endif
c
c top chamber
c************  
c now decode strip number...
		 n_u=0
c loop over the 24 strips:
         do k = 1,24
		 kk1=k+64
		 if (itright.eq.3)kk1=89-k
		 if (t(kk1).gt.0.) then
c valid hit at one end... now check the other end
         kk2=k+96
         if(itleft.eq.1)kk2=121-k
		 if (t(kk2).gt.0.) then
c         write(*,*)" hit in top chamber   strip",k
c		 write(*,*) t(kk1),t(kk2)
		   n_u=n_u+1
		   cen=0.
c calculate x position and check that it is in chamber....		   
      xp(1)=0.5*xl*(1.0+(t(kk2)-t(kk1)-time_offset_t)/10.)+t_t_corr
		  if(xp(1).lt.0. .or. xp(1).gt.158.)then
		  if(t2(kk1).gt.0..or.t2(kk2).gt.0.)then
c x_position outside chamber and second hit exists.
      xp(2)=0.5*xl*(1.0+(t(kk2)-t2(kk1)-time_offset_t)/10.)+t_t_corr
      xp(3)=0.5*xl*(1.0+(t2(kk2)-t(kk1)-time_offset_t)/10.)+t_t_corr
      xp(4)=0.5*xl*(1.0+(t2(kk2)-t2(kk1)-time_offset_t)/10.)+t_t_corr
	  	  if(idebug3.eq.1)
     $       write(*,*)' xptop',nev,xp(1),xp(2),xp(3),xp(4)

		  xp(1)=abs(xp(1)-78.)
		  xp(2)=abs(xp(2)-78.)
		  xp(3)=abs(xp(3)-78.)
		  xp(4)=abs(xp(4)-78.)
		  xp_old=xp(1)
		  kk_old=1
		  do kk=2,4
		  if(xp(kk).lt.xp_old)then
		  kk_old=kk
		  xp_old=xp(kk)
		  endif
		  enddo
		  if(idebug3.eq.1)write(*,*)' kk_old,xp_old',kk_old,xp_old
		  if(kk_old.eq.2)then
		  t(kk1)=t2(kk1)
		  elseif(kk_old.eq.3)then
		  t(kk2)=t2(kk2)
		  elseif(kk_old.eq.4)then
		  t(kk1)=t2(kk1)
		  t(kk2)=t2(kk2)
		  endif

          endif
		  endif		   

           tu_sum=t(kk1)+t(kk2)
		   tt_left=tt_left+t(kk2)
		   tt_right=tt_right+t(kk1)
		   n_tt_hits=n_tt_hits+1

cc
ccc Y-coordinate is perpendicular to strip direction   Y=0 for strip 1   Y=82 for strip 24
ccc X-coordinate is along the strip direction and obtained from the time-difference
ccc   X is proportional to (T_left-T_right) which goes from -10 ns to +10 ns
ccc   (T_left - T_right)=-9  X=0
ccc   (T_left - T_right)=+9  X=158
ccc
ccc   X  |0---------------------------------------> 158
ccc      |
ccc      | Left                                    Right
ccc      |
ccc  Y   |82
ccc                                                 V

c
		   ihitr_t(n_u)=kk1
		   ihitl_t(n_u)=kk2


	  y_u(n_u)=float(k)*3.2
      x_u(n_u)=0.5*xl*(1.0+(t(kk2)-t(kk1)-time_offset_t)/10.)+t_t_corr
	  t_u(n_u)=(t(kk2)+t(kk1))/2.
		 
         		 
		 endif
		 endif
		 
				   
		 enddo
		 
	 

		 
c
c  now merge neighbouring strips  bottom plane
c
        i_good=0
		
        do k=1,24
		i_good_b(k)=0
		i_good_m(k)=0
		i_good_u(k)=0
		enddo
		

		
      if(n_b.gt.1.or.n_u.gt.1)then
	  if(idebug2.eq.1)then
	  write(*,*)' hits bottom, hits top',n_b,n_u
	  write(*,*) 'expected tof',atofd,atofd_low,atofd_high
	  endif
        do n11=1,n_b
        do n33=1,n_u
		tofd=t_b(n11)-t_u(n33)
	  
		if(idebug2.eq.1)write(*,*)'n11,n33,tofd',n11,n33,tofd
		 if(tofd.gt.atofd_low.and.tofd.lt.atofd_high)then
		 i_good=1
		 i_good_b(n11)=1
		 i_good_u(n33)=1
		 if(idebug2.eq.1)
     $   write(*,*)'n11,n33,igood',n11,n33,i_good_b(n11),i_good_u(n33)
		 endif
		enddo
	    enddo

	  if(idebug2.eq.1)then
	  write(*,*)' igoodb',(i_good_b(k),k=1,n_b)
	  write(*,*)' igoodu',(i_good_u(k),k=1,n_u)
	  endif
	  
	  

	  
	  
	  if(i_good.eq.1)then
	  n11=1
7     continue	  
	  if(n_b.gt.1)then
	  
	  do kk=1,n_b
	  if(i_good_b(kk).eq.1)then
	    ibefore=0
		iafter=0
		if(kk.gt.1)then
		  if(abs(y_b(kk-1)-y_b(kk)).lt.3.5)then
		  ibefore=1
		  endif
		endif
		if(kk.lt.n_b)then
		  if(abs(y_b(kk+1)-y_b(kk)).lt.3.5)then
		  iafter=1
		  endif
		endif
		iboth=ibefore*iafter
		if(iboth.eq.0.and.ibefore.eq.1)then
		y_b(kk)=(y_b(kk-1)+y_b(kk))/2.
		endif
		if(iboth.eq.0.and.iafter.eq.1)then
		y_b(kk)=(y_b(kk+1)+y_b(kk))/2.
		endif
	  endif
	  enddo
	  
	  
		if(n11.le.n_b)then
		
		 if(i_good_b(n11).eq.0)then
		 if(n_b.gt.n11)then
		  do kkk=n11,n_b-1
		  y_b(kkk)=y_b(kkk+1)
		  x_b(kkk)=x_b(kkk+1)
		  t_b(kkk)=t_b(kkk+1)
		  i_good_b(kkk)=i_good_b(kkk+1)
		  ihitr_b(kkk)=ihitr_b(kkk+1)
		  ihitl_b(kkk)=ihitl_b(kkk+1)

		  enddo
		 n_b=n_b-1
		 n11=n11-1
		 endif
		 endif
		n11=n11+1
		goto 7
		endif
	  endif
      n33=1
8     continue	  
	  if(n_u.gt.1)then
	  
	  do kk=1,n_u
	  if(i_good_u(kk).eq.1)then
	    ibefore=0
		iafter=0
		if(kk.gt.1)then
		  if(abs(y_u(kk-1)-y_u(kk)).lt.3.5)then
		  ibefore=1
		  endif
		endif
		if(kk.lt.n_u)then
		  if(abs(y_u(kk+1)-y_u(kk)).lt.3.5)then
		  iafter=1
		  endif
		endif
		iboth=ibefore*iafter
		if(iboth.eq.0.and.ibefore.eq.1)then
		y_u(kk)=(y_u(kk-1)+y_u(kk))/2.
		endif
		if(iboth.eq.0.and.iafter.eq.1)then
		y_u(kk)=(y_u(kk+1)+y_u(kk))/2.
		endif
	  endif
	  enddo
	  
	  
	    if(n33.le.n_u)then
		
		if(i_good_u(n33).eq.0)then
		if(n_u.gt.n33)then
		do kkk=n33,n_u-1
		  y_u(kkk)=y_u(kkk+1)
		  x_u(kkk)=x_u(kkk+1)
		  t_u(kkk)=t_u(kkk+1)
		  i_good_u(kkk)=i_good_u(kkk+1)
		  ihitr_t(kkk)=ihitr_t(kkk+1)
		  ihitl_t(kkk)=ihitl_t(kkk+1)
		enddo
		n33=n33-1
		n_u=n_u-1
		endif
		endif		
	   n33=n33+1
	   goto 8
	   endif		 
	  endif
	  endif
	  endif
      if(idebug2.eq.1)then
 	  write(*,*)' n_b after tof cluster',n_b,n_u
	  endif		
	
        k=1
9        continue		
         if(k.lt.n_b)then
		kk=k+1
		istrip1=ihitr_b(k)
		istrip2=ihitr_b(kk)
		
		
		if (iabs(istrip1-istrip2).lt.2)then

		if(t_b(k).gt.t_b(kk)) then
		t_b(k)=t_b(kk)
		x_b(k)=x_b(kk)
		endif
		y_b(k)=(y_b(k)+y_b(kk))*0.5
c now move hits down by one place		
        if(n_b.gt.kk)then
		  do kkk=kk,n_b-1
		  y_b(kkk)=y_b(kkk+1)
		  x_b(kkk)=x_b(kkk+1)
		  t_b(kkk)=t_b(kkk+1)
		  ihitr_b(kkk)=ihitr_t(kkk+1)
		  ihitl_b(kkk)=ihitl_t(kkk+1)
		  enddo
		endif
		n_b=n_b-1
		endif		
		k=k+1
		goto 9				 
		endif
		
      if(idebug2.eq.1)then
 	  write(*,*)' n_b after merging neighbours',n_b	
	  endif	
	
	
	
																																																																																													
	
	
	
c  now merge neighbouring strips  middle plane
c
        k=1
19        continue		
         if(k.lt.n_m)then
		kk=k+1
		istrip1=ihitr_m(k)
		istrip2=ihitr_m(kk)
	  if(idebug2.eq.1)then
 	  write(*,*)' middle',istrip1,istrip2
	  endif	

		if (iabs(istrip1-istrip2).lt.2)then
		if(t_m(k).gt.t_m(kk)) then
		t_m(k)=t_m(kk)
		x_m(k)=x_m(kk)
		endif
		y_m(k)=(y_m(k)+y_m(kk))*0.5
c now move hits down by one place		
        if(n_m.gt.kk)then
		  do kkk=kk,n_m-1
		  y_m(kkk)=y_m(kkk+1)
		  x_m(kkk)=x_m(kkk+1)
		  t_m(kkk)=t_m(kkk+1)
		  ihitr_m(kkk)=ihitr_t(kkk+1)
		  ihitl_m(kkk)=ihitl_t(kkk+1)
		  enddo
		endif
		n_m=n_m-1
		endif		
		k=k+1		 
		goto 19
		endif

      if(idebug2.eq.1)then
 	  write(*,*)' n_m after merging neighbours',n_m	
	  endif	

c  now merge neigbouring strips top plane



        k=1
29        continue
         if(idebug2.eq.1)write(*,*)' k,n_u',k,n_u		
         if(k.lt.n_u)then
		kk=k+1
		istrip1=ihitr_t(k)
		istrip2=ihitr_t(kk)


		if (iabs(istrip1-istrip2).lt.2)then


		
		if(t_u(k).gt.t_u(kk)) then
		t_u(k)=t_u(kk)
		x_u(k)=x_u(kk)
		endif
		y_u(k)=(y_u(k)+y_u(kk))*0.5
c now move hits down by one place
        if(n_u.gt.kk)then
		  do kkk=kk,n_u-1
		  y_u(kkk)=y_u(kkk+1)
		  x_u(kkk)=x_u(kkk+1)
		  t_u(kkk)=t_u(kkk+1)
		  ihitr_t(kkk)=ihitr_t(kkk+1)
		  ihitl_t(kkk)=ihitl_t(kkk+1)
		  enddo
		endif
		n_u=n_u-1
		endif		
		k=k+1
		goto 29		 
		endif

      if(idebug2.eq.1)then
 	  write(*,*)' n_u after merging neighbours',n_u	
	  endif	
		

	
c
c Hits multiplicity
c
      nhits_tot=n_b+n_m+n_u
      mhits_bottom(n_b)=mhits_bottom(n_b)+1
      mhits_middle(n_m)=mhits_middle(n_m)+1
      mhits_up(n_u)=mhits_up(n_u)+1
      mhits_tot(nhits_tot)=mhits_tot(nhits_tot)+1

c
c Reconstruction of clusters from hits
c Consider at the moment only events with maximum number of 2 hits in each chamber
c Events with more than 2 hits/chamber under test
c
      if(iout_e.eq.1) then
       write(2,*)'No. of hits bottom-middle-up ',n_b,n_m,n_u
      endif
c
c Skip events with more than 2 hits
c don't skip go to 100 commented
c
      if(n_b.gt.2.or.n_m.gt.2.or.n_u.gt.2) then
       n_3hits=n_3hits+1
c       go to 100
      endif
c
c Skip events with no hits
c
      if(n_b*n_m*n_u.eq.0) then
       go to 2000
      endif
      
      n_2hits=n_2hits+1
	  

	  
c
c Bottom chamber
c



	  do kk=1,n_b
	  x_bc(kk)=x_b(kk)
	  y_bc(kk)=y_b(kk)
	  
	  t_bc(kk)=t_b(kk)
	  
	  
	  istrip_bc(kk)=ihitr_b(kk)
	  enddo

	  
	  n_bc=n_b

c      delta_b=0.
c just one hit	  
c      if(n_b.eq.1) then
c        n_bc=1
c        x_bc(1)=x_b(1)
c        y_bc(1)=y_b(1)
c		t_bc(1)=t_b(1)
c        go to 10
c      endif
c two hits 	  
c      if(n_b.eq.2) then
c	  if (abs(y_b(1)-y_b(2)).lt.3.5)then
c	   n_bc=1
c neighbouring strips fire - choose strip that fires earlier.
c      if(t_b(1).lt.t_b(2))then
c          x_bc(1)=x_b(1)
c          y_bc(1)=(y_b(1)+y_b(2))*0.5
c		  t_bc(1)=t_b(1)
c	  else
c          x_bc(1)=x_b(2)
c          y_bc(1)=y_b(2)
c		  t_bc(1)=t_b(2)
c	  endif
c	   goto 10
c	  endif	
c two hits - but not neighbours	    
c        delta_b=sqrt((x_b(1)-x_b(2))**2+(y_b(1)-y_b(2))**2)
c        if(delta_b.gt.delta_bmin) then
c          n_bc=2
c          x_bc(1)=x_b(1)
c          y_bc(1)=y_b(1)
c		  t_bc(1)=t_b(1)
c          x_bc(2)=x_b(2)
c          y_bc(2)=y_b(2)
c		  t_bc(2)=t_b(2)
c          go to 10
c        else
c          n_bc=1
c          x_bc(1)=0.5*(x_b(1)+x_b(2))
c          y_bc(1)=0.5*(y_b(1)+y_b(2))
c		  if(t_b(1).lt.t_b(2)) then
c		  t_bc(1)=t_b(1)
c		  else
c		  t_bc(1)=t_b(2)
c		  endif
c          go to 10
c        endif
c      endif


c
c Middle chamber
c
  10  continue
  	  do kk=1,n_m
	  x_mc(kk)=x_m(kk)
	  y_mc(kk)=y_m(kk)
	  t_mc(kk)=t_m(kk)
	  istrip_mc(kk)=ihitr_m(kk)
	  enddo
	  n_mc=n_m

c     delta_m=0.
c     if(n_m.eq.1) then
c       n_mc=1
c       x_mc(1)=x_m(1)
c       y_mc(1)=y_m(1)
c		t_mc(1)=t_m(1)
c        go to 20
c      endif
c      if(n_m.eq.2) then
c	  	  if (abs(y_m(1)-y_m(2)).lt.3.5)then
c	   n_mc=1
c neighbouring strips fire - choose strip that fires earlier.
c      if(t_m(1).lt.t_m(2))then
c          x_mc(1)=x_m(1)
c          y_mc(1)=y_m(1)
c		  t_mc(1)=t_m(1)
c	  else
c  		  x_mc(1)=x_m(2)
c          y_mc(1)=y_m(2)
c		  t_mc(1)=t_m(2)
c	  endif
c	   goto 20
c	  endif	

c        delta_m=sqrt((x_m(1)-x_m(2))**2+(y_m(1)-y_m(2))**2)
c        if(delta_m.gt.delta_mmin) then
c          n_mc=2
c          x_mc(1)=x_m(1)
c          y_mc(1)=y_m(1)
c		  t_mc(1)=t_m(1)
c          x_mc(2)=x_m(2)
c          y_mc(2)=y_m(2)
c		  t_mc(2)=t_m(2)
c          go to 20
c        else
c          n_mc=1
c          x_mc(1)=0.5*(x_m(1)+x_m(2))
c          y_mc(1)=0.5*(y_m(1)+y_m(2))
c		  if(t_m(1).lt.t_m(2)) then
c		  t_mc(1)=t_m(1)
c		  else
c		  t_mc(1)=t_m(2)
c		  endif
c          go to 20
c        endif
c      endif
c
c Up chamber
c
 20   continue
      if(idebug2.eq.1)write(*,*)' n_u',n_u
	  

	  
	  
	  do kk=1,n_u
	  x_uc(kk)=x_u(kk)
	  y_uc(kk)=y_u(kk)
	  t_uc(kk)=t_u(kk)
	  istrip_uc(kk)=ihitr_t(kk)
	  enddo
	  
	  
	  n_uc=n_u

c      delta_u=0.
c      if(n_u.eq.1) then
c        n_uc=1
c        x_uc(1)=x_u(1)
c        y_uc(1)=y_u(1)
c		t_uc(1)=t_u(1)
c        go to 30
c      endif
c      if(n_u.eq.2) then
c        delta_u=sqrt((x_u(1)-x_u(2))**2+(y_u(1)-y_u(2))**2)
c			  if (abs(y_u(1)-y_u(2)).lt.3.5)then
c	   n_uc=1
c neighbouring strips fire - choose strip that fires earlier.
c      if(t_u(1).lt.t_u(2))then
c          x_uc(1)=x_u(1)
c          y_uc(1)=y_u(1)
c		  t_uc(1)=t_u(1)
c	  else
c          x_uc(1)=x_u(2)
c          y_uc(1)=y_u(2)
c		  t_uc(1)=t_u(2)
c	  endif
c	   goto 30
c	  endif	

c        if(delta_u.gt.delta_umin) then
c          n_uc=2
c          x_uc(1)=x_u(1)
c          y_uc(1)=y_u(1)
c		  t_uc(1)=t_u(1)
c          x_uc(2)=x_u(2)
c          y_uc(2)=y_u(2)
c		  t_uc(2)=t_u(2)
c          go to 30
c        else
c          n_uc=1
c          x_uc(1)=0.5*(x_u(1)+x_u(2))
c          y_uc(1)=0.5*(y_u(1)+y_u(2))
c		  if(t_u(1).lt.t_u(2)) then
c		  t_uc(1)=t_u(1)
c		  else
c		  t_uc(1)=t_u(2)
c		  endif
c         go to 30
c        endif
c      endif
c
  30  continue

c
c Cluster multiplicity
c
      n_clust_tot=n_bc+n_mc+n_uc
      mult_bottom(n_bc)=mult_bottom(n_bc)+1
      mult_middle(n_mc)=mult_middle(n_mc)+1
      mult_up(n_uc)=mult_up(n_uc)+1
      mult_tot(n_clust_tot)=mult_tot(n_clust_tot)+1
      
      
c
c Events with 1 cluster in each chamber
c
      if(iout_e.eq.1) then
      write(2,*) 'No. of clusters bottom-middle-up ',n_bc,n_mc,n_uc
      endif

c
c Evaluate all combinations of clusters in the 3 chambers and select
c the one with minimum chi2.
c
      tof_old=1000.
      chi_old=1.0E9
      chi2rif=1.0E9
	  itrack_cand=0
	  if (idebug2.eq.1)then
	  write(*,*)' nev n_bc n_mc n_uc',nev,n_bc,n_mc,n_uc
	  
	  endif
c	  if(n_bc.gt.1.and.n_mc.gt.1.and.n_uc.gt.1)then
c	  write(*,*)' possible two track event event number',nev
c	  endif
      do n11=1,n_bc
       do n22=1,n_mc
        do n33=1,n_uc
      
      tof=t_bc(n11)-t_uc(n33)
c	  write(*,*)' n11,n33,tof',n11,n33,tof
      if(n_bc.eq.1.and.n_mc.eq.1.and.n_uc.eq.1.) n_1clust=n_1clust+1

      if(iout_e.eq.1) then
       write(2,*) 'X-Y (cm) bottom-middle-up ',x_bc(n11),y_bc(n11),
     *            x_mc(n22),y_mc(n22),x_uc(n33),y_uc(n33)
      endif
c
c Reconstruction of angles theta,phi
c
c Fit of the 3 clusters through straight lines in plane x-z,  y-z
c  distance between chambers=80 cm
c
      xx1=x_bc(n11)
      yy1=y_bc(n11)
c      zz1=-80.0  
      xx2=x_mc(n22)
      yy2=y_mc(n22)
c      zz2=0.0
      xx3=x_uc(n33)
      yy3=y_uc(n33)
c      zz3=80.0
c
c Select only physical coordinates within chambers
c

c      if(xx1.lt.0.or.xx1.gt.158.or.xx2.lt.0.or.xx2.gt.158.
c     *or.xx3.lt.0.or.xx3.gt.158.or.yy1.lt.0.or.yy1.gt.82.
c     *or.yy2.lt.0.or.yy2.gt.82.or.yy3.lt.0.or.yy3.gt.82)go to 2000
c
c To evaluate space resolution compare position extrapolated from UP/BOTTOM
c  chambers to position found in MIDDLE chamber
c
c      write(2,*) 'x13,x2,y13,y2= ',(xx1+xx3)/2., xx2, (yy1+yy3)/2.,yy2
c
c
c keep track of running averages and x positions out of range
c

c       write(*,*)" xx1=",xx1,yy1,zz1
c       write(*,*)" xx1=",xx2,yy2,zz2
c       write(*,*)" xx1=",xx3,yy3,zz3
	   
       x1_ra=x1_ra+xx1
	   n_x1=n_x1+1
       x2_ra=x2_ra+xx2
	   n_x2=n_x2+1
       x3_ra=x3_ra+xx3
	   n_x3=n_x3+1
	   if(xx1.lt.0) n_xl1=n_xl1+1
	   if(xx1.gt.158.)n_xh1=n_xh1+1
	   if(xx2.lt.0) n_xl2=n_xl2+1
	   if(xx2.gt.158.)n_xh2=n_xh2+1
	   if(xx3.lt.0) n_xl1=n_xl3+1
	   if(xx3.gt.158.)n_xh3=n_xh3+1
       sx=xx1+xx2+xx3
       sy=yy1+yy2+yy3
       sz=zz1+zz2+zz3
       sxz=xx1*zz1+xx2*zz2+xx3*zz3
       syz=yy1*zz1+yy2*zz2+yy3*zz3
       sx2=xx1*xx1+xx2*xx2+xx3*xx3
       sy2=yy1*yy1+yy2*yy2+yy3*yy3
       denx=3.*sx2-sx*sx
       deny=3.*sy2-sy*sy
       a=(3.*sxz-sx*sz)/denx
       b=(sx2*sz-sx*sxz)/denx
       c=(3.*syz-sy*sz)/deny
       d=(sy2*sz-sy*syz)/deny
       chi2xz=(zz1-a*xx1-b)**2+(zz2-a*xx2-b)**2+(zz3-a*xx3-b)**2
       chi2yz=(zz1-c*yy1-d)**2+(zz2-c*yy2-d)**2+(zz3-c*yy3-d)**2
c       write(*,*) 'Chi2xz = ',chi2xz
c       write(*,*) xx1,zz1, a*xx1+b
c       write(*,*) xx2,zz2, a*xx2+b
c       write(*,*) xx3,zz3, a*xx3+b
c       write(*,*) 'Chi2yz = ',chi2yz
c       write(*,*) yy1,zz1, c*yy1+d
c       write(*,*) yy2,zz2, c*yy2+d
c       write(*,*) yy3,zz3, c*yy3+d
c       write(*,*)'----------'
c	   write(*,*)' a,b,c,d',a,b,c,d
c tetaf = angle extracted from fit
c teta  = angle extracted from only 2 clusters (in bottom and up chambers)
c
      tetaf=atan(sqrt(1.+((b-d)/c-(a+b-d)/c)**2)/abs(a))*(180./3.1415)
c        teta=atan(sqrt((xx3-xx1)**2+(yy3-yy1)**2)/20.)*(180/3.14)
       teta=atan(sqrt((xx3-xx1)**2+(yy3-yy1)**2)/(zz3-zz1))*(180/3.14)
c
c phif = angle extracted from fit
c phi  = angle extracted from only 2 clusters (in bottom and up chambers)
c
       tphif=(a/c)
       phif=atan(tphif)*(180./3.1415)
       phi=atan((yy3-yy1)/(xx3-xx1))*(180./3.1415)
        if((yy3-yy1).lt.0.and.(xx3-xx1).lt.0.) then
          phi=phi+180.
          phif=phif+180.
        endif
        if((yy3-yy1).gt.0.and.(xx3-xx1).lt.0.) then
          phi=phi+180.
          phif=phif+180.
        endif
        if((yy3-yy1).lt.0.and.(xx3-xx1).gt.0.) then
         phi=360.-abs(phi)
         phif=360.-abs(phif)
        endif
c
c Fit procedure in the 3D-space
c
      sumx=xx1+xx2+xx3
      sumy=yy1+yy2+yy3
      sumz=zz1+zz2+zz3
      xz=xx1*zz1+xx2*zz2+xx3*zz3
      yz=yy1*zz1+yy2*zz2+yy3*zz3
      z2=zz1*zz1+zz2*zz2+zz3*zz3
      sumz2=sumz*sumz
      p0=(3.0*xz-sumx*sumz)/(3.0*z2-sumz2)
      p1=(sumx-p0*sumz)/3.
      p2=(3*yz-sumy*sumz)/(3.0*z2-sumz2)
      p3=(sumy-p2*sumz)/3.
      n0=p0/sqrt(1.0+p0*p0+p2*p2)
      n1=p2/sqrt(1.0+p0*p0+p2*p2)
      n2=1.0/sqrt(1.0+p0*p0+p2*p2)
      teta3=(180./3.1415)*atan(sqrt(n0**2+n1**2)/n2)
      phi3=(180./3.1415)*atan(n1/n0)
      zzz=n0*n0+n1*n1+n2*n2
c      write(*,*)'p0,p1,p2,p3 = ',p0,p1,p2,p3
c      write(*,*)'n0,n1,n2 = ',n0,n1,n2,zzz
        if((yy3-yy1).lt.0.and.(xx3-xx1).lt.0.) then
          phi3=phi3+180.
        endif
        if((yy3-yy1).gt.0.and.(xx3-xx1).lt.0.) then
          phi3=phi3+180.
        endif
        if((yy3-yy1).lt.0.and.(xx3-xx1).gt.0.) then
         phi3=360.-abs(phi3)
        endif
c      write(*,*) 'teta2,phi2,teta3,phi3,teta,phi = ',
c     * tetaf,phif,teta3,phi3,teta,phi
c
c Evaluation of distances between points and line in 3D-space
c
      dd=sqrt(n0*n0+n1*n1+n2*n2)
      ax1=n2*(yy1-p3)-n1*zz1
      ay1=-n2*(xx1-p1)+n0*zz1
      az1=n1*(xx1-p1)-n0*(yy1-p3)
      dn1=sqrt(ax1**2+ay1**2+az1**2)
      dist1=dn1/dd

      ax2=n2*(yy2-p3)-n1*zz2
      ay2=-n2*(xx2-p1)+n0*zz2
      az2=n1*(xx2-p1)-n0*(yy2-p3)
      dn2=sqrt(ax2**2+ay2**2+az2**2)
      dist2=dn2/dd
      
      ax3=n2*(yy3-p3)-n1*zz3
      ay3=-n2*(xx3-p1)+n0*zz3
      az3=n1*(xx3-p1)-n0*(yy3-p3)
      dn3=sqrt(ax3**2+ay3**2+az3**2)
      dist3=dn3/dd
      
      chi2=sqrt(dist1**2+dist2**2+dist3**2)
c      write(*,*) 'dist1,2,3= ',dist1,dist2,dist3,chi2

c
c      write(2,*) teta3,phi3,(xx3+xx1)/2.,xx2,(yy3+yy1)/2.,yy2
c      write(2,*) xx1,yy1,xx2,yy2,xx3,yy3,teta3,phi3,chi2,n_b,n_m,n_u
      if(iout_e.eq.1) then
c       write(2,*)'Teta,Phi = ',teta3,phi3,tetaf,phif,teta,phi
      endif
c
c  keep all track candidates
c
       if(itrack_cand.lt.20)then
       itrack_cand=itrack_cand+1
	   chi_tc(itrack_cand)=chi2
	   v0_tc(itrack_cand)=n0
	   v1_tc(itrack_cand)=n1
	   v2_tc(itrack_cand)=n2
	   tof_tc(itrack_cand)=t_bc(n11)-t_uc(n33)
	   time_track(itrack_cand)=(t_bc(n11)+t_uc(n33))/2.
	   
	   istrip_b_tc(itrack_cand)=istrip_bc(n11)
	   istrip_m_tc(itrack_cand)=istrip_mc(n22)
	   istrip_u_tc(itrack_cand)=istrip_uc(n33)
	   endif	  
	  

c      if(chi2.lt.chi2rif) then
c         teta_ev=teta3
c         phi_ev=phi3
c         chi2_ev=chi2
c         chi2rif=chi2
c         x1_ev=xx1
c         y1_ev=yy1
c         x3_ev=xx3
c         y3_ev=yy3
c		 teta_rad=teta_ev*3.1415/180.
c		 phi_rad=phi_ev*3.1415/180.
c      endif
c
c  End of loops on cluster combinations
c
        end do
       end do
      end do
c
c write-out event info
c
c       write(2,*) x1_ev,y1_ev,x3_ev,y3_ev,tb_sum,tu_sum
c      write(2,300) nev,nhits_tot,n_clust_tot,teta_ev,phi_ev,
c     * chi2_ev,time_ev
c  300 format(I6,1x,I2,1x,I2,1x,F7.3,1x,F7.3,1x,F7.3,1x,D28.20)
  
c.. pick out lowest chi2
	   chi_old=1000000000.
	   do k=1,itrack_cand
       if(chi_tc(k).lt.chi_old)then
	   chi_old=chi_tc(k)
	   v0_ev=v0_tc(k)
	   v1_ev=v1_tc(k)
	   v2_ev=v2_tc(k)
	   tof_ev=tof_tc(k)
	   track_time=time_track(k)
	   istr_b=istrip_b_tc(k)
	   istr_m=istrip_m_tc(k)
	   istr_u=istrip_u_tc(k)
	   itr_cand_ev=k
	   endif	  
       enddo
	
c... check that tof if ok
      if(abs(tof_ev-atofd).gt.3.)then
c  tof not OK... check if there are candidates with better tof
       tof_old=3.
	   do k=1,itrack_cand
	   tof_cand=abs(tof_tc(k)-atofd)
	   if(tof_cand.lt.tof_old)then
	   tof_old=tof_cand
	   chi_old=chi_tc(k)
	   v0_ev=v0_tc(k)
	   v1_ev=v1_tc(k)
	   v2_ev=v2_tc(k)
	   tof_ev=tof_tc(k)
	   track_time=time_track(k)
	   istr_b=istrip_b_tc(k)
	   istr_m=istrip_m_tc(k)
	   istr_u=istrip_u_tc(k)
	   itr_cand_ev=k
	   endif	  
       enddo

	  
	  endif

      zzz=zz3-zz1
	  
c      path=sqrt(zzz*zzz*(1.+(v0_ev*v0_ev+v1_ev*v1_ev)))
	  vxy=sqrt(v0_ev*v0_ev+v1_ev*v1_ev)
	  transverse=(vxy/v2_ev)*zzz
	  path=sqrt(transverse*transverse+zzz*zzz)
	  anglexy=atan(v1_ev/v0_ev)
	  if(v0_ev.lt.0.)anglexy=anglexy+pi
	  anglexy=anglexy+angle
	  if(anglexy.gt.2*pi)anglexy=anglexy-(2*pi)
	  v1_ev=vxy*sin(anglexy)
	  v0_ev=vxy*cos(anglexy)
	  if(chi_old.gt.99.999)chi_old=99.999
	  tof_out=tof_ev-atofcable

c	  write(*,*)' inanosec,track_time,iwindow_start',
c     * inanosec,track_time,iwindow_start

	itest = track_time
	  
c	  inanosec=inanosec+itest+iwindow_start

	inanosec = inanosec+itest+iwindow_start

	  write(2,301) 
     $  irun_number,nev,isec,inanosec,
     $  iusec,v0_ev,v1_ev,v2_ev,
     $  chi_old,tof_out,path

c	  write(2,*)
c     $  irun_number,tab,nev,tab,isec,tab,inanosec,tab,
c     $  iusec,tab,v0_ev,tab,v1_ev,tab,v2_ev,tab,
c     $  chi_old,tab,tof_ev,tab,path



  301 format(1X,I5,1X,I10,1X,I10,1X,I10,1X,I12,F10.5, 
     $  F10.5,F10.5,1X,F8.5,1X,F10.3,1X,F10.2)
c  301 format(I5,a1,I10,a1,I10,a1,I10,1X,I12,F10.5, 
c     $  F10.5,F10.5,1X,F8.5,1X,F10.3,1X,F10.2)
	 
		if(idebug.eq.1)then
			  write(*,301) 
     $  irun_number,nev,isec,inanosec,iusec,v0_ev,v1_ev,v2_ev,
     $  chi_old,tof_ev,path

c	    write(*,*)' number of hits    ',n_b,n_m,n_u
c	    write(*,*)' number of clusters',n_bc,n_mc,n_uc
		do jj=1,n_b
		write(*,*)'hit bottom',jj,x_b(jj),y_b(jj),t_b(jj)
		enddo
		do jj=1,n_m
		write(*,*)'hit middle',jj,x_m(jj),y_m(jj),t_m(jj)
		enddo
		do jj=1,n_u
		write(*,*)'hit top',jj,x_u(jj),y_u(jj),t_u(jj)
		enddo
		
		do jj=1,n_bc
		write(*,*)'cluster bottom',jj,x_bc(jj),y_bc(jj),t_bc(jj)
		enddo
		do jj=1,n_mc
		write(*,*)'cluster middle',jj,x_mc(jj),y_mc(jj),t_mc(jj)
		enddo
		do jj=1,n_uc
		write(*,*)'cluster top',jj,x_uc(jj),y_uc(jj),t_uc(jj)
		enddo
		


		
c		write(*,*)ihit_b_l,ihit_b_r,ihit_m_l,ihit_m_r,ihit_t_l,ihit_t_r
	   do jj=1,192
	     if(t(jj).gt.0.) then
		 write(*,*)jj,t(jj)
		 endif
	   enddo
	   do jj=1,itdc1hits
	   write(*,*)itdc1ch(jj),itdc1time(jj),itdc1width(jj)
	   enddo
	   
	   do jj=1,itdc2hits
	   write(*,*)itdc2ch(jj),itdc2time(jj),itdc2width(jj)
	   enddo
	   endif


c
c
c Events with at least one chamber with 2 or more clusters
c
      if(n_bc.ge.2.or.n_mc.ge.2.or.n_uc.ge.2) then
        n_3clust=n_3clust+1
      endif

c
c Event with exactly 2 clusters in each chamber
c

      if(itrack_cand.gt.1)then
c	  write(*,*)' nev,itrack_cand',nev,itrack_cand
c pick out second best track
       if(idebug2.eq.1)then
	   do k=1,itrack_cand
	   write(*,*)
     $  ' track cand',k,' tof',tof_tc(k),istrip_b_tc(k),istrip_u_tc(k)
	   enddo
	   endif
	   i_tr_diff_old=0
	   do k=1,itrack_cand
	   if(k.ne.itr_cand_ev)then
	   itr_b_diff=0
	   itr_m_diff=0
	   itr_u_diff=0
	   if(istr_b.ne.istrip_b_tc(k))itr_b_diff=1
	   if(istr_m.ne.istrip_m_tc(k))itr_m_diff=1
	   if(istr_u.ne.istrip_u_tc(k))itr_u_diff=1
	   i_tr_diff=itr_b_diff+itr_m_diff+itr_u_diff
	   if(i_tr_diff.gt.i_tr_diff_old)i_tr_diff_old=i_tr_diff
	   endif
	   enddo
	   if(i_tr_diff_old.lt.2)goto 100
	   chi_old2=1000000000.
	   tof_limit=3.
	   itof_ev_cand=0
       if(idebug2.eq.1)write(*,*)' i_tr_diff_old', i_tr_diff_old
	   do k=1,itrack_cand
	   if(k.ne.itr_cand_ev)then
	   itr_b_diff=0
	   itr_m_diff=0
	   itr_u_diff=0
	   if(istr_b.ne.istrip_b_tc(k))itr_b_diff=1
	   if(istr_m.ne.istrip_m_tc(k))itr_m_diff=1
	   if(istr_u.ne.istrip_u_tc(k))itr_u_diff=1
	   i_tr_diff=itr_b_diff+itr_m_diff+itr_u_diff
	   if(idebug2.eq.1)write(*,*)' i_tr_diff,i_tr_diff_old',
     $ i_tr_diff,i_tr_diff_old 
	   if(i_tr_diff.eq.i_tr_diff_old)then
	   if(idebug2.eq.1)write(*,*)'k,chi_tc(k),chi_old2',
     $ k,chi_tc(k),chi_old2
	   if(chi_tc(k).lt.chi_old2)then
	   tof_test=abs(tof_tc(k)-atofd)
c	   if(tof_test.lt.tof_limit)then
	   tof_limit=tof_test
	   itof_ev_cand=k
c	   endif
	   chi_old2=chi_tc(k)
	   v0_ev2=v0_tc(k)
	   v1_ev2=v1_tc(k)
	   v2_ev2=v2_tc(k)
	   tof_ev2=tof_tc(k)
	   istr_b2=istrip_b_tc(k)
	   istr_m2=istrip_m_tc(k)
	   istr_u2=istrip_u_tc(k)
	   itr_cand_ev2=k
	   endif
	   endif
	   endif
	   enddo
	   if(idebug2.eq.1)write(*,*)' itr_cand_ev,itr_cand_ev2',
     $  itr_cand_ev,itr_cand_ev2
c
c  check that tof is ok
      if(idebug2.eq.1)write(*,*)' tof_ev2,atofd',
     $  tof_ev2,atofd
      if(abs(tof_ev2-atofd).gt.3.)then
	  if(itof_ev_cand.ne.0)then
	  k=itof_ev_cand
	   chi_old2=chi_tc(k)
	   v0_ev2=v0_tc(k)
	   v1_ev2=v1_tc(k)
	   v2_ev2=v2_tc(k)
	   tof_ev2=tof_tc(k)
	   istr_b2=istrip_b_tc(k)
	   istr_m2=istrip_m_tc(k)
	   istr_u2=istrip_u_tc(k)
	   itr_cand_ev2=k

	  endif
	  endif
 
	  
c      path2=sqrt(zzz*zzz*(1.+(v0_ev2*v0_ev2+v1_ev2*v1_ev2)))
	  vxy2=sqrt(v0_ev2*v0_ev2+v1_ev2*v1_ev2)
	  transverse2=(vxy/v2_ev)*zzz
	  path2=sqrt(transverse2*transverse2+zzz*zzz)
	  anglexy2=atan(v1_ev2/v0_ev2)
	  if(v0_ev.lt.0.)anglexy2=anglexy2+pi
	  anglexy2=anglexy2+angle
	  if(anglexy2.gt.2*pi)anglexy2=anglexy2-(2*pi)
	  v0_ev2=vxy2*cos(anglexy2)
	  v1_ev2=vxy2*sin(anglexy2)
	  if(chi_old2.gt.99.999)chi_old2=99.999
	  tof_out=tof_ev-atofcable
	  tof_out2=tof_ev2-atofcable
	  if(idebug2.eq.1)write(*,302)
     $  irun_number,nev,time_ev,iusec,v0_ev,v1_ev,v2_ev,
     $  chi_old,tof_ev,path,v0_ev2,v1_ev2,v2_ev2, 
     $  chi_old2,tof_ev2,path2

	
	  write(4,302) 
     $  irun_number,nev,isec,inanosec,iusec,v0_ev,v1_ev,v2_ev,
     $  chi_old,tof_out,path,v0_ev2,v1_ev2,v2_ev2, 
     $  chi_old2,tof_out2,path2
  302 format(1X,I5,1X,I10,1X,I10,1X,I10,1X,I12,F10.5,F10.5,F10.5,1X, 
     $  F8.5,1X,F10.3,1X,F10.2,F10.5,F10.5,F10.5,1X, 
     $  F8.5,1X,F10.3,1X,F10.2)
	  
	  
	  
c      if(n_bc.eq.2.and.n_mc.eq.2.and.n_uc.eq.2) then
c       write(2,*) delta_b,delta_m,delta_u
c      write(4,202) irun_number,nev,time_ev
202   format(1X,I5,1X,I10,1X,E28.20)	  
c      write(4,*) x_bc(1),y_bc(1),zb,x_bc(2),y_bc(2),zb,
c     *  x_mc(1),y_mc(1),zm,x_mc(2),y_mc(2),zm,
c     *  x_uc(1),y_uc(1),zu,x_uc(2),y_uc(2),zu
       n_2clust=n_2clust+1
c      endif
	  endif

 100  continue



c
c Event with more than 2 clusters in each chamber
c
c      if(n_b.eq.3.and.n_m.eq.3.and.n_u.eq.3.) then
       if(n_b.gt.2.and.n_m.gt.2.and.n_u.gt.2) then
        d12u=sqrt((x_u(1)-x_u(2))**2+(y_u(1)-y_u(2))**2)
        d13u=sqrt((x_u(1)-x_u(3))**2+(y_u(1)-y_u(3))**2)
        d23u=sqrt((x_u(2)-x_u(3))**2+(y_u(2)-y_u(3))**2)
        d12b=sqrt((x_b(1)-x_b(2))**2+(y_b(1)-y_b(2))**2)
        d13b=sqrt((x_b(1)-x_b(3))**2+(y_b(1)-y_b(3))**2)
        d23b=sqrt((x_b(2)-x_b(3))**2+(y_b(2)-y_b(3))**2)
        d12m=sqrt((x_m(1)-x_m(2))**2+(y_m(1)-y_m(2))**2)
        d13m=sqrt((x_m(1)-x_m(3))**2+(y_m(1)-y_m(3))**2)
        d23m=sqrt((x_m(2)-x_m(3))**2+(y_m(2)-y_m(3))**2)
        if(d12u.gt.10.and.d13u.gt.10.and.d23u.gt.10.and.
     *     d12b.gt.10.and.d13b.gt.10.and.d23b.gt.10.and.
     *     d12m.gt.10.and.d13m.gt.10.and.d23m.gt.10.) then
c         write(*,*) nev,(x_u(j),y_u(j),j=1,3)
c       write(*,*) nev,n_b,n_m,n_u
        endif
        
      endif


 2000 continue
c
c End of loop on events
c
c  just analyse one event
       go to 1236
c		go to 1235
2999  continue      
	  

      write(*,*) 'End of loop on events'
 3000 continue
c      close(1)
      close(2)
      close(3)
      close(4)
      close(10)
c
c Run summary
c
c      write(*,*) 'Output file name for run summary'
c      read(*,1) filesum
      open(unit=5,file=filesum,status='unknown')
      
      write(5,*) 'Analyzed events = ',n_tot
	  write(5,*)' GPS events',igps_event
      write(5,*)'****** Hit analysis ***************'
      write(5,*) 'Events with no hits in a chamber = ',n_nohits
      write(5,*) 'Events with 1 or 2 hits/chamber = ',n_2hits
      write(5,*) 'Event with more than 2 hits in a chamber = ',n_3hits
      write(5,*) 'Hits multiplicity chamber BOTTOM'
      do i=1,50
       if(mhits_bottom(i).ne.0) write(5,*) i,mhits_bottom(i)
      end do
      write(5,*) 'Hits multiplicity chamber MIDDLE'
      do i=1,50
       if(mhits_middle(i).ne.0) write(5,*) i,mhits_middle(i)
      end do
      write(5,*) 'Hits multiplicity chamber UP'
      do i=1,50
       if(mhits_up(i).ne.0) write(5,*) i,mhits_up(i)
      end do
      write(5,*) 'Hits total multiplicity'
      do i=1,50
       if(mhits_tot(i).ne.0) write(5,*) i,mhits_tot(i)
      end do
      
c
      write(5,*) '******** Cluster analysis ************'
      write(5,*) 'Events with 1 cluster in each chamber = ',n_1clust
      write(5,*) 'Events with >=2 clusters in a chamber = ',n_3clust
      write(5,*) 'Events with 2 clusters  in each chamber = ',n_2clust

      write(5,*) 'Cluster multiplicity chamber BOTTOM'
      do i=1,50
       if(mult_bottom(i).gt.0) write(5,*) i,mult_bottom(i)
      end do
      write(5,*) 'Cluster multiplicity chamber MIDDLE'
      do i=1,50
       if(mult_middle(i).gt.0) write(5,*) i,mult_middle(i)
      end do
      write(5,*) 'Cluster multiplicity chamber UP'
      do i=1,50
       if(mult_up(i).gt.0) write(5,*) i,mult_up(i)
      end do
      write(5,*) 'Cluster total multiplicity'
      do i=1,50
       if(mult_tot(i).gt.0) write(5,*) i,mult_tot(i)
      end do
	  
        write(5,*)' time cuts'
		write(5,*)' bottom chamber',
     $  tb_low_limit_left,tb_high_limit_left,
     $  tb_low_limit_right,tb_high_limit_right
		write(5,*)' middle chamber',
     $  tm_low_limit_left,tm_high_limit_left,
     $  tm_low_limit_right,tm_high_limit_right
		write(5,*)' top chamber',
     $  tt_low_limit_left,tt_high_limit_left,
     $  tt_low_limit_right,tt_high_limit_right
	  
	   if(n_time_br.gt.0)time_br=time_br/float(n_time_br)
	   if(n_time_bl.gt.0)time_bl=time_bl/float(n_time_bl)
	   if(n_time_mr.gt.0)time_mr=time_mr/float(n_time_mr)
	   if(n_time_ml.gt.0)time_ml=time_ml/float(n_time_ml)
	   if(n_time_ur.gt.0)time_ur=time_ur/float(n_time_ur)
	   if(n_time_ul.gt.0)time_ul=time_ul/float(n_time_ul)
	   write(5,*)' average time of hits - no cuts'
	   write(5,*)' bottomleft/right middleleft/right topleft/right'
	   write(5,*) time_bl,time_br,time_ml,time_mr,time_ul,time_ur
        tb_left=tb_left/float(n_tb_hits)
        tb_right=tb_right/float(n_tb_hits)
        tm_left=tm_left/float(n_tm_hits)
        tm_right=tm_right/float(n_tm_hits)
        tt_left=tt_left/float(n_tt_hits)
        tt_right=tt_right/float(n_tt_hits)
		
		write (5,*) "average time of hits" 
		
		write (5,*)" bottom", tb_left,tb_right,n_tb_hits
		write (5,*)" middle", tm_left,tm_right,n_tm_hits
		write (5,*)" top   ",tt_left,tt_right,n_tt_hits
		
	   x1_ra=x1_ra/float(n_x1)
	   x2_ra=x2_ra/float(n_x2)
	   x3_ra=x3_ra/float(n_x3)
	   write (5,*) ' average x ch bottom, ch middle, chamber top'
	   write (5,*) x1_ra,n_x1,x2_ra,n_x2,x3_ra,n_x3
	   write (5,*) 'out of range x coordinate'
	   write (5,*) n_xl1,n_xh1,n_xl2,n_xh2,n_xl3,n_xh3
c
c   open calibration file...
c
			if(n_x1.gt.100.and.n_x2.gt.100.and.n_x3.gt.100)then
		open(unit=20,file='eee_calib.txt',IOSTAT=ios,status='unknown')
		   if (ios.eq.0) then
		   if(icalib_exist.eq.1)then
		   t_b_corr=(78.-x1_ra)/10.+t_b_corr
		   t_m_corr=(78.-x2_ra)/10.+t_m_corr
		   t_t_corr=(78.-x3_ra)/10.+t_t_corr
		   else
		   t_b_corr=(78.-x1_ra)
		   t_m_corr=(78.-x2_ra)
		   t_t_corr=(78.-x3_ra)
		   			   endif

		   
		   tb_low_limit_left=tb_left-75.
		   tb_high_limit_left=tb_left+50.
		   tb_low_limit_right=tb_right-75.
		   tb_high_limit_right=tb_right+50.
		   
		   tm_low_limit_left=tm_left-75.
		   tm_high_limit_left=tm_left+50.
		   tm_low_limit_right=tm_right-75.
		   tm_high_limit_right=tm_right+50.
		   
		   tt_low_limit_left=tt_left-75.
		   tt_high_limit_left=tt_left+50.
		   tt_low_limit_right=tt_right-75.
		   tt_high_limit_right=tt_right+50.
		   write(20,*)t_b_corr,t_m_corr,t_t_corr
		   
		write(20,*)
     $  tb_low_limit_left,tb_high_limit_left,
     $  tb_low_limit_right,tb_high_limit_right
		write(20,*)
     $  tm_low_limit_left,tm_high_limit_left,
     $  tm_low_limit_right,tm_high_limit_right
		write(20,*)
     $  tt_low_limit_left,tt_high_limit_left,
     $  tt_low_limit_right,tt_high_limit_right
	         tb_left=tb_left/float(n_tb_hits)
        tb_right=tb_right/float(n_tb_hits)
        tm_left=tm_left/float(n_tm_hits)
        tm_right=tm_right/float(n_tm_hits)
        tt_left=tt_left/float(n_tt_hits)
        tt_right=tt_right/float(n_tt_hits)
		   
		   close(20)
		   endif
		   endif


		write(*,*) 'End of analysis'
      stop
      end
