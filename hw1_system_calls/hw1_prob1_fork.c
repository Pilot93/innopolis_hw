#include <unistd.h>
int main()
{
	int i;
	i = 5;
	while(i) {
		fork();
		sleep(5);
		i--;
	}
	return 0;
}
