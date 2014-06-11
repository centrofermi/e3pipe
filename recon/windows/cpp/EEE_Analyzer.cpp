#include <iostream>
#include <fstream>
#include <string>
#include <sstream>
#include <cmath>
#include <iomanip>
#include <bitset>
#include <stdint.h>


void openInput(std::string fileName, std::ifstream& input);
void reOpenInput(std::ifstream& input);
int readInput(std::ifstream& input, int*& data, int& type, int& error);
int read(std::ifstream& input, char*& buffer, int length);
void chambers(int& number, int difference, int iLeft, int iRight, float& left, float& right, int& numberOfHits, float* t, float* t2, int* iHitLeft, int* iHitRight, float timeOffset, float corr, float* xChamber, float* yChamber, float* tChamber);
void merge(int& number, int* iHitR, int* iHitL, int* iHitTL, int* iHitTR, float* xChamber, float* yChamber, float* tChamber);

/*
* Rules:
*
* 1 = sizeof(char) <= sizeof(short) <= sizeof(int) <= sizeof(long)
* sizeof(float) <= sizeof(double) <= sizeof(double)
*/


const int sizeOfInt = (sizeof(int) > 4) ? (sizeof(int)) : (4);

int main(int argc, char** argv)
{
	//std::cout << "*****  Analysis of run EEE  ******" << std::endl << std::endl;
	//Parameter checking
	if (argc < 2)
	{
		//std::cout << "You must specify a binary file to analyse" << std::endl << ":e.g.  EEE_V15 inputfile.bin" << std::endl;
		return (-1);
	}

	//The first argument has to be a binary file
	std::string fileName(argv[1]);
	if (fileName.compare(fileName.length() - 4, 4, ".bin") != 0)
	{
		//std::cout << "The input file must be binary" << std::endl << "and have the extension .bin";
		return (-1);
	}
	//std::cout << "Input file name is " << fileName << std::endl;

	//It has to contain the run number too.
	int runNumber = atoi(fileName.substr(fileName.length() - 8, 4).c_str());
	if (runNumber == 0)
	{
		//std::cout << "The input file must contain the run number" << std::endl;
		return (-1);
	}

	//Checking the second argument
	int numberOfEvent = 0;
	if (argc > 2)
	{
		//if is not a number, numberOfEvent will be zero.
		numberOfEvent = atoi(argv[2]);
	}

	std::ifstream inputFile;
	//iopenfile(const_cast<char*>(fileName.c_str()), 0);
	openInput(fileName, inputFile);

	std::ofstream outputFileOUT(fileName.substr(0, fileName.length() - 3) + "out");
	std::ofstream outputFileTIM(fileName.substr(0, fileName.length() - 3) + "tim");
	std::ofstream outputFile2TT(fileName.substr(0, fileName.length() - 3) + "2tt");
	std::ofstream outputFileSUM(fileName.substr(0, fileName.length() - 3) + "sum");

	std::ifstream inputCalib("eee_calib.txt");

	float tbCorr = 0, tmCorr = 0, ttCorr = 0;
	float tbLowLimitLeft, tbHighLimitLeft, tbLowLimitRight, tbHighLimitRight, ibLeft, ibRight;
	float tmLowLimitLeft, tmHighLimitLeft, tmLowLimitRight, tmHighLimitRight, imLeft, imRight;
	float ttLowLimitLeft, ttHighLimitLeft, ttLowLimitRight, ttHighLimitRight, itLeft, itRight;
	float tbLeft = 0, tbRight = 0, tmLeft = 0, tmRight = 0, ttLeft = 0, ttRight = 0;
	double tDelay;

	float zzB = 0, zzM, zzT; // distances
	float PI = std::acos(-1.), angle;

	float iword, atofCable, atofD, atofDLow, atofDHigh;
	float timeOffsetB, timeOffsetM, timeOffsetT;
	int iHitBL[24], iHitBR[24], iHitML[24], iHitMR[24], iHitTL[24], iHitTR[24];
	float xB[24], yB[24], tB[24], xM[24], yM[24], tM[24], xT[24], yT[24], tT[24];

	float xBRA = 0, xMRA = 0, xTRA = 0;
	int numberxBRA = 0, numberxMRA = 0, numberxTRA = 0;
	int numberxBLow = 0, numberxBHigh = 0, numberxMLow = 0, numberxMHigh = 0, numberxTLow = 0, numberxTHigh = 0;
	int numberOftbHits = 0, numberOftmHits = 0, numberOfttHits = 0;

	//for statistic
	int mHitsB[50], mHitsM[50], mHitsT[50], mHitsTotal[50];
	int mClusB[50], mClusM[50], mClusT[50], mClusTotal[50];
	int numberOf3Hits = 0, numberOf2Hits = 0, number1Clust = 0, numberOf3Clust = 0, numberOf2Clust = 0;


	int timeBR = 0, nTimeBR = 0;
	int timeBL = 0, nTimeBL = 0;
	int timeTR = 0, nTimeTR = 0;
	int timeTL = 0, nTimeTL = 0;
	int timeMR = 0, nTimeMR = 0;
	int timeML = 0, nTimeML = 0;

	long helper = 0;

	//From the modified Fortran code:
	float time_track[20], track_time = 0;
	int iwindow_start;

	outputFile2TT << " run_number,event_number,secs_since_1.1.2007,nanosecs,microseconds_since_start_of_run track1: unit_vector_x,unit_vector_y,unit_vector_z,chi_squared,time of flight[ns],track length[cm],track2: unit_vector_x,unit_vector_y,unit_vector_z,chi_squared,time of flight[ns],track length[cm]" << std::endl;
	outputFileOUT << " run_number,event_number,secs_since_1.1.2007,nanosec,microseconds_since_start_of_run track: unit_vector_x,unit_vector_y,unit_vector_z,chi_squared,time of flight[ns],track length[cm]" << std::endl;
	outputFileTIM << " run_number,event_number,event_time secs since 1.1.2007,nanosec" << std::endl;

	for (int i = 0; i < 50; i++)
	{
		mHitsB[i] = 0; mHitsM[i] = 0; mHitsT[i] = 0; mHitsTotal[i] = 0;
		mClusB[i] = 0; mClusM[i] = 0; mClusT[i] = 0; mClusTotal[i] = 0;
	}

	if (inputCalib.is_open())
	{
		inputCalib >> tbCorr >> tmCorr >> ttCorr
			>> tbLowLimitLeft >> tbHighLimitLeft >> tbLowLimitRight >> tbHighLimitRight
			>> tmLowLimitLeft >> tmHighLimitLeft >> tmLowLimitRight >> tmHighLimitRight
			>> ttLowLimitLeft >> ttHighLimitLeft >> ttLowLimitRight >> ttHighLimitRight;
	}

	int iGeo = 0;
	bool geometry = false; bool wad = false;
	while (iGeo < 10 && (!geometry || !wad))
	{
		int *data = NULL;
		//int data[1000];
		int type, error;
		int retVal = readInput(inputFile, data, type, error);
		int nwords;
		//int retVal = iread_file(&nwords, &type, data, &error);

		switch (type)
		{
		case 6:
		{
			wad = true;
			tDelay = ((double)data[4]) / 1000000000.0;

			//std::cout << "data for delay: " << data[4] << std::endl;

			//From the modified Fortran code:
			iwindow_start = data[1];
			break;
		}
		case 5:
		{
			geometry = true;
			angle = PI*((float)data[0] / 100) / 180;

			zzM = (float)data[1]; zzT = (float)data[2] + zzM;
			ibLeft = data[9]; ibRight = data[10];
			imLeft = data[11]; imRight = data[12];
			itLeft = data[13]; itRight = data[14];
			iword = data[16];

			float iCableBLeft = data[3]; float iCableBRight = data[4];
			float iCableMLeft = data[5]; float iCableMRight = data[6];
			float iCableTLeft = data[7]; float iCableTRight = data[8];

			float iCableB = iCableBLeft + iCableBRight;
			float iCableT = iCableTLeft + iCableTRight;

			atofCable = (float(iCableB - iCableT)) / 40;
			atofD = ((float)data[1] + (float)data[2]) / 30 + atofCable;
			atofDLow = atofD - 3;
			atofDHigh = atofD + 3;

			if (!inputCalib.is_open())
			{
				tbLowLimitLeft = 100; 	tbHighLimitLeft = 600; tbLowLimitRight = 100; tbHighLimitRight = 600;
				tmLowLimitLeft = 100;  tmHighLimitLeft = 600; tmLowLimitRight = 100; tmHighLimitRight = 600;
				ttLowLimitLeft = 100;  ttHighLimitLeft = 600; ttLowLimitRight = 100; ttHighLimitRight = 600;
			}

			timeOffsetB = (iCableBLeft - iCableBRight)*0.0536;
			timeOffsetM = (iCableMLeft - iCableMRight)*0.0536;
			timeOffsetT = (iCableTLeft - iCableTRight)*0.0536;
			break;
		}

		}
		delete[] data;

		iGeo++;
	}
	if (iGeo == 10)
	{
		if (!geometry)
		{
			//std::cout << "Have not found geometry data block in"  << std::endl << "first 10 blocks of data-something is wrong" << std::endl;
		}

		if (!wad)
		{
			//std::cout << "Have not found wad data block in" << std::endl << "first 10 blocks of data-something is wrong" << std::endl;
		}

	}

	int iGPSEvent = 0;
	int type;
	int iCalib[2], iCalibNew[2];

	do
	{
		int* data = NULL;
		//int data[1000];
		int error;

		//int pos = inputFile.tellg();

		int read = readInput(inputFile, data, type, error);

		int nwords;
		//int read = iread_file(&nwords, &type, data, &error);

		//pos = inputFile.tellg();

		if (type == 0)
			if (iGPSEvent == 1)
			{
			//std::cout << "Have found initial gps event" << std::endl;
			reOpenInput(inputFile);
			//irewind();
			}
			else
			{
				iGPSEvent = 1;
				type = -1;
			}
		if (type == 1 || type == 2)
			iCalib[type - 1] = data[2];

		delete[] data;

	} while (iGPSEvent != 1 || type != 0);

	int currentEvent = 0;
	int iTimeEvent = 0;
	int numberOfNoHits = 0;

	//reading data from input
	int error = 0;
	int* data = NULL;
	//int data[1000];

	//time
	int tns, sec, day, year;
	int nEvent1, tns1, nEvent2, tns2;

	int retVal = readInput(inputFile, data, type, error);

	int nwords;
	//int retVal = iread_file(&nwords, &type, data, &error);

	iGPSEvent = 0;
	bool firstDBOut = false; int countDB = 0;

	while ((currentEvent < numberOfEvent || numberOfEvent == 0) && error == 0)
	{
		int numberOfiHitBL = 0, numberOfiHitBR = 0;
		int numberOfiHitML = 0, numberOfiHitMR = 0;
		int numberOfiHitTL = 0, numberOfiHitTR = 0;

		bool logical = false;

		int iHit[192];
		float t[192], t2[192];

		for (int i = 0; i < 192; i++)
		{
			iHit[i] = 0;
			t[i] = 0.;
			t2[i] = 0.;
		}

		while (error == 0 && !logical)
		{
			switch (type)
			{
			case 0:
			{
				tns = data[0];
				sec = data[1];
				day = data[2];
				year = data[3] - 2007;
				day += 365 * year;

				if (currentEvent != 0)
				{
					for (int i = 0; i < 2; i++)
						iCalib[i] = iCalibNew[i];
				}
				for (int i = 0; i < year; i++)
				{
					if ((i + 2007) % 4 == 0)
						day++;
				}
				iGPSEvent++;

				break;
			}
			case 1:
			{
				nEvent1 = data[0];
				iCalibNew[0] = data[2];
				tns1 = data[2];

				helper += data[1];

				for (int i = 0; i < data[1]; i++)
				{
					int k = (i + 1) * 3;
					float timeHit = float(data[k + 1]) / 10;
					if (data[k] > 0 && data[k] < 25)
					{
						//Right Bottom Hit
						if (iHit[k] == 0)
						{
							iHit[k] = 1;
							timeBR += timeHit;
							nTimeBR++;
						}
						if (timeHit >= tbLowLimitRight && timeHit < tbHighLimitRight)
						{
							if (t[data[k]] == 0)
							{
								t[data[k]] = timeHit;
								numberOfiHitBR++;
							}
							else
							{
								t2[data[k]] = (t2[data[k]] == 0) ? (timeHit) : (t2[data[k]]);
							}
						}
					}
					if (data[k] > 32 && data[k] < 57)
					{
						//Left Bottom Hit
						if (iHit[k] == 0)
						{
							iHit[k] = 1;
							timeBL += timeHit;
							nTimeBL++;
						}
						if (timeHit >= tbLowLimitLeft && timeHit < tbHighLimitLeft)
						{
							if (t[data[k]] == 0)
							{
								t[data[k]] = timeHit;
								numberOfiHitBL++;
							}
							else
							{
								t2[data[k]] = (t2[data[k]] == 0) ? (timeHit) : (t2[data[k]]);
							}
						}
					}
					if (data[k] > 64 && data[k] < 89)
					{
						//Right Top Hit
						if (iHit[k] == 0)
						{
							iHit[k] = 1;
							timeTR += timeHit;
							nTimeTR++;
						}
						if (timeHit >= ttLowLimitRight && timeHit < ttHighLimitRight)
						{
							if (t[data[k]] == 0)
							{
								t[data[k]] = timeHit;
								numberOfiHitTR++;
							}
							else
							{
								t2[data[k]] = (t2[data[k]] == 0) ? (timeHit) : (t2[data[k]]);
							}
						}
					}
					if (data[k] > 96 && data[k] < 121)
					{
						//Left Top Hit
						if (iHit[k] == 0)
						{
							iHit[k] = 1;
							timeTL += timeHit;
							nTimeTL++;
						}
						if (timeHit >= ttLowLimitLeft && timeHit < ttHighLimitLeft)
						{
							if (t[data[k]] == 0)
							{
								t[data[k]] = timeHit;
								numberOfiHitTL++;
							}
							else
							{
								t2[data[k]] = (t2[data[k]] == 0) ? (timeHit) : (t2[data[k]]);
							}
						}
					}
				}
				break;
			}//end of case 1
			case 2:
			{
				nEvent2 = data[0];
				iCalibNew[1] = data[2];
				tns2 = data[2];
				for (int i = 0; i < data[1]; i++)
				{
					int k = (i + 1) * 3;
					float timeHit = float(data[k + 1]) / 10;
					if (data[k] > 0 && data[k] < 25)
					{
						if (iHit[k] == 0)
						{
							iHit[k] = 1;
							timeMR += timeHit;
							nTimeMR++;
						}
						//Right Middle Hit
						if (timeHit >= tmLowLimitRight && timeHit < tmHighLimitRight)
						{
							if (t[data[k] + 128] == 0)
							{
								t[data[k] + 128] = timeHit;
								numberOfiHitMR++;
							}
							else
							{
								t2[data[k] + 128] = (t2[data[k] + 128] == 0) ? (timeHit) : (t2[data[k] + 128]);
							}
						}
					}
					if (data[k] > 32 && data[k] < 57)
					{
						//Left Middle Hit
						if (iHit[k] == 0)
						{
							iHit[k] = 1;
							timeML += timeHit;
							nTimeML++;
						}
						if (timeHit >= tmLowLimitLeft && timeHit < tmHighLimitLeft)
						{
							if (t[data[k] + 128] == 0)
							{
								t[data[k] + 128] = timeHit;
								numberOfiHitML++;
							}
							else
							{
								t2[data[k] + 128] = (t2[data[k] + 128] == 0) ? (timeHit) : (t2[data[k] + 128]);
							}
						}
					}
				}
				logical = true;
				//end of case 2
				break;
			}
			}
			delete[] data;

			retVal = readInput(inputFile, data, type, error);

			int nwords;
			//int retVal = iread_file(&nwords, &type, data, &error);

		}

		//Analyization

		currentEvent++;

		//float to double except first
		double timeEvent = (day - 1) * 86400 + sec + ((double)tns) / 1000000000;

		double v1 = (double)tns1 / (double)iCalib[0];
		v1 = v1 * 10E14;
		double f = v1 / 10E14;

		v1 = (double)tns2 / (double)iCalib[1];
		v1 = v1 * 10E14;
		f += v1 / 10E14;
		
		double tstdc = (1.000001 - tDelay)*(f)*0.5;

		tstdc -= 0.000001;

		timeEvent += tstdc;

		int te2i = (int)timeEvent;

		double nt = ((tstdc * 1000000000 + ((double)tns)) / 1000000000) * 10E14;

		timeEvent = te2i + (double)nt / 10E14;

		if (currentEvent == 1)
		{
			iTimeEvent = timeEvent;
		}

		//float to double
		double timeDiff = (double)(te2i - iTimeEvent);
		timeDiff += (double)nt / 10E14;
		//std::cout << "TIMEDIFF: " << static_cast<float>(timeDiff) << std::endl;
		unsigned long long iTimeDiff = /*(long int)*/(timeDiff * 1000000); 			//iusec=ifix(usec*1000000)

		int iSec = (int)timeEvent;

		double valnew = ((double)tns) + tstdc * 1000000000;

		//		unsigned long long nt = valnew * 10E14;

		double aNanoSec = valnew; // (double)nt / 10E14; //(timeEvent - iSec);

		unsigned long long iNanoSec = (unsigned long long)aNanoSec;

		int NumberOfHits = numberOfiHitBL*numberOfiHitBR*numberOfiHitML*numberOfiHitMR*numberOfiHitTL*numberOfiHitTR;
		if (NumberOfHits != 0)
		{
			int numberB = 0, numberM = 0, numberT = 0;
			outputFileTIM.width(10);
			outputFileTIM << runNumber << std::setw(15) << currentEvent - 1 << std::setw(16) << iSec << std::setw(16) << iNanoSec << std::endl;
			//3 chambers function
			chambers(numberB, 0, ibLeft, ibRight, tbLeft, tbRight, numberOftbHits, t, t2, iHitBL, iHitBR, timeOffsetB, tbCorr, xB, yB, tB);
			chambers(numberM, 128, imLeft, imRight, tmLeft, tmRight, numberOftmHits, t, t2, iHitML, iHitMR, timeOffsetM, tmCorr, xM, yM, tM);
			chambers(numberT, 64, itLeft, itRight, ttLeft, ttRight, numberOfttHits, t, t2, iHitTL, iHitTR, timeOffsetT, ttCorr, xT, yT, tT);

			int iGood = 0;
			int iGoodB[24], iGoodM[24], iGoodT[24];

			for (int j = 0; j < 24; j++)
			{
				iGoodB[j] = 0;
				iGoodM[j] = 0;
				iGoodT[j] = 0;
			}

			if (numberB > 1 || numberT > 1)
			{
				for (int iB = 0; iB < numberB; iB++)
				{
					for (int iT = 0; iT < numberT; iT++)
					{
						float tofD = tB[iB] - tT[iT];
						if (tofD > atofDLow && tofD < atofDHigh)
						{
							iGood = 1;
							iGoodB[iB] = 1;
							iGoodT[iT] = 1;
						}
					}
				}

				if (iGood == 1)
				{
					int iB = 1;
					bool logForMerge = false;
					while (numberB > 1 && !logForMerge)
					{
						for (int j = 0; j < numberB; j++)
						{
							int before = 0, after = 0;
							if (iGoodB[j] == 1)
							{
								if (j > 0)
								{
									if (std::abs(yB[j - 1] - yB[j]) < 3.5)
										before = 1;
								}
								if (j < numberB - 1)
								{
									if (std::abs(yB[j + 1] - yB[j]) < 3.5)
										after = 1;
								}

								if (after == 0 && before == 1)
								{
									yB[j] = (yB[j - 1] + yB[j]) / 2;
								}
								if (after == 1 && before == 0)
								{
									yB[j] = (yB[j + 1] + yB[j]) / 2;
								}
							}
						}
						currentEvent;
						if (iB <= numberB)
						{
							if (iGoodB[iB - 1] == 0 && numberB > iB)
							{
								for (int j = iB - 1; j < numberB - 1; j++)
								{
									yB[j] = yB[j + 1];
									xB[j] = xB[j + 1];
									tB[j] = tB[j + 1];

									iGoodB[j] = iGoodB[j + 1];
									iHitBR[j] = iHitBR[j + 1];
									iHitBL[j] = iHitBL[j + 1];
								}
								numberB--;
								iB--;
							}
							iB++;
						}
						else
						{
							logForMerge = true;
						}
					}
					int iT = 1;
					logForMerge = false;

					while (numberT > 1 && !logForMerge)
					{
						for (int j = 0; j < numberT; j++)
						{
							int before = 0, after = 0;
							if (iGoodT[j] == 1)
							{
								if (j > 0)
								{
									if (std::abs(yT[j - 1] - yT[j]) < 3.5)
										before = 1;
								}
								if (j < numberT - 1)
								{
									if (std::abs(yT[j + 1] - yT[j]) < 3.5)
										after = 1;
								}

								if (after == 0 && before == 1)
								{
									yT[j] = (yT[j - 1] + yT[j]) / 2;
								}

								if (after == 1 && before == 0)
								{
									yT[j] = (yT[j + 1] + yT[j]) / 2;
								}
							}
						}

						if (iT <= numberT)
						{
							if (iGoodT[iT - 1] == 0 && numberT > iT)
							{
								for (int j = iT - 1; j < numberT - 1; j++)
								{
									yT[j] = yT[j + 1];
									xT[j] = xT[j + 1];
									tT[j] = tT[j + 1];

									iGoodT[j] = iGoodT[j + 1];
									iHitTR[j] = iHitTR[j + 1];
									iHitTL[j] = iHitTL[j + 1];
								}
								numberT--;
								iT--;
							}
							iT++;
						}
						else
						{
							logForMerge = true;
						}
					}
				}
			}

			//merge
			merge(numberB, iHitBL, iHitBR, iHitTL, iHitTR, xB, yB, tB);
			merge(numberM, iHitML, iHitMR, iHitTL, iHitTR, xM, yM, tM);
			merge(numberT, iHitTL, iHitTR, iHitTL, iHitTR, xT, yT, tT);



			/*
			* Hits multiplicity
			*/

			int total = numberB + numberM + numberT;

			if (numberB > 0 && numberB < 50)
				mHitsB[numberB - 1]++;
			if (numberM > 0 && numberM < 50)
				mHitsM[numberM - 1]++;
			if (numberT > 0 && numberT < 50)
				mHitsT[numberT - 1]++;
			if (total > 0 && total < 50)
				mHitsTotal[total - 1]++;

			numberOf3Hits = (numberB > 2 || numberM > 2 || numberT > 2) ? (numberOf3Hits + 1) : (numberOf3Hits);

			if (numberB*numberM*numberT != 0)
			{
				numberOf2Hits++;

				int clusterTotal = numberB + numberM + numberT;

				mClusB[numberB - 1]++;
				mClusM[numberM - 1]++;
				mClusT[numberT - 1]++;
				mClusTotal[clusterTotal - 1]++;

				float tofOld = 1000;
				int trackCand = 0;
				float chiTC[20], v0TC[20], v1TC[20], v2TC[20], tofTC[20];
				int stripBTC[20], stripMTC[20], stripTTC[20];

				float zzz, chi2;
				float chiOld, v0Event, v1Event, v2Event, tofEvent;
				int strB, strM, strT, place;

				float chiOld2, v0Event2, v1Event2, v2Event2, tofEvent2;
				int strB2, strM2, strT2, place2;


				for (int i = 0; i < numberB; i++)
				{
					for (int j = 0; j < numberM; j++)
					{
						for (int k = 0; k < numberT; k++)
						{
							if (numberB == 1 && numberM == 1 && numberT == 1)
								number1Clust++;
							/*
							* Reconstruction of angles theta,phi
							* Fit of the 3 clusters through straight lines in plane x-z,  y-z
							* distance between chambers=80 cm
							*/

							float xxB = xB[i];	 float yyB = yB[i];
							float xxM = xM[j];	 float yyM = yM[j];
							float xxT = xT[k];	 float yyT = yT[k];

							/*
							* Select only physical coordinates within chambers
							* To evaluate space resolution compare position extrapolated from UP/BOTTOM
							* chambers to position found in MIDDLE chamber
							* keep track of running averages and x positions out of range
							*/

							xBRA += xxB; numberxBRA++;
							xMRA += xxM; numberxMRA++;
							xTRA += xxT; numberxTRA++;

							if (xxB < 0)
								numberxBLow++;
							if (xxB > 158)
								numberxBHigh++;

							if (xxM < 0)
								numberxMLow++;
							if (xxM > 158)
								numberxMHigh++;

							if (xxT < 0)
								numberxTLow++;
							if (xxT > 158)
								numberxTHigh++;

							float sumX = xxB + xxM + xxT;
							float sumY = yyB + yyM + yyT;
							float sumZ = zzB + zzM + zzT;

							float sXZ = xxB*zzB + xxM*zzM + xxT*zzT;
							float sYZ = yyB*zzB + yyM*zzM + yyT*zzT;
							float sX2 = xxB*xxB + xxM*xxM + xxT*xxT;
							float sY2 = yyB*yyB + yyM*yyM + yyT*yyT;
							float sZ2 = zzB*zzB + zzM*zzM + zzT*zzT;
							float sumZ2 = sumZ*sumZ;

							float denX = 3 * sX2 - sumX*sumX;
							float denY = 3 * sY2 - sumY*sumY;

							float a = (3 * sXZ - sumX*sumZ) / denX;
							float b = (sX2*sumZ - sumX*sXZ) / denX;
							float c = (3 * sYZ - sumY*sumZ) / denY;
							float d = (sY2*sumZ - sumY*sYZ) / denY;

							float chi2XZ = std::pow((zzB - a*xxB - b), 2) + std::pow((zzM - a*xxM - b), 2) + std::pow((zzT - a*xxT - b), 2);
							float chi2YZ = std::pow((zzB - c*yyB - d), 2) + std::pow((zzM - c*yyM - d), 2) + std::pow((zzT - c*yyT - d), 2);

							/*
							* phif = angle extracted from fit
							* phi  = angle extracted from only 2 clusters (in bottom and up chambers)
							*/

							float phif = std::atan(a / c)*(180. / PI);
							float phi = std::atan((yyT - yyB) / (xxT - xxB)) * (180. / PI);

							if (((yyT - yyB) < 0 && (xxT - xxB) < 0) || ((yyT - yyB) > 0 && (xxT - xxB) < 0))
							{
								phi += 180;
								phif += 180;
							}
							if ((yyT - yyB) < 0 && (xxT - xxB) > 0)
							{
								phi = 360. - std::abs(phi);
								phif = 360. - std::abs(phif);
							}

							/*
							* Fit procedure in the 3D-space
							*/

							float p0 = (3.*sXZ - sumX*sumZ) / (3.*sZ2 - sumZ2);
							float p1 = (sumX - p0*sumZ) / 3.;
							float p2 = (3.*sYZ - sumY*sumZ) / (3.*sZ2 - sumZ2);
							float p3 = (sumY - p2*sumZ) / 3.;

							float n0 = p0 / std::sqrt(1. + p0*p0 + p2*p2);
							float n1 = p2 / std::sqrt(1. + p0*p0 + p2*p2);
							float n2 = 1. / sqrt(1. + p0*p0 + p2*p2);

							//teta3 and phi3 are useless

							zzz = n0*n0 + n1*n1 + n2*n2;

							/*
							* Evaluation of distances between points and line in 3D-space
							*/

							float dd = std::sqrt(zzz);

							float axB = n2*(yyB - p3) - n1*zzB;
							float ayB = -1 * n2 * (xxB - p1) + n0 * zzB;
							float azB = n1 * (xxB - p1) - n0*(yyB - p3);
							float distB = std::sqrt(std::pow(axB, 2) + std::pow(ayB, 2) + std::pow(azB, 2)) / dd;

							float axM = n2*(yyM - p3) - n1*zzM;
							float ayM = -1 * n2 * (xxM - p1) + n0 * zzM;
							float azM = n1 * (xxM - p1) - n0*(yyM - p3);
							float distM = std::sqrt(std::pow(axM, 2) + std::pow(ayM, 2) + std::pow(azM, 2)) / dd;

							float axT = n2*(yyT - p3) - n1*zzT;
							float ayT = -1 * n2 * (xxT - p1) + n0 * zzT;
							float azT = n1 * (xxT - p1) - n0*(yyT - p3);
							float distT = std::sqrt(std::pow(axT, 2) + std::pow(ayT, 2) + std::pow(azT, 2)) / dd;

							chi2 = std::sqrt(std::pow(distB, 2) + std::pow(distM, 2) + std::pow(distT, 2));

							if (trackCand < 20)
							{
								chiTC[trackCand] = chi2;

								v0TC[trackCand] = n0;
								v1TC[trackCand] = n1;
								v2TC[trackCand] = n2;

								tofTC[trackCand] = tB[i] - tT[k];

								//Next line from modified Fortran code:
								time_track[trackCand] = (tB[i] + tT[k]) / 2;

								stripBTC[trackCand] = iHitBR[i];
								stripMTC[trackCand] = iHitMR[i];
								stripTTC[trackCand] = iHitTR[i];
								trackCand++;
							}
						}
					}
				}

				//different solution for selecting the best trajectory
				//pick up the lowest chi2 with good tof

				/*bool log = false;
				int minPlace = -1;

				int iCand = 0;
				while (iCand < trackCand)
				{
				if ((tofTC[iCand] - atofD) < 3)
				{
				if (!log)
				{
				log = true;
				minPlace = iCand;
				}
				else
				{
				if (chiTC[minPlace] > chiTC[iCand])
				{
				minPlace = iCand;
				}
				}
				}
				iCand++;
				}*/

				int minPlace = 0;
				for (int iCand = 1; iCand < trackCand; iCand++)
				{
					if (chiTC[minPlace] > chiTC[iCand])
						minPlace = iCand;
				}

				/*				if (std::abs(std::abs(tofTC[minPlace]) - atofD) >= 3)
				{
				int minPlace2 = -1;
				int iCand = 0;
				bool log = false;

				while (iCand < trackCand)
				{
				if (std::abs(std::abs(tofTC[iCand]) - atofD) < 3)
				{
				if (!log)
				{
				log = true;
				minPlace2 = iCand;
				}
				else
				{
				if (std::abs(std::abs(tofTC[iCand]) - atofD) < std::abs(std::abs(tofTC[minPlace2]) - atofD))
				{
				minPlace2 = iCand;
				}
				}
				}
				iCand++;
				}
				if (log)
				{
				minPlace = minPlace2;
				}

				}*/
				if (true)
				{
					chiOld = chiTC[minPlace];
					v0Event = v0TC[minPlace];
					v1Event = v1TC[minPlace];
					v2Event = v2TC[minPlace];
					////std::cout << std::setprecision(15) << tofTC[minPlace] << std::endl;
					tofEvent = tofTC[minPlace];

					/*for (int i = 0; i < 20; ++i)
					//std::cout << std::setprecision(20) << tofTC[i] << std::endl;
					return 1111;
					*/

					//Next line from modified Fortran code:
					track_time = time_track[minPlace];

					strB = stripBTC[minPlace];
					strM = stripMTC[minPlace];
					strT = stripTTC[minPlace];
					place = minPlace;
				}

				// check that tof if ok
				if (abs(tofEvent - atofD) > 3.)
				{
					// tof not OK... check if there are candidates with better tof
					float tof_old = 3.;
					for (int k = 0; k < trackCand; ++k)
					{
						float tof_cand = abs(tofTC[k] - atofD);
						if (tof_cand < tof_old)
						{
							tof_old = tof_cand;
							chiOld = chiTC[k];
							v0Event = v0TC[k];
							v1Event = v1TC[k];
							v2Event = v2TC[k];
							tofEvent = tofTC[k];
							track_time = time_track[k];
							strB = stripBTC[k];
							strM = stripMTC[k];
							strT = stripTTC[k];
							place = k;
						}
					}


				}

				zzz = zzT - zzB;

				////std::cout << v0Event << " " << strB << std::endl;

				float vxy = std::sqrt(std::pow(v0Event, 2) + std::pow(v1Event, 2));
				float transverse = (vxy / v2Event) * zzz;
				float path = std::sqrt(std::pow(transverse, 2) + std::pow(zzz, 2));
				float angleXY = std::atan(v1Event / v0Event);
				if (v0Event < 0)
					angleXY += PI;
				angleXY += angle;
				if (angleXY > 2 * PI)
					angleXY -= 2 * PI;
				v0Event = vxy*std::cos(angleXY);
				v1Event = vxy*std::sin(angleXY);
				if (chiOld > 99.999)
					chiOld = 99.999;

				//Next two line added by Richard
				float tofOut;
				tofOut = tofEvent - atofCable;

				iNanoSec += (int)track_time + iwindow_start;

				//printing out - output
				if (true)
				{
					outputFileOUT << runNumber << std::setw(15) << currentEvent - 1 << std::setw(15) << iSec << std::setw(15) << iNanoSec << std::setw(15)
						<< iTimeDiff << std::setw(15) << v0Event << std::setw(15) << v1Event << std::setw(15) << v2Event << std::setw(15)
					<< chiOld << std::setw(15) << /*tofEvent*/ tofOut << std::setw(15) << path << std::endl;
				}
				/*
				* Events with at least one chamber with 2 or more clusters
				*/

				if (numberB > 2 || numberM > 2 || numberT > 2)
				{
					numberOf3Clust++;
				}
				/*
				* Event with exactly 2 clusters in each chamber
				*/

				if (trackCand > 1)
				{
					int trDiffOld = 0;

					for (int i = 0; i < trackCand; i++)
					{
						if (i != place)
						{
							int trBDiff = 0, trMDiff = 0, trTDiff = 0;

							if (strB != stripBTC[i])
								trBDiff++;
							if (strM != stripMTC[i])
								trMDiff++;
							if (strT != stripTTC[i])
								trTDiff++;
							int trDiff = trBDiff + trMDiff + trTDiff;
							if (trDiff > trDiffOld)
								trDiffOld = trDiff;
						}
					}
					if (trDiffOld >= 2)
					{
						bool log = false;
						minPlace = -1;

						for (int i = 0; i < trackCand; i++)
						{
							if (i != place)
							{
								int trDiff = 0;

								trDiff += (strB != stripBTC[i]) ? (1) : (0);
								trDiff += (strM != stripMTC[i]) ? (1) : (0);
								trDiff += (strT != stripTTC[i]) ? (1) : (0);

								if (trDiff == trDiffOld)
								{
									if (!log)
									{
										log = true;
										minPlace = i;
									}
									else
									{
										if (chiTC[i] < chiTC[minPlace])
										{
											minPlace = i;
										}
									}
								}
							}
						}
						if (!log)
						{
							std::cerr << "There is some problem with finding ch2" << std::endl;
						}
						else
						{
							chiOld2 = chiTC[minPlace];
							v0Event2 = v0TC[minPlace];
							v1Event2 = v1TC[minPlace];
							v2Event2 = v2TC[minPlace];
							tofEvent2 = tofTC[minPlace];

							//Next line from modified Fortran code:
							track_time = time_track[minPlace];

							strB2 = stripBTC[minPlace];
							strM2 = stripMTC[minPlace];
							strT2 = stripTTC[minPlace];
							place2 = minPlace;
						}

						float vxy2 = std::sqrt(std::pow(v0Event2, 2) + std::pow(v1Event2, 2));
						float transverse2 = (vxy2 / v2Event) * zzz;
						float path2 = std::sqrt(std::pow(transverse2, 2) + std::pow(zzz, 2));
						float angleXY2 = std::atan(v1Event2 / v0Event2);
						if (v0Event2 < 0)
							angleXY2 += PI;
						angleXY += angle;
						if (angleXY2 > 2 * PI)
							angleXY2 -= 2 * PI;
						v0Event2 = vxy2*std::cos(angleXY2);
						v1Event2 = vxy2*std::sin(angleXY2);
						if (chiOld2 > 99.999)
							chiOld2 = 99.999;

						//printing out - output2TT

						outputFile2TT << runNumber << std::setw(15) << currentEvent << std::setw(15) << iSec << std::setw(15) << iNanoSec << std::setw(15)
							<< iTimeDiff << std::setw(15) << v0Event << std::setw(15) << v1Event << std::setw(15) << v2Event << std::setw(15)
							<< chiOld << std::setw(15) << tofEvent - atofCable << std::setw(15) << path << std::setw(15)
							<< v0Event2 << std::setw(15) << v1Event2 << std::setw(15) << v2Event2 << std::setw(15)
							<< chiOld2 << std::setw(15) << tofEvent2 - atofCable << std::setw(15) << path2 << std::endl;

						numberOf2Clust++;
					}
				}
			}
			else
			{
				numberOfNoHits++;
			}

		}
	}
	/*
	* Summary
	*/

	outputFileOUT.close();
	outputFileTIM.close();
	outputFile2TT.close(); // outputFileSUM

	outputFileSUM << "Analyzed events = " << currentEvent << std::endl << "GPS events " << iGPSEvent << std::endl
		<< "****** Hit analysis ***************" << std::endl << "Events with no hits in a chamber = " << numberOfNoHits << std::endl
		<< "Events with 1 or 2 hits/chamber = " << numberOf2Hits << std::endl << "Event with more than 2 hits in a chamber = " << numberOf3Hits << std::endl
		<< "Hits multiplicity chamber BOTTOM" << std::endl;

	for (int i = 0; i < 50; i++)
	{
		if (mHitsB[i] != 0)
			outputFileSUM << i + 1 << std::setw(15) << mHitsB[i] << std::endl;
	}

	outputFileSUM << "Hits multiplicity chamber MIDDLE" << std::endl;

	for (int i = 0; i < 50; i++)
	{
		if (mHitsM[i] != 0)
			outputFileSUM << i + 1 << std::setw(15) << mHitsM[i] << std::endl;
	}

	outputFileSUM << "Hits multiplicity chamber TOP" << std::endl;

	for (int i = 0; i < 50; i++)
	{
		if (mHitsT[i] != 0)
			outputFileSUM << i + 1 << std::setw(15) << mHitsT[i] << std::endl;
	}

	outputFileSUM << "Hits total multiplicity" << std::endl;

	for (int i = 0; i < 50; i++)
	{
		if (mHitsTotal[i] != 0)
			outputFileSUM << i + 1 << std::setw(15) << mHitsTotal[i] << std::endl;
	}

	outputFileSUM << "******** Cluster analysis ************" << std::endl
		<< "Events with 1 cluster in each chamber = " << number1Clust << std::endl
		<< "Events with >=2 clusters in a chamber = " << numberOf3Clust << std::endl
		<< "Events with 2 clusters  in each chamber = " << numberOf2Clust << std::endl
		<< "Cluster multiplicity chamber BOTTOM" << std::endl;

	for (int i = 0; i < 50; i++)
	{
		if (mClusB[i] != 0)
			outputFileSUM << i + 1 << std::setw(15) << mClusB[i] << std::endl;
	}

	outputFileSUM << "Cluster multiplicity chamber MIDDLE" << std::endl;

	for (int i = 0; i < 50; i++)
	{
		if (mClusM[i] != 0)
			outputFileSUM << i + 1 << std::setw(15) << mClusM[i] << std::endl;
	}

	outputFileSUM << "Cluster multiplicity chamber TOP" << std::endl;

	for (int i = 0; i < 50; i++)
	{
		if (mClusT[i] != 0)
			outputFileSUM << i + 1 << std::setw(15) << mClusT[i] << std::endl;
	}

	outputFileSUM << "Cluster total multiplicity" << std::endl;

	for (int i = 0; i < 50; i++)
	{
		if (mClusTotal[i] != 0)
			outputFileSUM << i + 1 << std::setw(15) << mClusTotal[i] << std::endl;
	}

	outputFileSUM << " time cuts" << std::endl << " bottom chamber " << tbLowLimitLeft << std::setw(15) << tbHighLimitLeft
		<< std::setw(15) << tbLowLimitRight << std::setw(15) << tbHighLimitRight << std::endl;
	outputFileSUM << " middle chamber " << tmLowLimitLeft << std::setw(15) << tmHighLimitLeft
		<< std::setw(15) << tmLowLimitRight << std::setw(15) << tmHighLimitRight << std::endl;
	outputFileSUM << " top chamber " << ttLowLimitLeft << std::setw(15) << ttHighLimitLeft
		<< std::setw(15) << ttLowLimitRight << std::setw(15) << ttHighLimitRight << std::endl;

	/*timeBR = (nTimeBR <= 0)?(timeBR):((float)timeBR/nTimeBR);
	timeBL = (nTimeBL <= 0)?(timeBL):((float)timeBL/nTimeBL);
	timeMR = (nTimeMR <= 0)?(timeMR):((float)timeMR/nTimeMR);
	timeML = (nTimeML <= 0)?(timeML):((float)timeML/nTimeML);
	timeTR = (nTimeTR <= 0)?(timeTR):((float)timeTR/nTimeTR);
	timeTL = (nTimeTL <= 0)?(timeTL):((float)timeTL/nTimeTL);*/

	outputFileSUM << " average time of hits - no cuts" << std::endl << " bottomleft/right middleleft/right topleft/right" << std::endl;
	outputFileSUM << ((nTimeBL <= 0) ? (timeBL) : ((float)timeBL / nTimeBL)) << std::setw(15) << ((nTimeBR <= 0) ? (timeBR) : ((float)timeBR / nTimeBR)) << std::setw(15)
		<< ((nTimeML <= 0) ? (timeML) : ((float)timeML / nTimeML)) << std::setw(15) << ((nTimeMR <= 0) ? (timeMR) : ((float)timeMR / nTimeMR)) << std::setw(15)
		<< ((nTimeTL <= 0) ? (timeTL) : ((float)timeTL / nTimeTL)) << std::setw(15) << ((nTimeTR <= 0) ? (timeTR) : ((float)timeTR / nTimeTR)) << std::endl;

	tbLeft /= (float)numberOftbHits;
	tbRight /= (float)numberOftbHits;
	tmLeft /= (float)numberOftmHits;
	tmRight /= (float)numberOftmHits;
	ttLeft /= (float)numberOfttHits;
	ttRight /= (float)numberOfttHits;

	outputFileSUM << "avarage of time of hits" << std::endl << " bottom" << tbLeft << std::setw(15) << tbRight << std::setw(15) << numberOftbHits << std::endl
		<< " middle" << tmLeft << std::setw(15) << tmRight << std::setw(15) << numberOftmHits << std::endl
		<< " top   " << ttLeft << std::setw(15) << ttRight << std::setw(15) << numberOfttHits << std::endl;

	xBRA /= (float)numberxBRA;
	xMRA /= (float)numberxMRA;
	xTRA /= (float)numberxTRA;

	outputFileSUM << " avarage x ch bottom, ch middle, ch top" << std::endl << xBRA << std::setw(15) << numberxBRA << std::setw(15)
		<< xMRA << std::setw(15) << numberxMRA << std::setw(15) << xTRA << std::setw(15) << numberxTRA << std::endl;
	outputFileSUM << "out of range x coordinate" << std::endl << numberxBLow << std::setw(15) << numberxBHigh << std::setw(15) << numberxMLow
		<< std::setw(15) << numberxMHigh << std::setw(15) << numberxTLow << std::setw(15) << numberxTHigh << std::endl;

	/*
	* open calibration file...
	*/

	bool calibIsExists = inputCalib.is_open();
	if (calibIsExists)
		inputCalib.close();

	if (numberxBRA > 100 && numberxMRA > 100 && numberxTRA > 100)
	{
		std::ofstream outputCalib("eee_calib.txt", std::ios::out | std::ios::trunc);
		if (calibIsExists)
		{
			tbCorr += (78. - xBRA) / 10.;
			tmCorr += (78. - xMRA) / 10.;
			ttCorr += (78. - xTRA) / 10.;
		}
		else
		{
			tbCorr = (78. - xBRA);
			tmCorr = (78. - xMRA);
			ttCorr = (78. - xTRA);
		}

		outputCalib << tbCorr << std::setw(15) << tmCorr << std::setw(15) << ttCorr << std::endl
			<< tbLeft - 75 << std::setw(15) << tbLeft + 50 << std::setw(15) << tbRight - 75 << std::setw(15) << tbRight + 50 << std::endl
			<< tmLeft - 75 << std::setw(15) << tmLeft + 50 << std::setw(15) << tmRight - 75 << std::setw(15) << tmRight + 50 << std::endl
			<< ttLeft - 75 << std::setw(15) << ttLeft + 50 << std::setw(15) << ttRight - 75 << std::setw(15) << ttRight + 50 << std::endl;

		outputCalib.close();
	}
	//std::cout << "End of analysis" << std::endl;
	return 0;
}

void openInput(std::string fileName, std::ifstream& input)
{
	input.open(fileName, std::ios_base::binary);

	if (!input.is_open())
		exit(-1);

	char* buffer = new char[9];
	if (!input.read(buffer, 8))
	{
		//std::cout << "Something wrong" << std::endl;
	}

	buffer[8] = '\0';
	/*char* buffer;
	read(input, buffer, 8);*/

	std::string res(buffer);

	if (res.compare(" EEEataD") != 0)
		exit(-1);

	delete[] buffer;

	return;
}

void reOpenInput(std::ifstream& input)
{
	input.seekg(0, std::ios::beg);

	char* buffer = new char[9];
	if (!input.read(buffer, 8))
	{
		//std::cout << "Something wrong" << std::endl;
	}

	buffer[8] = '\0';
	std::string res(buffer);

	if (res.compare(" EEEataD") != 0)
		exit(-1);

	delete[] buffer;

	return;
}

int readInput(std::ifstream& input, int*& data, int& type, int& error)
{
	//reading the length of the following block
	char* buffer = new char[sizeOfInt];
	int pos = input.tellg();

	if (!input.read(buffer, 4))
	{
		error = 3;
		return 0;
	}

	int* len = (int*)buffer;
	int length = len[0];

	if (length < 1)
	{
		error = 1;
		return 0;
	}
	if (length > 8000)
	{
		error = 2;
		return 0;
	}

	length--;
	delete[] buffer;

	//reading the type of the following block
	buffer = new char[sizeOfInt];
	if (!input.read(buffer, 4))
	{
		//std::cout << "Something wrong" << std::endl;
	}

	int* typ = (int*)buffer;
	type = typ[0];

	length--;
	delete[] buffer;

	switch (type)
	{
	case 0:
	{
		data = new int[4];

		buffer = new char[sizeOfInt * 5];
		for (int i = 0; i < 5; i++)
		{
			if (!input.read(&(buffer[i*sizeOfInt]), 4))
			{
				//std::cout << "Something wrong" << std::endl;
			}
		}

		int* dat = (int*)buffer;

		data[0] = ((dat[1] & 0xFFFF) + ((dat[2] & 0x7FF) * 0x10000)) * 10;
		//data[0]=((iarray[2] & 0xFFFF)+((iarray[3] & 0x7FF)*0x10000))*10;  // nanosecs 
		data[1] = (dat[3] & 0xFFF) * 0x20 + ((dat[2] & 0xF800) >> 11);
		//idata[1]=(iarray[4] & 0xFFF)*0x20 + ((iarray[3] & 0xF800) >> 11); // seconds in day
		data[2] = ((dat[3] & 0xF000) >> 12) + ((dat[4] & 0x1F) * 0x10);
		//idata[2]=((iarray[4] & 0xF000) >> 12) + ((iarray[5]& 0x1F) * 0x10); // day in year
		data[3] = ((dat[4] & 0x3E0) >> 5) + 1996;
		//idata[3]=((iarray[5] & 0x3E0) >> 5) +1996 ;*/

		delete[] buffer;

		input.seekg((length - 5) * 4, std::ios::cur);

		break;
	}
	case 1:
	{}
	case 2:
	{
		int currentPosition = input.tellg();
		int numberOfCaenInformation = 0;

		for (int i = 0; i < length; i++)
		{
			buffer = new char[sizeOfInt];

			if (!input.read(buffer, 4))
			{
				std::cerr << "Something wrong" << std::endl;
			}

			int* dat = (int*)buffer;

			if ((dat[0] & 0xF8000000) == 0 && (dat[0] & 0x04000000) == 0)
				numberOfCaenInformation++;

			delete[] buffer;
		}
		input.seekg(currentPosition, std::ios::beg);

		data = new int[(++numberOfCaenInformation) * 3];
		int* dataFlag = new int[200];
		for (int i = 0; i < 200; i++)
			dataFlag[i] = 0;

		int extendedTimeTag = 0;
		int currentPos = 0;
		int counter = 0;

		for (int i = 0; i < length; i++)
		{
			buffer = new char[sizeOfInt];
			if (!input.read(buffer, 4))
			{
				//std::cout << "Something wrong" << std::endl;
			}

			int* dat = (int*)buffer;

			int wordCounter = 0;
			int tdcNumber = 0, tdcNumberTr = 0, tdcNumberErr = 0;
			int eventId = 0, eventIdTr = 0;
			int bunchId = 0;
			int errorFlags = 0;

			int caen = dat[0] & 0xF8000000;

			switch (caen)
			{
			case 0x40000000:
			{
				data[0] = (dat[0] & 0x07FFFFE0) >> 5;
				break;
			}
			case 0x80000000:
			{
				counter = (dat[0] & 0x1F);
				break;
			}
			case 0x08000000:
			{
				tdcNumber = (dat[0] & 0x03000000) >> 24;
				eventId = (dat[0] & 0x00FFF000) >> 12;
				bunchId = (dat[0] & 0x00000FFF);
				break;
			}
			case 0x18000000:
			{
				tdcNumberTr = (dat[0] & 0x03000000) >> 24;
				eventIdTr = (dat[0] & 0x00FFF000) >> 12;
				wordCounter = (dat[0] & 0x00000FFF);
				break;
			}
			case 0x20000000:
			{
				tdcNumberErr = (dat[0] & 0x03000000) >> 24;
				errorFlags = (dat[0] & 0x00003FFF);
				break;
			}
			case 0x88000000:
			{
				extendedTimeTag = (dat[0] & 0x07FFFFFF);
				break;
			}
			case 0:
			{
				int leading = dat[0] & 0x04000000;
				if (leading == 0)
				{
					int k = (++currentPos) * 3;

					data[k] = 1 + ((dat[0] & 0x03F80000) >> 19);
					dataFlag[data[k]] = k;
					data[k + 1] = (dat[0] & 0x0007FFFF);
					data[k + 2] = 0;
				}
				else
				{
					int channelNumber = 1 + ((dat[0] & 0x03F80000) >> 19);
					if (dataFlag[channelNumber] != 0)
					{
						data[dataFlag[channelNumber] + 2] = (dat[0] & 0x0007FFFF) - data[dataFlag[channelNumber] + 1];
						dataFlag[channelNumber] = 0;
					}
				}
			}

			}

			delete[] buffer;


		}
		data[1] = currentPos;
		data[2] = extendedTimeTag * 0x20 + counter;

		break;
	}
	case 5:
	{
	}
	case 6:
	{
		data = new int[length];

		for (int i = 0; i < length; i++)
		{
			buffer = new char[sizeOfInt];
			if (!input.read(buffer, 4))
			{
				//std::cout << "Something wrong" << std::endl;
			}

			int* dat = (int*)buffer;
			data[i] = dat[0];

			delete[] buffer;
		}
		break;
	}
	default:
	{
		data = new int[1]; //for delete

		input.seekg(length * 4, std::ios::cur);
	}
	}

	return 0;
}

int read(std::ifstream& input, char*& buffer, int length)
{
	buffer = new char[length + 1];
	buffer[length] = '\n';

	for (int i = 0; i < length; i++)
	{
		buffer[i] = input.peek();
		if (!input)
		{
			return -1;
		}
	}
	return 0;
}


void chambers(int& number, int difference, int iLeft, int iRight, float& left, float& right, int& numberOfHits, float* t, float* t2, int* iHitLeft, int* iHitRight, float timeOffset, float corr, float* xChamber, float* yChamber, float* tChamber)
{
	float x1 = 158;
	float* xp = new float[4];

	number = 0;
	for (int i = 0; i < 24; i++)
	{
		int kk1 = i + 1 + difference;
		if (iRight == 3)
		{
			kk1 = 25 + difference - (i + 1);
		}
		int kk2;

		if (t[kk1] > 0)
		{
			kk2 = i + 1 + 32 + difference;

			if (iLeft == 1)
			{
				kk2 = 57 - (i + 1) + difference;
			}
			if (t[kk2] > 0)
			{
				number++;

				xp[0] = 0.5*x1*(1 + (t[kk2] - t[kk1] - timeOffset) / 10) + corr;
				if (xp[0] < 0 || xp[0] > 158)
				{
					if (t2[kk1] > 0 || t2[kk2] > 0)
					{
						xp[1] = 0.5*x1*(1 + (t[kk2] - t2[kk1] - timeOffset) / 10) + corr;
						xp[2] = 0.5*x1*(1 + (t2[kk2] - t[kk1] - timeOffset) / 10) + corr;
						xp[3] = 0.5*x1*(1 + (t2[kk2] - t2[kk1] - timeOffset) / 10) + corr;

						for (int j = 0; j < 4; j++)
						{
							xp[j] = std::abs(xp[j] - 78);
						}

						float minXP = xp[0];
						int placeXP = 0;
						for (int j = 1; j < 4; j++)
						{
							if (xp[j] < minXP)
							{
								minXP = xp[j];
								placeXP = j;
							}
						}
						switch (placeXP)
						{
						case 1:
						{
							t[kk1] = t2[kk1];
							break;
						}
						case 2:
						{
							t[kk2] = t2[kk2];
							break;
						}
						case 3:
						{
							t[kk1] = t2[kk1];
							t[kk2] = t2[kk2];
							break;
						}
						}
					}
				}
				left += t[kk2];
				right += t[kk1];
				numberOfHits++;

				/*  Y-coordinate is perpendicular to strip direction   Y=0 for strip 1   Y=82 for strip 24
				*  X-coordinate is along the strip direction and obtained from the time-difference
				*  X is proportional to (T_left-T_right) which goes from -10 ns to +10 ns
				*  (T_left - T_right)=-9  X=0
				*  (T_left - T_right)=+9  X=158
				*
				*  X  |0---------------------------------------> 158
				*     |
				*     | Left                                    Right
				*     |
				*  Y  |82
				*                                                 V
				*/
				iHitLeft[number - 1] = kk1;
				iHitRight[number - 1] = kk2;

				yChamber[number - 1] = ((float)i + 1)*3.2;
				xChamber[number - 1] = 0.5*x1*(1.0 + (t[kk2] - t[kk1] - timeOffset) / 10.) + corr;
				tChamber[number - 1] = (t[kk2] + t[kk1]) / 2;
			}
		}
	}
}

void merge(int& number, int* iHitR, int* iHitL, int* iHitTR, int* iHitTL, float* xChamber, float* yChamber, float* tChamber)
{
	int k = 0;

	while (k < number - 1)
	{
		int j = k + 1;
		int strip1 = iHitR[k];
		int strip2 = iHitR[j];

		if (std::abs(strip1 - strip2) < 2)
		{
			if (tChamber[k] > tChamber[j])
			{
				tChamber[k] = tChamber[j];
				xChamber[k] = xChamber[j];
			}
			yChamber[k] = (yChamber[j] + yChamber[k]) / 2;

			for (int i = j; i < number - 1; i++)
			{
				yChamber[i] = yChamber[i + 1];
				xChamber[i] = xChamber[i + 1];
				tChamber[i] = tChamber[i + 1];




				iHitR[i] = iHitTR[i + 1];
				iHitL[i] = iHitTL[i + 1];
			}

			number--;
		}
		k++;
	}
}

