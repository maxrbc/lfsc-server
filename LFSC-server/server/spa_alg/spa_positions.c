
#include <stdio.h>
#include <ctype.h>
#include <unistd.h>
#include <stdlib.h>
#include <getopt.h>

#include <time.h>
#include <math.h>
#include "spa.h"
#include "spa_positions.h"



int main(int argc , char *argv[]){

	double lat,lon,height = {0};
	time_t initial = parse_date(argv[1]);
	time_t final = parse_date(argv[2]);

	lat = atof(argv[3]);
	lon = atof(argv[4]);
	height = atof(argv[5]);

	double machine_position[] = { lat , lon , height };
	int measures = calculate_measures_between_dates(initial,final) + 1;
	printf("MEASURES : %d\n",measures);


	running_with_epoch(initial, measures , machine_position);
	return 0;
}

int running_with_epoch(time_t init, int measures , double machine_pos[]){

	motors motor_data;
	time_t stream[measures];

	calculate_stream_dates(init,stream,measures);

	int i;
	for( i = 0 ; i < measures ; i++){

		printf("===============================================================\n");
		make_position_calculation_sec(&motor_data,&stream[i] , machine_pos);


	}


	return 0;
}




int make_position_calculation_sec(motors *motors_data , time_t *date , double machine_pos[]){
	struct tm *local = localtime(date);
	printf("Date is > %s\n",asctime(local));
	make_position_calculation(motors_data,local , machine_pos);
	return 0;
}

time_t add_seconds_to_date(time_t *date , int min ){

	struct tm *local = localtime(date);
	local->tm_sec = local->tm_sec + min;
	time_t result = mktime(local);
	return result ;
}

void calculate_stream_dates(time_t time , time_t results[] , int measures){

	int num_measures ;
	results[0] = time;


	for ( num_measures = 1 ; num_measures < measures ; num_measures++){
		results[num_measures] = (time_t)add_seconds_to_date(&time,(num_measures*TIME_INTERVAL));
	}

	return;
}

int calculate_measures_between_dates(time_t init, time_t final){

	double delta = difftime(final,init);
	int result = (int)(delta/240);

	return result;
}


time_t parse_date(char str[]){

	int day,month,year,hour,min = {0};
	time_t cur_date = time(NULL);
	struct tm *date = localtime(&cur_date);

	sscanf(str,"%d/%d/%d/%d:%d",&month,&day,&year,&hour,&min);
	date->tm_year = (year - 1900);
	date->tm_mon = (month -1 );
	date->tm_mday = day;
	date->tm_hour = hour;
	date->tm_min = min;
	date->tm_sec = 0;

	return mktime(date);

}


int make_position_calculation(motors *motors_data ,struct tm *local , double machine_pos[])
{

	spa_data spa;


	spa.year = (1900 + local->tm_year);
	spa.month = (local->tm_mon + 1);
	spa.day = local->tm_mday;
	spa.hour = local->tm_hour;
	spa.minute = local->tm_min;
	spa.second = local->tm_sec;

	spa.timezone = -4;
	spa.latitude = machine_pos[0];
	spa.longitude = machine_pos[1];
	spa.elevation = machine_pos[2];

// 18.21 -67.14 12

	spa_calculate(&spa);
	motors_data->zenith = (spa.zenith);
	motors_data->azimuth = (spa.azimuth - 180);

	printf(" The azimuth > %f \n The zenith > %f \n",motors_data->azimuth , motors_data->zenith);
	return 0;


}

