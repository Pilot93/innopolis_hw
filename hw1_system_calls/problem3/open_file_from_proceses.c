#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <sys/wait.h>

int	main (){
	int	process, c;
	FILE *f;
	f = fopen("text.txt", "r");
	if(!f) {
		perror("text.txt");
		exit(1);
	}
	process = fork();
			if (process == -1) {
				perror("fork");
				exit(1);
			}
			if (process == 0) {
				c = fgetc(f);
				printf("child read: %c\n", c);
				exit(1);
			}
			c = fgetc(f);
			printf("parent read: %c\n", c);
			fclose(f);
	return 0;
}
