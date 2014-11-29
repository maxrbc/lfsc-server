
// Struct definition for the message communication and storing



#ifndef __SPA_POSITIONS_H
#define __SPA_POSITIONS_H

typedef struct {
	double motors_position [5];
	double motors_last[5];
	double azimuth ;
	double zenith ;
} motors;

#define TIME_INTERVAL  240// 4 min interval in seconds to be used if ask to calculate more than one position

void calculate_stream_dates(time_t time , time_t results[] , int measures);

int running_with_epoch(time_t init, int measures, double machine_pos[]);
int make_position_calculation(motors *motors_data ,struct tm *local , double machine_pos[]);
int make_position_calculation_sec(motors *motors_data , time_t *date , double machine_pos[]);
int calculate_measures_between_dates(time_t init , time_t final);

time_t add_seconds_to_date(time_t *date , int min );
time_t parse_date(char str[]);





#endif /* __SPA_POSITIONS_H */
